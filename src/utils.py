import sys
import time
import threading
import json


def merge_iterators(*args):
    for iterator in args:
        for i in iterator:
            yield i


def json_dump(serializable, output_path, indent=2):
    with open(output_path, "w") as f:
        json.dump(serializable, f, indent=indent)


class Loading(object):
    """
    Print three dots repeatedly, like so:
        Loading.
        Loading..
        Loading...
        Loading.
        Loading..
        Loading...
    """ 
    def __init__(self, msg="Loading", time_gap=1):
        self.done = False
        self.dots_amount = 3
        self.msg = msg
        self.time_gap = time_gap
        self.PYTHON_VERSION = sys.version_info.major

    def __enter__(self):
        self.start()

    def __exit__(self, *exc):
        self.stop()

    def start(self):
        if self.PYTHON_VERSION == 2:
            cmd = "print self.msg,"
        elif self.PYTHON_VERSION == 3:
            cmd = "print(self.msg, end=' ')"
        else:
            raise NotImplementedError("WTF PYTHON %d???" % PYTHON_VERSION)
        exec(cmd)  # Dirty hack

        t = threading.Thread(target=self.print_dots,
                             args=(self.msg, self.time_gap))
        t.daemon = True
        t.start()

    def stop(self):
        self.done = True

    def print_dots(self, msg, time_gap):
        while not self.done:
            spaces = " " * self.dots_amount
            sys.stdout.write("\r%s%s" % (msg, spaces))
            for i in range(1, self.dots_amount + 1):
                dots = "." * i
                sys.stdout.write("\r%s%s" % (msg, dots))
                sys.stdout.flush()
                time.sleep(time_gap)
        num_spaces_to_clean = len(msg) + self.dots_amount
        print("\r%s\n" % " " * num_spaces_to_clean)
        print("hi")
        sys.stdout.flush()
