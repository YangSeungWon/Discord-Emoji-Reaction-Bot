from itertools import accumulate
from bisect import bisect
from random import randrange
from unicodedata import name as unicode_name
from dataclasses import dataclass
from json import dumps
from google.cloud import translate_v2 as translate

# 😁 Get full emoji test list from https://unicode.org/Public/emoji/[VERSION]/emoji-test.txt
#
# Discord supports Emoji 12.0, so I save it local.
# https://unicode.org/Public/emoji/12.0/emoji-test.txt

INPUT_FILENAME = "emoji"
OUTPUT_FILENAME = "emoji"


# Google Cloud Platform Translate API
# export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
# https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python

translate_client = translate.Client()


def valid_line(s: str) -> bool:
    if s == "" or s[0] == "#" or s[0] == "\n" or ": " in s or "fully-qualified" not in s:
        return False
    return True


def parse_line(s: str):
    s = s.split("# ")[1].split(" ", 1)
    return s[0], s[1]


def load_txt(filename=INPUT_FILENAME) -> list:
    s = ""
    with open(filename, mode='r', encoding='utf-8') as f:
        s = f.read()

    return s.split("\n")


def emoji_text(loader=load_txt, validator=valid_line) -> list:
    full_lines = loader()
    emoji_lines = [line for line in full_lines if validator(line)]

    return emoji_lines


def emoji_dict(emoji_lines: list, text_converter=None) -> dict:
    d = {}
    for line in emoji_lines:
        parsed = parse_line(line)
        key = parsed[1] if text_converter is None else text_converter(parsed[1])
        d[key] = parsed[0]
        print(key, parsed)

    return d


def dict_to_json(d: dict, filename=None):
    json_text = dumps(d, sort_keys=True, ensure_ascii=False)

    if filename is not None:
        text_to_file(json_text, filename)
    return json_text


def text_to_file(data: str, filename: str):
    with open(filename, mode='w') as f:
        f.write(data)


def eng_to_kor(s: str) -> str:
    try:
        return translate_client.translate(s, target_language="ko", model="base")["translatedText"]
    except Exception as e:
        print(e)
        return s


if __name__ == "__main__":
    print(dict_to_json(emoji_dict(emoji_text(), None), f"{OUTPUT_FILENAME}.txt"))
    print(dict_to_json(emoji_dict(emoji_text(), eng_to_kor), f"{OUTPUT_FILENAME}-ko.txt"))
