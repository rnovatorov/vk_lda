#! venv/bin/python


import json
from argparse import ArgumentParser
from tqdm import tqdm
# Project
from src.TextProcessor import TextProcessor
from src.utils import json_dump


def main(args):
    text_proc = TextProcessor()

    if args.stopwords_path:
        custom_stopwords = load_custom_stopwords(args.stopwords_path)
        text_proc.extend_stopwords(custom_stopwords)

    posts = load_posts(args.posts_path)
    docs = parse_posts(posts)

    print("Normalizing...")
    prepared_docs = []
    for doc in tqdm(docs):
        prepared = text_proc.prepare_for_lda(doc, only_nouns=args.only_nouns)
        prepared_docs.append(prepared)

    print("Saving...")
    json_dump(prepared_docs, args.output_path, args.indent)
    print("Done")


def parse_posts(posts):
    """
    Parses posts
    """
    docs = []
    for p in posts:
        post_text = p["post"]["text"]
        comments = [c["text"] for c in p["comments"] if c["text"]]
        comments_text = "\n".join(comments)
        if not post_text and not comments_text:
            continue
        doc = "%s\n%s" % (post_text, comments_text)
        docs.append(doc)
    return docs


def load_posts(posts_path):
    with open(posts_path) as f:
        return json.load(f)


def load_custom_stopwords(stopwords_path, encoding="utf-8"):
    with open(stopwords_path) as f:
        return [w.decode(encoding).rstrip("\n\r")
                for w in f.readlines()]


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("posts_path",
        help="path to get posts from"
    )
    arg_parser.add_argument("-o",
        dest="output_path",
        required=True,
        help="path to save processed posts to"
    )
    arg_parser.add_argument("-s",
        dest="stopwords_path",
        required=False,
        help="extend stopwords with given in file"
    )
    arg_parser.add_argument("-n",
        dest="only_nouns",
        action="store_true",
        required=False,
        help="only nouns needed"
    )
    arg_parser.add_argument("-i",
        dest="indent",
        type=int,
        required=False,
        default=2,
        help="indent in json output file"
    )
    args = arg_parser.parse_args()
    main(args)
