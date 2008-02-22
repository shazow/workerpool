# jobs.py - Generic jobs used with the worker pool

from exceptions import TerminationNotice

class Job(object):
    "Interface for a Job object."
    def __init__(self):
        pass

    def run(self):
        "The actual task for the job should be implemented here."
        pass

class SuicideJob(Job):
    "A worker receiving this job will commit suicide."
    def run(self, **kw):
        raise TerminationNotice()

class SimpleJob(Job):
    """
    Given a `result` queue, a `method` pointer, and an `args` dictionary or
    list, the method will execute r = method(*args) or r = method(**args), 
    depending on args' type, and perform result.put(r).
    """
    def __init__(self, result, method, args=[]):
        self.result = result
        self.method = method
        self.args = args

    def run(self):
        if isinstance(self.args, list):
            r = self.method(*self.args)
        elif isinstance(self.args, dict):
            r = self.method(**self.args)
        self.result.put(r)

