from argparse import ArgumentParser
import json
import progressbar as pb
# Project
import config as conf
from src.utils import prepare_doc
from src.VKPostsGetter import VKPostsGetter


def main(args):
    vkpg = VKPostsGetter(vk_access_token=conf.VK_ACCESS_TOKEN,
                         wait_time=conf.WAIT_TIME)
    owner_posts = vkpg.get_posts(args.group_id, vk_filter="owner")
    others_posts = vkpg.get_posts(args.group_id, vk_filter="others")
    group_posts = owner_posts + others_posts

    # group_id = -108394847

    if args.need_comments:
        bar = pb.ProgressBar(
            maxval=len(group_posts),
            widgets=[
                "Getting comments: ",
                pb.Bar(left="[", marker="=", right="] "),
                pb.SimpleProgress(),
            ]
        ).start()

    with open(args.output_path, "w") as f:
        f.write("[\n")  # In order not to hold all comments in memory
        for n, post in enumerate(group_posts):
            if args.need_comments:
                bar.update(n + 1)
                comments = vkpg.get_comments(post, need_likes=args.need_likes)
            else:
                comments = []
            doc = prepare_doc(post, comments, formatting=args.formatting)
            json.dump(doc, f, indent=args.indent)
            f.write(",\n")
        f.write("]")
    if args.need_comments:
        bar.finish()
    print("Done.\n")


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("group_id",
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
        default=4,
        help=""
    )
    args = arg_parser.parse_args()
    main(args)
