import re, subprocess, json, threading, string
from dataclasses import dataclass, field
from typing import Any, Optional

# import pycantonese
# import opencc
from fenci.segment import Segment
from .ust import Property, Section, Ust
from .translate import tr


ENLONGING = ("R", "-", "+")

PUNCTUATION = (
    "",
    " ",
    "，",
    "。",
    "、",
    "：",
    "；",
    "？",
    "！",
    "”",
    "“",
    "（",
    "）",
    "～",
    "「",
    "」",
    "…",
)

YALE = {"oe": "eu", "eo": "eu", "jyu": "yu", "j": "y", "z": "j", "c": "ch"}
CHURCH = {"eo": "oe", "z": "dz", "c": "ts", "yu": "y"}
SCHEME = {"yale": YALE, "church": CHURCH}

LAZY = {"oi": "ngoi", "au": "ngau", "ok": "ngok"}


@dataclass
class T2P:
    seg: Segment = field(default_factory=Segment)
    user_dict: dict[str, str] = field(default_factory=dict)


def text2jyut(
    text: str, is_lazy=False, is_fast=True, t2p: Optional[T2P] = None
) -> list[str]:

    if not t2p:
        raise SyntaxError("you need t2p in fast mode")
    segment, user_dict = t2p.seg, t2p.user_dict
    no_tone_jyutping = text2jyut_with_fenci(text, segment, user_dict)
    # else:
    #     # simplified to HongKong traditional
    #     converter = opencc.OpenCC("s2hk.json")
    #     text = converter.convert(text)
    #     no_tone_jyutping = text2jyut_with_pycantonese(text)

    if is_lazy:
        for idx, jyutping in enumerate(no_tone_jyutping):
            if jyutping in LAZY:
                no_tone_jyutping[idx] = LAZY[jyutping]

    return no_tone_jyutping


# def text2jyut_with_pycantonese(text: str) -> list[str]:
#     no_tone_jyutping = []
#     for word, jyutping in pycantonese.characters_to_jyutping(text):
#         if word.encode("utf-8").isalpha():
#             no_tone_jyutping.append(word)  # keep possible English word
#             continue
#         if word.isdigit():
#             no_tone_jyutping.append(word)  # keep posiible number
#             continue
#         if jyutping is None:
#             continue
#         no_tone_jyutping.extend(re.split(r"[0-9]", jyutping)[:-1])
#     return no_tone_jyutping


def text2jyut_with_fenci(
    text: str, segment: Segment, user_dict: dict[str, str]
) -> list[str]:
    no_tone_jyutping = []

    for word in segment.cut(text):
        if word in PUNCTUATION or word in string.punctuation:
            continue

        def is_han(word: str) -> bool:
            b = word.encode("utf-8")
            if b.isdigit():
                return False
            if b.isalpha():
                return False
            if b.isalnum():
                return False
            return True

        if is_han(word):
            try:
                no_tone_jyutping.extend(
                    [jyut for jyut in re.split(r"[0-9]", user_dict[word]) if jyut]
                )
            except KeyError:
                # unknown compound word
                for char in word:
                    no_tone_jyutping.append(user_dict.get(char, char + "0")[:-1])
        # separate same weird alpha digit combination
        elif word.encode("utf-8").isalnum():
            alpha = re.compile(r"([a-zA-Z]+)")
            no_tone_jyutping.extend([char for char in re.split(alpha, word) if char])
            continue
        else:
            # keep posiible English or digit maybe?
            no_tone_jyutping.append(word)

    return no_tone_jyutping


def call_autoCVVC(args: str, plugin_dir: Optional[str] = None):
    if plugin_dir is None:
        plugin_dir = r"../autoCVVC2.002/autoCVVC.exe"
    while True:
        try:
            result = subprocess.run([plugin_dir, args])
            break
        except FileNotFoundError:
            plugin_dir = input(
                tr("plz input the dir of autoCVVC or press enter to quit:\n")
            )
            if not plugin_dir:
                return
    try:
        result.check_returncode()
        print(tr("auto cvvc success"))
    except subprocess.CalledProcessError as e:
        print(e)


def fill_lyrics(lyrics: list[str], ust: Ust, is_skip=False) -> None:
    skipped = 0
    for idx, note in enumerate(ust.notes):
        if note.get(Property.LYRIC) in ENLONGING and is_skip:
            skipped += 1
            continue
        try:
            note.add_property(Property.LYRIC, lyrics[idx - skipped])
        except IndexError:
            break


