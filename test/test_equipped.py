import unittest
import sys
sys.path.append('../')

from six.moves import range
from six.moves.queue import Queue

import workerpool


class Counter(object):
    "Counter resource used for testing EquippedWorker."
    def __init__(self):
        self.count = 0


class CountJob(workerpool.Job):
    "Job that just increments the count in its resource and append it to the"
    "results queue."
    def __init__(self, results):
        self.results = results

    def run(self, toolbox):
        "Append the current count to results and increment."
        self.results.put(toolbox.count)
        toolbox.count += 1


class TestEquippedWorkers(unittest.TestCase):
    def test_equipped(self):
        """
        Created equipped worker that will use an internal Counter resource to
        keep track of the job count.
        """
        results = Queue()

        def toolbox_factory():
            return Counter()

        def worker_factory(job_queue):
            return workerpool.EquippedWorker(job_queue, toolbox_factory)

        pool = workerpool.WorkerPool(1, worker_factory=worker_factory)

        # Run 10 jobs
        for i in range(10):
            j = CountJob(results)
            pool.put(j)

        # Get 10 results
        for i in range(10):
            r = results.get()
            # Each result should be an incremented value
            self.assertEquals(r, i)

        pool.shutdown()
