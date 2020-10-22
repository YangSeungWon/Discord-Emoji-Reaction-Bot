import json
from collections import OrderedDict

sorted_db_kor = OrderedDict()

with open("emoji.json","rb") as f:
    db_eng = json.load(f)

with open("emoji-ko.json","rb") as f:
    db_kor = json.load(f)


def find_key(dictionary, value):
    for _key, _value in dictionary.items():
        if value == _value:
            return _key

for eng, emoji in sorted(db_eng.items(), key=lambda k:k[0]):
    print(emoji)
    sorted_db_kor[find_key(db_kor, emoji)] = emoji

with open("emoji-ko-sorted.json", "wb") as f:
    f.write(json.dumps([sorted_db_kor], ensure_ascii = False).encode('utf8'))