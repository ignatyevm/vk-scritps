import asyncio
import datetime
import logging
import time
from collections import defaultdict
from typing import Awaitable

from .models import Timing

logger = logging.getLogger("vk-scripts.broadcaster.scheduler")


class Scheduler:
    tasks_by_timings: dict[Timing, list[Awaitable]] = defaultdict(list)

    def __init__(self, event_loop):
        self.event_loop = event_loop

    def make_timing(
            self,
            time: datetime.datetime,
            *,
            use_weekday: bool = False
    ) -> Timing:
        if use_weekday:
            return Timing(
                hour=time.hour,
                minute=time.minute,
                weekday=time.weekday() + 1
            )
        return Timing(hour=time.hour, minute=time.minute)

    def register_task(self, timing: Timing, task: Awaitable):
        self.tasks_by_timings[timing].append(task)

    def try_execute_tasks(self):
        async def execute_tasks(tasks):
            for task in tasks:
                asyncio.create_task(task)

        def try_execute_tasks_by_timing(timing):
            if timing in self.tasks_by_timings:
                asyncio.create_task(
                    execute_tasks(self.tasks_by_timings[timing])
                )

        current_time = datetime.datetime.now()
        current_timing = self.make_timing(current_time)
        current_timing_with_weekday = self.make_timing(
            current_time, use_weekday=True
        )

        have_tasks = (
            current_timing in self.tasks_by_timings
            or current_timing_with_weekday in self.tasks_by_timings
        )
        if not have_tasks:
            logger.debug("no tasks to execute")
            return

        try_execute_tasks_by_timing(current_timing)
        try_execute_tasks_by_timing(current_timing_with_weekday)

    async def run(self):
        if len(self.tasks_by_timings) == 0:
            return

        logger.debug("entered to scheduler loop")
        delay = 60.0
        next_time = time.time() + delay
        while True:
            self.try_execute_tasks()
            logger.debug("moved to next iteration")
            await asyncio.sleep(max(0.0, next_time - time.time()))
            next_time += (time.time() - next_time) // delay * delay + delay
