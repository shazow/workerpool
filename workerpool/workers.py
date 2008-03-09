# workers.py - Worker objects who become members of a worker pool
# Copyright (c) 2008 Andrey Petrov
#
# This module is part of workerpool and is released under
# the MIT license: http://www.opensource.org/licenses/mit-license.php

from threading import Thread
from jobs import Job, SimpleJob
from exceptions import TerminationNotice

class Worker(Thread):
    """
    A loyal worker who will pull jobs from the `jobs` queue and perform them.

    The run method will get jobs from the `jobs` queue passed into the
    constructor, and execute them. After each job, task_done() must be executed
    on the `jobs` queue in order for the pool to know when no more jobs are
    being processed.
    """

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
                self.jobs.task_done()
            except TerminationNotice:
                self.jobs.task_done()
                break 

class EquippedWorker(Worker):
    """
    Each worker will create an instance of ``toolbox`` and hang on to it during
    its lifetime. This can be used to pass in a resource such as a persistent 
    connections to services that the worker will be using.

    A ``toolbox`` is a ``(klass, args)`` tuple, where klass is a reference to a
    Class and args is a list or dictionary of parameters that will be passed
    into the constructor of the klass.
    """
    # TODO: Should a variation of this become the default Worker someday?

    def __init__(self, jobs, toolbox):
        klass, args = toolbox
        if isinstance(args, list):
            self.toolbox = klass(*args)
        elif isinstance(args, dict):
            self.toolbox = klass(**args)
        Worker.__init__(self, jobs)

    def run(self):
        "Get jobs from the queue and perform them as they arrive."
        while 1:
            job = self.jobs.get()
            try:
                job.run(toolbox=self.toolbox)
                self.jobs.task_done()
            except TerminationNotice:
                self.jobs.task_done()
                break
