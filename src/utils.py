def compose_doc(post, comments, formatting):
    if formatting not in ["short", "full"]:
        raise NotImplementedError("%s formatting is not supported" % formatting)
    doc = {}
    if not post:
        return doc
    if formatting == "short":
        doc["post"] = post["text"]
        doc["comments"] = [c["text"] for c in comments if c["text"]]
    elif formatting == "full":
        doc["post"] = post
        doc["comments"] = comments
    return doc


def merge_iterators(*args):
    for iterator in args:
        for i in iterator:
            yield i
