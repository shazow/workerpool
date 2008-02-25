# workerpool.py - Module for distributing jobs to a pool of worker threads.
# Copyright (c) 2008 Andrey Petrov
#
# This module is part of workerpool and is released under
# the MIT license: http://www.opensource.org/licenses/mit-license.php

from Queue import Queue
from workers import Worker
from jobs import SimpleJob, SuicideJob

class WorkerPool:
    """
    Initialize a pool of threads which will be used to perform operations.

    size = 1
        Number of active worker threads the pool should contain.

    maxjobs = 0
        Maximum number of jobs to allow in the queue at a time. Will block on
        `put` if full.

    WorkerClass = Worker
        Class pointer to a Worker object to instantiate.

    workerargs = None
        Arguments to pass to the WorkerClass constructor (list or dict).
    """
    def __init__(self, size=1, maxjobs=0, WorkerClass=Worker, workerargs=None):
        self._WorkerClass = WorkerClass
        self._workerargs = workerargs
        self._jobs = Queue(maxjobs) # This queue will contain Job objects read by the workers.
        self._size = 0 # Number of active workers we have

        # Oh noes, we're understaffed. Hire some workers!
        for i in xrange(size):
            self.grow()

    def __repr__(self):
        return "%s(size=%d, WorkerClass=%s, workerargs=%r)" % (self.__class__.__name__, self.size(), self._WorkerClass.__name__, self._workerargs)

    def __del__(self):
        "Retire the workers."
        for i in xrange(self.size()):
            self.put(SuicideJob())

    def grow(self):
        "Add another worker to the pool."
        # TODO: Is there a benefit to hiring a specific type of worker? (Pool of mixed workers?)
        # TODO: This part is kind of nasty... Come up with something cleverer
        workerargs = self._workerargs
        if isinstance(workerargs, list):
            t = self._WorkerClass(self._jobs, *workerargs)
        elif isinstance(workerargs, dict):
            t = self._WorkerClass(self._jobs, **workerargs)
        else:
            t = self._WorkerClass(self._jobs)
        t.start()
        self._size += 1

    def shrink(self):
        "Get rid of one worker from the pool. Raises IndexError if empty."
        if self._size <= 0:
            raise IndexError("pool is already empty")
        self._size -= 1
        self.put(SuicideJob())

    def put(self, job, block=True, timeout=None):
        """
        Insert a job into the pool queue. Takes same parameters as a Queue
        object.

        Hint: Have the job append the results to a queue shared by all workers,
        from which the caller will read an expected number of results.
        """
        self._jobs.put(job, block, timeout)

    def wait(self):
        "Block until all jobs are completed."
        self._jobs.join()

    def size(self):
        "Approximate number of active workers (could be more if a shrinking is in progress)."
        return self._size

    def map(self, fn, seq, JobClass=SimpleJob):
        "Perform a map operation distributed among the workers. Will block until done."
        # TODO: Enhance this method to support multiple sequences similarly to
        # the built-in version of map.
        results = Queue()
        for s in seq:
            j = JobClass(results, fn, [s])
            self.put(j)

        # Aggregate results
        r = []
        for i in xrange(len(seq)):
            r.append(results.get())

        return r
