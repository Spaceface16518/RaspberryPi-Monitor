from datetime import datetime
from threading import Event, Thread

import psutil

from models import Log, Reading


class Worker(Thread):
    def __init__(self, terminate: Event, delay: float = 600.0, args=None, kwargs=None) -> None:
        super().__init__(name="worker")
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.terminate = terminate
        self.delay = delay

    def work(self, *args, **kwargs):
        pass

    def run(self) -> None:
        while True:
            self.work(*self.args, **self.kwargs)
            if self.terminate.wait(self.delay):
                break


class TemperatureLogger(Worker):
    def __init__(self, mongo, terminate: Event):
        super().__init__(terminate, args=[mongo])

    def work(self, *args, **kwargs):
        mongo = args[0]
        read_time = datetime.now()
        reading = Reading(psutil.sensors_temperatures())
        log = Log(reading, created=read_time)
        return mongo.db.temperatures.insert_one(log)
