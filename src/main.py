import sys, argparse, re

from can_jyut import (
    init_fenci,
    init_parser,
    T2P,
    read_config,
    tr,
    input_mode,
    export_mode,
    convert_mode,
    call_autoCVVC,
    set_default_dict,
)


def main():
    argv = sys.argv
    parser = init_parser()

    t2p = T2P()
    config = read_config()
    init_fenci(config["default_dict"], t2p)

    user_argv = input(
        tr(
            "Welcome to Can-Jyut, a Kanji to Jyutping UTAU plugin with a command line interface.\n"
            "For more options or help, you can enter -h\n"
            "Or you can just input the kanji\n>>> "
        )
    )

    while True:
        try:
            if not user_argv:
                user_argv = input(">>> ")
                continue

            args = parser.parse_args(re.split(r"\s", user_argv))
            is_fast = not args.precise

            if args.help:
                parser.print_help()
                user_argv = input(">>> ")
                continue
            if args.quit:
                parser.exit()

            try:
                if args.set_default_dict:
                    init_fenci(args.set_default_dict, t2p)
                    warning = set_default_dict(args.set_default_dict)
                    if warning:
                        print(warning)
                    print(tr("set default dict success!"))
                    if not args.text:
                        user_argv = ""
                        continue
                if args.set_user_dict:
                    init_fenci(args.set_user_dict, t2p, True)
            except FileNotFoundError as e:
                e.add_note(
                    tr("Please check if the corresponding json dict exist or not.")
                )
                print(e)
                break

            if not (args.convert or args.export) and args.text:
                input_mode(
                    argv[-1],
                    " ".join(args.text),
                    t2p,
                    args.lazy,
                    args.scheme,
                    args.skip,
                    is_fast,
                )
                print(tr("convert success"))
                if not args.skip_auto_cvvc:
                    call_autoCVVC(argv[-1])
                break
            elif args.export:
                if args.text:
                    converted = export_mode(
                        args.text[-1], is_fast, t2p, args.lazy, args.scheme
                    )
                else:
                    converted = export_mode(
                        argv[-1],
                        is_fast,
                        t2p,
                        args.lazy,
                        args.scheme,
                        "gb2312",
                        True,
                    )
                print(tr("convert success!\nconverted file exported at "), converted)
                break
            elif args.convert:
                if args.text:
                    convert_mode(
                        args.text[-1],
                        is_fast,
                        t2p,
                        args.lazy,
                        args.scheme,
                        "utf-8",
                    )
                else:
                    convert_mode(
                        argv[-1],
                        is_fast,
                        t2p,
                        args.lazy,
                        args.scheme,
                        "gb2312",
                    )
                print(tr("convert success!"))
                break
            user_argv = input(">>> ")
        except argparse.ArgumentError as e:
            print(e)
            user_argv = input(">>> ")


if __name__ == "__main__":
    main()
