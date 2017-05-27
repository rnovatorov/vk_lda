def merge_iterators(*args):
    for iterator in args:
        for i in iterator:
            yield i
