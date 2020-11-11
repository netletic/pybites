import os
import urllib.request
import re
from collections import Counter

# data provided
tmp = os.getenv("TMP", "/tmp")
stopwords_file = os.path.join(tmp, "stopwords")
harry_text = os.path.join(tmp, "harry")
urllib.request.urlretrieve(
    "https://bites-data.s3.us-east-2.amazonaws.com/stopwords.txt", stopwords_file
)
urllib.request.urlretrieve(
    "https://bites-data.s3.us-east-2.amazonaws.com/harry.txt", harry_text
)


def get_harry_most_common_word():
    with open(stopwords_file) as fp:
        stopwords = {stopword.strip() for stopword in fp.readlines()}
    with open(harry_text) as fp:
        all_words = re.findall(r"[a-zA-Z0-9']+", fp.read())
        filtered_words = [
            word.lower().strip() for word in all_words if word.lower() not in stopwords
        ]

    return Counter(filtered_words).most_common(1)[0]


if __name__ == "__main__":
    print(get_harry_most_common_word())