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
        if isinstance(self.args, list):
            r = self.method(toolbox.domain, *self.args)
        elif isinstance(self.args, dict):
            r = self.method(toolbox.domain, **self.args)
        self.result.put(r)

# Sample usage

def main():
    import time
    conn = boto.connect_sdb()
    domain = conn.get_domain("benchmark")

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
    pool = WorkerPool(size=20, WorkerClass=EquippedWorker, workerargs={'toolbox': (SDBToolBox, ['benchmark'])})

    print "Starting to fetch items..."
    now = time.time()
    r = pool.map(boto.sdb.domain.Domain.get_item, items, JobClass=SdbJob)
    elapsed = time.time() - now

    print "Fetched %d items paralleled in %f seconds." % (len(r), elapsed)

    del pool

if __name__ == "__main__":
    main()

