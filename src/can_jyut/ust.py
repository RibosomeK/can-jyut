from dataclasses import dataclass, field
from enum import StrEnum
import re
from typing import Any, Optional


class Section(StrEnum):
    VERSION = "[#VERSION]"
    SETTING = "[#SETTING]"
    PREVNOTE = "[#PREV]"
    NOTE = "[#NOTE]"
    NEXTNOTE = "[#NEXT]"
    TRACKEDN = "[#TRACKEND]"


class Property(StrEnum):
    PROJECT = "Project"
    TEMPO = "Tempo"
    TRACKS = "Tracks"
    PROJECT_NAME = "ProjectName"
    OUT_FILE = "OutFile"
    CACHE_DIR = "CacheDir"
    TOOL1 = "Tool1"
    TOOL2 = "Tool2"

    LENGTH = "Length"
    LYRIC = "Lyric"
    NOTE_NUM = "NoteNum"
    PRE_UTTERANCE = "PreUtterance"


NOTES = (Section.PREVNOTE, Section.NOTE, Section.NEXTNOTE)


class Note(dict[str, Any]):
    def __init__(self):
        self[Property.LENGTH] = "480"
        self[Property.LYRIC] = "R"
        self[Property.NOTE_NUM] = "60"

    def add_property(self, name: str, value: Any) -> None:
        self[name] = value

    def __str__(self) -> str:
        return "\n".join(f"{key}={value}" for key, value in self.items())


class Notes(list[Note]):
    def __str__(self) -> str:
        return "\n".join(f"[#{idx:04}]\n{note}" for idx, note in enumerate(self))


@dataclass
class Ust:
    settings: dict[str, Any] = field(default_factory=dict)
    prev_note: Optional[Note] = None
    notes: Notes = field(default_factory=Notes)
    next_note: Optional[Note] = None

    @classmethod
    def init_from(cls, ust_dir: str, encoding: str = "shift-jis") -> "Ust":
        ust = Ust()
        ust.settings[Section.VERSION] = set()
        ust.settings[Section.SETTING] = {}

        with open(ust_dir, mode="r", encoding=encoding) as fp:
            name = ""
            for section in re.split(r"(\[#.+\])\n", fp.read()):

                if section in (
                    Section.VERSION,
                    Section.SETTING,
                    Section.PREVNOTE,
                    Section.NEXTNOTE,
                ):
                    name = section
                    continue

                if section == Section.TRACKEDN:
                    ust.settings[section] = {}
                    name = Section.TRACKEDN
                    continue

                if re.match(r"\[#[0-9]+\]", section):
                    name = Section.NOTE
                    continue

                if name == Section.VERSION:
                    ust.settings[Section.VERSION].update(
                        [e for e in section.split("\n") if e]
                    )

                elif name == Section.SETTING:
                    ust.settings[Section.SETTING].update(
                        {
                            item.split("=")[0]: item.split("=")[1]
                            for item in section.split("\n")
                            if item
                        }
                    )

                elif name in NOTES:
                    note = Note()
                    for item in section.split("\n"):
                        if item:
                            key, value = item.split("=")
                            note.add_property(key, value)

                    if name == Section.NOTE:
                        ust.notes.append(note)
                    elif name == Section.PREVNOTE:
                        ust.prev_note = note
                    elif name == Section.NEXTNOTE:
                        ust.next_note = note

        return ust

    def export(self, file_dir: str, encoding="shift-jis"):
        with open(file_dir, mode="w", encoding=encoding) as fp:
            fp.write(str(self))

    def __str__(self) -> str:
        version = f"{Section.VERSION}\n{chr(10).join(self.settings[Section.VERSION])}"
        setting = "\n".join(
            [f"{key}={value}" for key, value in self.settings[Section.SETTING].items()]
        )
        prev_note = f"[#PREVNOTE]{self.prev_note}\n" if self.prev_note else ""
        next_note = f"[#NEXTNOTE]{self.next_note}" if self.next_note else ""
        notes = f"{prev_note}{self.notes}{next_note}"
        trackend = Section.TRACKEDN if Section.TRACKEDN in self.settings else ""
        return f"{version}\n{Section.SETTING}\n{setting}\n{notes}\n{trackend}\n"
