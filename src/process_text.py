import re
import pymorphy2
import nltk
from stop_words import get_stop_words
from pprint import pprint as pp


class TextProcessor(object):
    """
    A class for russian text processing i.e.:
    - Tokenizing
    - Normalizing
    - Removing punctuation
    - Counting and removing urls
    - And so on
    """
    def __init__(self):
        # MorphAnalyzer instance (should be created only once)
        self.morph = pymorphy2.MorphAnalyzer()
        # nltk RegexpTokenizer also removes punctuation
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")

        # Some common stopwords
        self.stop_words = get_stop_words("ru")

        # Used to remove [id123456789|username] in VK comments
        self.re_reply = re.compile(r"\[id\d+\|.+\]")
        # Used to remove <br> which is \n in VK posts
        self.re_br = re.compile(r"<br>")
        # I really suggest you not trying to understand how that works
        self.re_url = re.compile(
           r"(?:(?:https?|ftp)://)"
           r"(?:\S+(?::\S*)?@)?"
           r"(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
           r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
           r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|"
           r"(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)"
           r"(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*"
           r"(?:\.(?:[a-z\u00a1-\uffff]{2,})))"
           r"(?::\d{2,5})?(?:/[^\s]*)?")

    def extend_stopwords(self, custom_stopwords):
        """
        Call this with list of your stop_words in unicode
        if you want to extend get_stop_words("ru")
        """
        error_text = "custom_stopwords must be a list of unicode strings"
        for word in custom_stopwords:
            if isinstance(word, unicode):
                self.stop_words.append(word)
            elif isinstance(word, string):
                try:
                    self.stop_words.append(unicode(word))
                except UnicodeDecodeError:
                    raise UnicodeError(error_text)
            else:
                raise UnicodeError(error_text)
            

    def tokenize(self, doc):
        """
        Tokenizing doc
        Also removes punctuation
        """
        return self.tokenizer.tokenize(doc)

    def normalize_token(self, token):
        """
        Puts token into its normal_form
        """
        return self.morph.parse(token)[0].normal_form

    def normalize_doc(self, doc):
        """
        Saves the structure, but puts all words into their normal_form
        """
        doc = self.remove_brs(self.remove_urls(doc))
        tokens = self.tokenizer.tokenize(doc)
        normalized = [self.normalize_token(t) for t in tokens]
        return " ".join(normalized)

    def remove_urls(self, doc):
        """
        Returns doc cleaned of url links
        """
        return self.re_url.sub("", doc)

    def remove_brs(self, doc):
        """
        Removes <br>
        """
        return self.re_br.sub("", doc)

    def count_urls(self, doc):
        """
        Counts urls
        Returns a dict {url: amount in doc}
        """
        urls = self.re_url.findall(doc)
        return {u: urls.count(u) for u in set(urls)}

    def prepare_for_lda(self, doc, pos=None):
        """
        Preparing doc for lda
        by filtering from garbage of any kind
        """
        # Removing links
        doc = self.remove_urls(doc)
        # Removing <br>
        doc = self.remove_brs(doc)
        # Removing [id123456789|username]
        doc = self.re_reply.sub("", doc)

        # Tokenizing
        tokens = self.tokenize(doc)

        # Normalizing
        normalized = []
        for t in tokens:
            parsed = self.morph.parse(t)[0]
            if pos and parsed.tag.POS == pos or pos is None:
                normalized.append(parsed.normal_form)

        # Applying stopwords filtering
        filtered = [w for w in normalized if w not in self.stop_words]

        return filtered
