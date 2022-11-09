from can_jyut import init_parser
import re


def test_parser():
    parser = init_parser()
    def p(args: str) -> list[str]:
        return re.split(r"\s", args)
    
    c1 = "this is a test"
    args = parser.parse_args(p(c1))
    assert args.text == ["this", "is", "a", "test"]
    
    c2 = "-h -p -s -ska -sch yale -l 如果我是陈奕迅 这句话太吸引"
    args = parser.parse_args(p(c2))
    assert args.help == True
    assert args.precise == True
    assert args.skip == True
    assert args.skip_auto_cvvc == True
    assert args.scheme == "yale"
    assert args.lazy == True
    