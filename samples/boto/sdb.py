"""
Collection of Amazon Web Services related jobs. Due to the distributed nature
of AWS, executing calls in parallel is super useful.
"""

from workerpool import *

try:
    import boto
    from boto.sdb.domain import Domain
except ImportError:
    print """
    This module requires `boto` to communicate with Amazon's web services.
    Install it using easy_install:
        easy_install boto
    Or get it from:
        http://code.google.com/p/boto/
    """
    raise

class SDBToolBox(object):
    "Create a connection to SimpleDB and hold on to it."
    def __init__(self, domain):
        self.conn = boto.connect_sdb()
        self.domain = self.conn.get_domain(domain)

class SdbJob(SimpleJob):
    def run(self, toolbox):
        assert isinstance(toolbox.domain, self.method.im_class), "Method pointer must come from the Domain class"
        r = self.method(toolbox.domain, *self.args)
        self.result.put(r)

# Sample usage
import time
from Queue import Queue

def main():
    DOMAIN = "benchmark"
    conn = boto.connect_sdb()
    domain = conn.get_domain(DOMAIN)

    # Prepare item list
    items = []
    now = time.time()
    for i in domain:
        items.append(i)
    elapsed = time.time() - now

    if not items:
        print "No items found."
        return

    print "Fetched manifest of %d items in %f seconds, proceeding." % (len(items), elapsed)

    # THE REAL MEAT:

    # Prepare the pool
    print "Initializing pool."

    def toolbox_factory():
        return SDBToolBox(DOMAIN)
    def worker_factory(job_queue):
        return EquippedWorker(job_queue, toolbox_factory)
    
    pool = WorkerPool(size=20, worker_factory=worker_factory)

    print "Starting to fetch items..."
    now = time.time()

    # Insert jobs
    results_queue = Queue()
    for i in items:
        j = SdbJob(results_queue, boto.sdb.domain.Domain.get_item, [i])
        pool.put(j)

    # Fetch results
    r = [results_queue.get() for i in items]
    elapsed = time.time() - now

    print "Fetched %d items paralleled in %f seconds." % (len(r), elapsed)

    pool.shutdown()

if __name__ == "__main__":
    main()

