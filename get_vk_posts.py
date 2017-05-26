from argparse import ArgumentParser
import json
import progressbar as pb
# Project
import config as conf
from src.utils import compose_doc, merge_iterators
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

    bar = pb.ProgressBar(
        maxval=groups_posts_volume,
        widgets=[
            "Downloading: ",
            pb.Bar(left="[", marker="=", right="] "),
            pb.SimpleProgress(),
        ]
    ).start()

    docs = []
    for n, post in enumerate(group_posts):
        if args.need_comments:
            comments = vkpg.get_comments(post, need_likes=args.need_likes)
        else:
            comments = []
        bar.update(n)
        doc = compose_doc(post, comments, formatting=args.formatting)
        if doc:
            docs.append(doc)
    bar.finish()
    
    print("Saving...")
    with open(args.output_path, "w") as f:
        json.dump(docs, f, indent=args.indent)


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
        dest="formatting",
        required=False,
        choices=["short", "full"],
        default="short",
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
        default=False)
    arg_parser.add_argument("-i",
        dest="indent",
        type=int,
        required=False,
        default=2,
        help=""
    )
    args = arg_parser.parse_args()
    main(args)
