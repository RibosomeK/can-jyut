from can_jyut.can_jyut import input_mode, T2P, init_fenci, export_mode

DICT_TYPE = "cantonese"
t2p = T2P()
init_fenci(DICT_TYPE, t2p, True)

def compare_file(f1, f2, encoding):
    with open(f1, mode="r", encoding=encoding) as fp:
        data1 = fp.read()
        
    with open(f2, mode="r", encoding=encoding) as fp:
        data2 = fp.read()
        
    assert data1 == data2

def test_input():
    text = "广东话插件测试"
    input_mode("./tests/test_ust/original/input.ust", text, t2p, output_dir="./tests/test_ust/changed/input.ust")
    compare_file("./tests/test_ust/compare/input.ust", "./tests/test_ust/changed/input.ust", "shift-jis")
    
    input_mode("./tests/test_ust/original/input-skip.ust", text, t2p, is_skip=True, output_dir="./tests/test_ust/changed/input-skip.ust")
    compare_file("./tests/test_ust/compare/input-skip.ust", "./tests/test_ust/changed/input-skip.ust", "shift-jis")
    
    text2 = "广东话"
    input_mode("./tests/test_ust/original/input-skip2.ust", text2, t2p, is_skip=True, output_dir="./tests/test_ust/changed/input-skip2.ust")
    compare_file("./tests/test_ust/compare/input-skip2.ust", "./tests/test_ust/changed/input-skip2.ust", "shift-jis")
    

def test_export():
    export_mode("./tests/test_ust/original/convert.ust", t2p=t2p, output_dir="./tests/test_ust/changed/convert.ust")
    compare_file("./tests/test_ust/changed/convert.ust", "./tests/test_ust/compare/convert.ust", encoding="utf-8")
    
    export_mode("./tests/test_ust/original/convert-skip.ust", t2p=t2p, output_dir="./tests/test_ust/changed/convert-skip.ust")
    compare_file("./tests/test_ust/changed/convert-skip.ust", "./tests/test_ust/compare/convert-skip.ust", encoding="utf-8")
    