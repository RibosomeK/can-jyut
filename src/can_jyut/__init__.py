from can_jyut import can_jyut, cli, translate

tr = translate.tr

T2P = can_jyut.T2P

init_parser = cli.init_parser
init_fenci = can_jyut.init_fenci

text2jyut = can_jyut.text2jyut
text2jyut_with_fenci = can_jyut.text2jyut_with_fenci
# text2jyut_with_pycantonese = can_jyut.text2jyut_with_pycantonese

to_other_scheme = can_jyut.to_other_scheme

read_config = can_jyut.read_config
load_dict = can_jyut.load_dict
set_default_dict = can_jyut.set_default_dict

input_mode = can_jyut.input_mode
convert_mode = can_jyut.convert_mode
export_mode = can_jyut.export_mode
call_autoCVVC = can_jyut.call_autoCVVC
