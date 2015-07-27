import unittest
import sys
sys.path.append('../')

from six.moves import range
from six.moves.queue import Queue, Empty

import workerpool


class TestWorkerPool(unittest.TestCase):
    def double(self, i):
        return i * 2

    def add(self, *args):
        return sum(args)

    def test_map(self):
        "Map a list to a method to a pool of two workers."
        pool = workerpool.WorkerPool(2)

        r = pool.map(self.double, [1, 2, 3, 4, 5])
        self.assertEquals(set(r), {2, 4, 6, 8, 10})
        pool.shutdown()

    def test_map_multiparam(self):
        "Test map with multiple parameters."
        pool = workerpool.WorkerPool(2)
        r = pool.map(self.add, [1, 2, 3], [4, 5, 6])
        self.assertEquals(set(r), {5, 7, 9})
        pool.shutdown()

    def test_wait(self):
        "Make sure each task gets marked as done so pool.wait() works."
        pool = workerpool.WorkerPool(5)
        q = Queue()
        for i in range(100):
            pool.put(workerpool.SimpleJob(q, sum, [range(5)]))
        pool.wait()
        pool.shutdown()

    def test_init_size(self):
        pool = workerpool.WorkerPool(1)
        self.assertEquals(pool.size(), 1)
        pool.shutdown()

    def test_shrink(self):
        pool = workerpool.WorkerPool(1)
        pool.shrink()
        self.assertEquals(pool.size(), 0)
        pool.shutdown()

    def test_grow(self):
        pool = workerpool.WorkerPool(1)
        pool.grow()
        self.assertEquals(pool.size(), 2)
        pool.shutdown()

    def test_changesize(self):
        "Change sizes and make sure pool doesn't work with no workers."
        pool = workerpool.WorkerPool(5)
        for i in range(5):
            pool.grow()
        self.assertEquals(pool.size(), 10)
        for i in range(10):
            pool.shrink()
        pool.wait()
        self.assertEquals(pool.size(), 0)

        # Make sure nothing is reading jobs anymore
        q = Queue()
        for i in range(5):
            pool.put(workerpool.SimpleJob(q, sum, [range(5)]))
        try:
            q.get(block=False)
        except Empty:
            pass  # Success
        else:
            assert False, "Something returned a result, even though we are"
            "expecting no workers."
        pool.shutdown()
