WorkerPool
==========
*Performing tasks in many threads made fun!*

The workerpool module is a simple framework for easily distributing jobs
into multiple worker threads.

Examples of usage can be found in the unit tests ([/test](https://github.com/shazow/workerpool/tree/master/test)) and the samples provided ([/samples](https://github.com/shazow/workerpool/tree/master/samples)).

This module facilitates distributing simple operations into jobs that are sent
to worker threads, maintained by a pool object.

It consists of these components:

* **Jobs** - single units of work that need to be performed.
* **Workers** - workers grab jobs from a queue and run them.
* **Worker pool** - keeps track of workers and the job queue.

## Getting Started
The best place to start for now is to read the code and look at the examples in
the unit tests ([/test](https://github.com/shazow/workerpool/tree/master/test)) and the sample uses ([/samples](https://github.com/shazow/workerpool/tree/master/samples)). Documentation contributions are welcome! What have you
accomplished with the workerpool?

## Tutorials:
[MassDownloader](https://github.com/shazow/workerpool/wiki/Mass-Downloader) - How to write a simple multi-threaded mass downloader in under
10 lines of code.


## Status
There's good work being done on a native Python multiprocessing module. The
functionality has a lot of overlap with workerpool. Worth having a look at!

## News
* 2011-06-02: Migrating project to Github. https://github.com/shazow/workerpool
* 2008-03-09: Released workerpool 0.9.2 (CHANGES) Warning: WorkerPool constructor signature changed.
* 2008-03-02: Released workerpool 0.9.1 (CHANGES)
* 2008-03-02: Added MassDownloader tutorial.
* TODO

Add more complete usage examples and wiki tutorials.
More thorough unit testing
Finalize the API for a 1.0 release

## Who's Using WorkerPool?
* [s3funnel](https://github.com/shazow/s3funnel) - Multithreaded tool for performing operations on Amazon's S3
* [starcluster](https://github.com/jtriley/StarCluster) - Tool for creating clusters of virtual machines on EC2

Are you using it? Let us know!

## Credit
This module was originally developed during my work at Idée Inc. Big thanks to
Idée for letting me open source it!

## License/Copyright
Copyright (c) 2008 Andrey Petrov (andrey.petrov@shazow.net)

Original copyright by Idee Inc. (http://ideeinc.com/)