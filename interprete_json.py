import json
from argparse import ArgumentParser


def main(args):
    lda = load_file(args.input_path)
    ljust_len = find_longest_word(lda)
    converted = convert_to_txt(lda, ljust_len)
    save_contents(converted, args.output_path)


def load_file(input_path):
    with open(input_path) as f:
        return json.load(f)


def convert_to_txt(lda, ljust_len, indent=4):
    result = ""
    for n, topic in enumerate(lda):
        result += "Topic %d:\n" % (n + 1)
        for word, prob in topic:
            result += "%s%s - %f\n" % (" " * indent, word.ljust(ljust_len), prob)
        result += "\n"
    return result


def find_longest_word(lda):
    longest = 0
    for topic in lda:
        for w, _ in topic:
            if len(w) > longest:
                longest = len(w)
    return longest


def save_contents(contents, output_path, encoding="utf-8"):
    with open(output_path, "w") as f:
        f.write(contents.encode(encoding))


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("input_path")
    arg_parser.add_argument("-o", dest="output_path", required=True)
    args = arg_parser.parse_args()
    main(args)
