#! venv/bin/python


import json
from argparse import ArgumentParser
# Project
from src.LDA import LDA
from src.utils import Loading, json_dump


def main(args):
    prepared_docs = load_preprared_docs(args.pdocs_path)

    with Loading(msg="Making LDA"):
        lda = LDA(prepared_docs,
                  num_topics=args.num_topics,
                  passes=args.passes)

    lda.print_topics()

    # Saving result
    if args.output_path is not None:
        print("Saving...")
        topics = lda.get_topics()
        json_dump(topics, args.output_path, args.indent)


def load_preprared_docs(pdocs_path):
    with open(pdocs_path) as f:
        return json.load(f)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("pdocs_path",
        help="path to get processed docs from"
    )
    parser.add_argument("-t",
        dest="num_topics",
        type=int,
        required=True,
        help="number of topics",
    )
    parser.add_argument("-p",
        dest="passes",
        type=int,
        required=False,
        default=30,
        help="number of passes through text",
    )
    parser.add_argument("-o",
        dest="output_path",
        required=False,
        help="path to save result to"
    )
    parser.add_argument("-i",
        dest="indent",
        required=False,
        default=2,
        help="indent in json output file"
    )
    args = parser.parse_args()
    main(args)
