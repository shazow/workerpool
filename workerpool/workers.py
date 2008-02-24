# workers.py - Worker objects who become members of a worker pool
# Copyright (c) 2008 Andrey Petrov
#
# This module is part of workerpool and is released under
# the MIT license: http://www.opensource.org/licenses/mit-license.php

from threading import Thread
from jobs import Job, SimpleJob
from exceptions import TerminationNotice

class Worker(Thread):
    "A loyal worker who will pull jobs from the `jobs` queue and perform them."
    DefaultJob = SimpleJob

    def __init__(self, jobs):
        self.jobs = jobs
        Thread.__init__(self)

    def run(self):
        "Get jobs from the queue and perform them as they arrive."
        while 1:
            # Sleep until there is a job to perform.
            job = self.jobs.get()
            # Yawn. Time to get some work done.
            try:
                job.run()
            except TerminationNotice:
                break 
            finally:
                # Get ready for bed
                self.jobs.task_done()

class EquippedWorker(Worker):
    """
    Each worker will create an instance of `toolbox` and hang on to it through
    its lifetime. This can be used to pass in persistent connections to
    services that the worker will be using.

    TODO: Should this become the default Worker someday?
    """
    DefaultJob = SimpleJob

    def __init__(self, jobs, toolbox):
        cls, args = toolbox
        if isinstance(args, list):
            self.toolbox = cls(*args)
        elif isinstance(args, dict):
            self.toolbox = cls(**args)
        Worker.__init__(self, jobs)

    def run(self):
        "Get jobs from the queue and perform them as they arrive."
        while 1:
            job = self.jobs.get()
            try:
                job.run(toolbox=self.toolbox)
            except TerminationNotice:
                break
            finally:
                self.jobs.task_done()

