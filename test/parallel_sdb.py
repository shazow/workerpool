import boto
import time
c = boto.connect_sdb()
d = c.get_domain("benchmark")

# Prepare item list
items = []
now = time.time()
for i in d:
    items.append(i)
elapsed = time.time() - now

if not items:
    print "No items found."
    exit()

print "Fetched %d items serially in %f seconds, proceeding." % (len(items), elapsed)

import workerpool

pool = workerpool.WorkerPool(10)

now = time.time()
r = pool.map(d.get_item, items[:5])
elapsed = time.time() - now

print "Fetched %d items paralleled in %f seconds." % (len(r), elapsed)

del pool
