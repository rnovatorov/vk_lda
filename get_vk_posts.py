#! venv/bin/python


import json
from argparse import ArgumentParser
from tqdm import tqdm
# Project
import config as conf
from src.utils import merge_iterators
from src.VKPostsGetter import VKPostsGetter


def main(args):
    # Initialising VKPostsGetter
    vkpg = VKPostsGetter(vk_access_token=conf.VK_ACCESS_TOKEN,
                         wait_time=conf.WAIT_TIME)

    # Getting owner's posts generator
    owner_posts_volume = vkpg.count_posts(args.owner_id,
                                          vk_filter=conf.VK_FILTER_OWNER)
    owner_posts = vkpg.get_posts(args.owner_id,
                                 volume=owner_posts_volume,
                                 vk_filter="owner")

    # Getting others' posts generator
    others_posts_volume = vkpg.count_posts(args.owner_id,
                                           vk_filter=conf.VK_FILTER_OTHERS)
    others_posts = vkpg.get_posts(args.owner_id,
                                  volume=others_posts_volume,
                                  vk_filter="others")

    # Counting total amount of posts to download
    groups_posts_volume = owner_posts_volume + others_posts_volume

    # Merging them together
    group_posts = merge_iterators(owner_posts, others_posts)

    print("Downloading...")
    docs = []
    for n, post in tqdm(enumerate(group_posts), total=groups_posts_volume):
        if args.need_comments:
            comments = vkpg.get_comments(post, need_likes=args.need_likes)
        else:
            comments = []
        doc = compose_doc(post, comments, full_posts=args.full_posts)
        if doc:
            docs.append(doc)
    
    print("Saving...")
    with open(args.output_path, "w") as f:
        json.dump(docs, f, indent=args.indent)
    print("Done")

def compose_doc(post, comments, full_posts):
    doc = {}
    if not post:
        return doc
    if full_posts:
        doc["post"] = post
        doc["comments"] = comments
    else:
        doc["post"] = {"text": post["text"]}
        doc["comments"] = [{"text": c["text"]} for c in comments]
    return doc


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("owner_id",
        type=int,
        help=""
    )
    arg_parser.add_argument("-o",
        dest="output_path",
        required=True,
        help=""
    )
    arg_parser.add_argument("-f",
        dest="full_posts",
        action="store_true",
        required=False,
        default=False,
        help=""
    )
    arg_parser.add_argument("-c",
        dest="need_comments",
        action="store_true",
        required=False,
        default=False,
        help=""
    )
    arg_parser.add_argument("-l",
        dest="need_likes",
        action="store_true",
        required=False,
        default=False,
        help=""
    )
    arg_parser.add_argument("-i",
        dest="indent",
        type=int,
        required=False,
        default=2,
        help=""
    )
    args = arg_parser.parse_args()
    main(args)