def to_other_scheme(lyrics: list[str], scheme: str) -> list[str]:
    if scheme == "jyutping":
        return lyrics

    for idx, lyric in enumerate(lyrics):
        for old, new in SCHEME[scheme].items():
            lyric = lyric.replace(old, new)
            lyrics[idx] = lyric

    return lyrics


def input_mode(
    dir: str,
    text: str,
    t2p: Optional[T2P] = None,
    is_lazy: bool = False,
    scheme: str = "jyutping",
    is_skip: bool = False,
    is_fast: bool = True,
    output_dir: Optional[str] = None,
):
    ust = Ust.init_from(dir)
    lyrics = to_other_scheme(text2jyut(text, is_lazy, is_fast, t2p), scheme)
    fill_lyrics(lyrics, ust, is_skip)
    if output_dir is None:
        output_dir = dir
    ust.export(output_dir)


def convert(
    ust: Ust,
    is_fast: bool = True,
    t2p: Optional[T2P] = None,
    is_lazy: bool = False,
    scheme: str = "jyutping",
    encoding="gb2312",
):

    idx_text_pair = {}
    for idx, note in enumerate(ust.notes):
        lyric = note.get(Property.LYRIC, "R")
        if lyric not in ENLONGING and not lyric.encode(encoding).isalpha():
            idx_text_pair[idx] = lyric
    text = "".join(idx_text_pair.values())
    lyrics = to_other_scheme(text2jyut(text, is_lazy, is_fast, t2p), scheme)

    idx_lyric_pair = dict(zip(idx_text_pair, lyrics))

    for idx, lyric in idx_lyric_pair.items():
        ust.notes[idx][Property.LYRIC] = lyric

    return ust


def convert_mode(
    dir: str,
    is_fast: bool = True,
    t2p: Optional[T2P] = None,
    is_lazy: bool = False,
    scheme: str = "jyutping",
    encoding: str = "gb2312",
) -> None:

    ust = Ust.init_from(dir, encoding)
    convert(ust, is_fast, t2p, is_lazy, scheme, encoding)
    ust.export(dir, encoding)


def export_mode(
    dir: str,
    is_fast: bool = True,
    t2p: Optional[T2P] = None,
    is_lazy: bool = False,
    scheme: str = "jyutping",
    encoding: str = "utf-8",
    is_inutau: bool = False,
    output_dir: Optional[str] = None,
) -> str:

    ust = Ust.init_from(dir, encoding)
    if is_inutau:
        encoding = "utf-8"
        dir = ust.settings[Section.SETTING][Property.PROJECT]
        ust = Ust.init_from(dir, encoding)

    convert(ust, is_fast, t2p, is_lazy, scheme, encoding)
    if output_dir is None:
        output_dir = f"{'.'.join(dir.split('.')[:-1])}-c.ust"
    ust.export(output_dir, encoding)

    return output_dir


def read_config(config: str = "./config.json") -> dict[str, Any]:
    with open(config, mode="r", encoding="utf-8") as fp:
        data = json.load(fp)
        if not isinstance(data, dict):
            return {}
        else:
            for key in data:
                if not isinstance(key, str):
                    raise TypeError
        return data


def load_dict(t2p: T2P, dict_dir: str):
    seg = Segment()
    with open(dict_dir, "r", encoding="utf-8") as fp:
        user_dict = json.load(fp)

    for word in user_dict:
        seg.add_word(word)

    t2p.seg, t2p.user_dict = seg, user_dict


def init_fenci(dict_type: str, t2p: T2P, need_finished: bool = False) -> None:
    dict_dir = f"./custome_dicts/{dict_type}.json"
    thread = threading.Thread(target=load_dict, args=[t2p, dict_dir])
    thread.start()
    while need_finished and thread.is_alive():
        continue


def set_default_dict(dict_type: str) -> str:
    with open("./config.json", "r") as fp:
        config = json.load(fp)
        if dict_type not in config["dict_type"]:
            return f"{dict_type} {tr('does not exist in dict_type')}"
        config["default_dict"] = dict_type

    with open("./config.json", "w") as fp:
        json.dump(config, fp, ensure_ascii=False)
        return ""
