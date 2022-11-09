from can_jyut import init_fenci, text2jyut_with_fenci, T2P, to_other_scheme


DICT_TYPE = "cantonese"
t2p = T2P()
init_fenci(DICT_TYPE, t2p, True)


def test_fenci():

    texts = ["人行道银行", "人行道銀行", "人行-道銀行", "人行+道銀行", "人行道。銀行？", "（人行道）銀行", "人行道：銀行"]
    for text in texts:
        assert (text2jyut_with_fenci(text, t2p.seg, t2p.user_dict), text) == (
            [
                "jan",
                "hang",
                "dou",
                "ngan",
                "hong",
            ],
            text,
        )

    t1 = "广东话 with you"
    t2 = "广东话123"
    t3 = "广东话 123 "
    t4 = "广 东 话"
    t5 = "广东话123 with 456"
    t6 = "广东话with123"
    t7 = "with 123 广东话"
    t8 = "with123广东话"

    assert text2jyut_with_fenci(t1, t2p.seg, t2p.user_dict) == [
        "gwong",
        "dung",
        "waa",
        "with",
        "you",
    ]
    assert text2jyut_with_fenci(t2, t2p.seg, t2p.user_dict) == [
        "gwong",
        "dung",
        "waa",
        "123",
    ]
    assert text2jyut_with_fenci(t3, t2p.seg, t2p.user_dict) == [
        "gwong",
        "dung",
        "waa",
        "123",
    ]
    assert text2jyut_with_fenci(t4, t2p.seg, t2p.user_dict) == ["gwong", "dung", "waa"]
    assert text2jyut_with_fenci(t5, t2p.seg, t2p.user_dict) == [
        "gwong",
        "dung",
        "waa",
        "123",
        "with",
        "456",
    ]
    assert text2jyut_with_fenci(t6, t2p.seg, t2p.user_dict) == [
        "gwong",
        "dung",
        "waa",
        "with",
        "123",
    ]
    assert text2jyut_with_fenci(t7, t2p.seg, t2p.user_dict) == [
        "with",
        "123",
        "gwong",
        "dung",
        "waa",
    ]
    assert text2jyut_with_fenci(t8, t2p.seg, t2p.user_dict) == [
        "with",
        "123",
        "gwong",
        "dung",
        "waa",
    ]

    t9 = "噉沿途嗰啲countryside嘅景色都係唔錯𠸏"
    assert text2jyut_with_fenci(t9, t2p.seg, t2p.user_dict) == [
        "gam",
        "jyun",
        "tou",
        "go",
        "di",
        "countryside",
        "ge",
        "ging",
        "sik",
        "dou",
        "hai",
        "m",
        "co",
        "ge",
    ]


def test_to_other_scheme():
    to_yale = [
        "doe",
        "soeng",
        "doek",
        "ceoi",
        "ceon",
        "jyut",
        "jyun",
        "jyu",
        "ji",
        "jaa",
        "jing",
        "zi",
        "zaa",
        "zoeng",
        "zeon",
    ]
    to_church = [
        "ceoi",
        "ceon",
        "zi",
        "zaa",
        "zeon",
        "ci",
        "caa",
        "ceon",
        "jyu",
        "jyut",
        "jyun",
        "zyun",
        "cyut",
    ]

    yale = [
        "deu",
        "seung",
        "deuk",
        "cheui",
        "cheun",
        "yut",
        "yun",
        "yu",
        "yi",
        "yaa",
        "ying",
        "ji",
        "jaa",
        "jeung",
        "jeun",
    ]
    church = [
        "tsoei",
        "tsoen",
        "dzi",
        "dzaa",
        "dzoen",
        "tsi",
        "tsaa",
        "tsoen",
        "jy",
        "jyt",
        "jyn",
        "dzyn",
        "tsyt",
    ]

    assert to_other_scheme(to_yale, "yale") == yale
    assert to_other_scheme(to_church, "church") == church
