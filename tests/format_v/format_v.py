import re, logging
from dataclasses import dataclass
from typing import Iterator

@dataclass
class Sentence:
    text: tuple[str, ...]
    pos: tuple[str, ...]
    roman: tuple[str, ...]
    

def get_text(sentence: Sentence) -> str:
    return "".join(sentence.text)
    
def get_toneless_roman(sentence: Sentence) -> list[str]:
    """punctuation will also be removed"""
    romans = []
    for roman in sentence.roman:
        if re.match(r"VQ[0-9]", roman):
            continue
        else:
            romans.extend([roman for roman in re.split(r"[0-9]", roman) if roman])
    return romans
    
def iter_sentence(sentence: Sentence) -> Iterator[tuple[str, str, str]]:
    ...



def read(file: str) -> Iterator[Sentence]:
    with open(file, mode="r", encoding="utf-8") as fp:
        data = fp.read()
        
    matched: list[str] = re.findall(r"<sent_tag>([\s\S]*?)</sent_tag>", data)
    for match in matched:
        text, pos, roman = [], [], []
        for line in match.split("\n"):
            line = line.strip()
            if any(line):
                splitted = line.split("/")
                text.append(splitted[0])
                pos.append(splitted[1])
                roman.append(splitted[2])
        yield Sentence(tuple(text), tuple(pos), tuple(roman))
            
    else:
        logging.info("no dialog matched")
    
    
if __name__ == "__main__":
     for sentence in read(file="./hkcancor-utf8/utf8/FC-001_v2"):
         print(get_toneless_roman(sentence))
    