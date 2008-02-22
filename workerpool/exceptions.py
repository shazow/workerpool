# exceptions.py - Exceptions used in the operation of a worker pool

class TerminationNotice(Exception):
    "This exception is raised inside a thread when it's time for it to die."
    pass


