import sys, os

sys.path.append("")

from format_v.format_v import read, get_text, get_toneless_roman
from can_jyut import text2jyut_with_fenci, init_fenci, T2P


DICT_TYPE = "cantonese"
t2p = T2P()
init_fenci(DICT_TYPE, t2p, True)


def load():
    for root, ds, fs in os.walk("./hkcancor-utf8/utf8"):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


def main():
    for file in load():
        for sentence in read(file):
            text = get_text(sentence)
            roman = get_toneless_roman(sentence)
            if u"\uece1" in text or "行" in text or "嘞" in text or "哩" in text or "𠻺" in text:
                continue
            if (jyut := text2jyut_with_fenci(text, t2p.seg, t2p.user_dict)) != roman:
                print(f"{text}\n{jyut}\n{roman}\n")


if __name__ == "__main__":
    main()
