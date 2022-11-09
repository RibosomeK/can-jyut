import argparse
from .translate import tr


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        tr("Welcom to Can-Jyut, a UTAU plugin convert kanji to jyutping with a cli."),
        add_help=False,
    )
    parser.add_argument("text", metavar="TEXT", type=str, nargs="*", default=None)
    parser.add_argument(
        "-h", "--help", help=tr("print out help info"), action="store_true"
    )
    parser.add_argument(
        "-p",
        "--precise",
        help=tr("use more accurate function, but much more slower"),
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--skip",
        help=tr("skip blank note, enlong symbol -, +"),
        action="store_true",
    )
    parser.add_argument(
        "-ska",
        "--skip-auto-cvvc",
        help=tr("do not call autoCVVC for further process"),
        action="store_true",
    )
    parser.add_argument(
        "-sch",
        "--scheme",
        help=tr(
            "use other romanaization scheme. "
            "default is jyutping, "
            "other avaliable value are yale and church"
        ),
        default="jyutping",
    )
    parser.add_argument(
        "-l",
        "--lazy",
        help=tr("add nasal consonant ng for oi, ok, au"),
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--convert",
        help=tr("convert a ust with kanji to romanaization scheme"),
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--export",
        help=tr("convert the whole ust file and export it"),
        action="store_true",
    )
    parser.add_argument(
        "--set-default-dict",
        help=tr("set default dictionary, see readme for more details"),
    )
    parser.add_argument(
        "--set-user-dict", help=tr("set current dictionary, do not change the defalut")
    )
    parser.add_argument(
        "-q", "--quit", help=tr("quit the program"), action="store_true"
    )
    return parser
