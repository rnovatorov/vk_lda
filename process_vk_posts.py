#! venv/bin/python


import json
from argparse import ArgumentParser
from tqdm import tqdm
# Project
from src.TextProcessor import TextProcessor


def main(args):
    tproc = TextProcessor()

    posts = load_posts(args.input_path)
    docs = parse_posts(posts)

    print("Normalizing...")
    prepared_docs = []
    for doc in tqdm(docs):
        prepared = tproc.prepare_for_lda(doc, only_nouns=args.only_nouns)
        prepared_docs.append(prepared)

    print("Saving...")
    save_docs(prepared_docs, args.output_path, args.indent)
    print("Done")


def parse_posts(posts):
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


def load_posts(input_path):
    with open(input_path) as f:
        return json.load(f)


def save_docs(docs, output_path, indent=2):
    with open(output_path, "w") as f:
        json.dump(docs, f, indent=indent)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("input_path",
        help=""
    )
    arg_parser.add_argument("output_path",
        help=""
    )
    arg_parser.add_argument("-n",
        dest="only_nouns",
        action="store_true",
        required=False,
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
