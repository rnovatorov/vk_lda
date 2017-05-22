import vk
import time
import progressbar as pb
import json


def get_all_posts(owner_id, filt):
    """
    Gets all posts
    requires waiting for some time (works with 0.4 for me)
    to get everything
    """
    print "Looking for %s posts on %d wall..." % (filt, owner_id)

    response = api.wall.get(owner_id=owner_id, count=1, filter=filt)
    volume = response[0]

    print "%d %s posts found on %d wall." % (volume, filt, owner_id)
    if not volume:
        print "Posts downloaded: 0\n"
        return []

    full_wall = []
    offset = 0
    while len(full_wall) != volume:
        if volume - len(full_wall) >= 100:
            count = 100
        else:
            count = volume - len(full_wall)
        bunch = api.wall.get(owner_id=owner_id,
                             count=count,
                             offset=offset,
                             filter=filt)
        full_wall.extend(bunch[1:]) # first elements is count
        offset += count
        time.sleep(0.3)

    print "Posts downloaded: %d\n" % len(full_wall)

    return full_wall


def get_post_comments(post, need_likes=0):
    """
    Gets all comments
    requires waiting for some time (works with 0.4 for me)
    to get everything
    """
    owner_id = post["from_id"]
    post_id = post["id"]
    try:
        time.sleep(0.4)
        response = api.wall.getComments(owner_id=owner_id,
                                        post_id=post_id,
                                        count=1)
    except Exception as e:
        print e
        return []
    volume = response[0]
    comments = []
    offset = 0
    time.sleep(0.4)
    while len(comments) != volume:
        if volume - len(comments) >= 100:
            count = 100
        else:
            count = volume - len(comments)
        bunch = api.wall.getComments(owner_id=owner_id,
                                     post_id=post_id,
                                     count=count,
                                     offset=offset,
                                     need_likes=need_likes)
        comments.extend(bunch[1:]) # first element is count
        offset += count
        time.sleep(0.4)
    return comments


if __name__ == "__main__":
    group_id = -108394847

    # VK api part
    access_token = ""
    session = vk.Session(access_token=access_token)
    api = vk.API(session)

    group_posts = (get_all_posts(group_id, filt="owner") +
                   get_all_posts(group_id, filt="others"))

    bar = pb.ProgressBar(maxval=len(group_posts), widgets=[
        "Downloading comments: ",
        pb.Bar(left="[", marker="=", right="] "),
        pb.SimpleProgress(),
    ]).start()

    with open("blank.txt", "w") as f:
        for n, post in enumerate(group_posts):
            bar.update(n + 1)
            comments = get_post_comments(post, need_likes=1)
            doc = {"_id": post["id"],
                   "post": post["text"],
                   "comments": comments}
            json.dump(doc, f)
    bar.finish()
    print "Done.\n"
