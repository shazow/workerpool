from workerpool import WorkerPool

"""
WARNING: This sample class is obsolete since version 0.9.2. It will be removed
or replaced soon.
"""


class BlockingWorkerPool(WorkerPool):
    """
    Similar to WorkerPool but a result queue is passed in along with each job
    and the method will block until the queue is filled with one entry per job.

    Bulk job lists can be performed using the `contract` method.
    """
    def put(self, job, result):
        "Perform a job by a member in the pool and return the result."
        self.job.put(job)
        r = result.get()
        return r

    def contract(self, jobs, result):
        """
        Perform a contract on a number of jobs and block until a result is
        retrieved for each job.
        """
        for j in jobs:
            WorkerPool.put(self, j)

        r = []
        for i in xrange(len(jobs)):
            r.append(result.get())

        return r
