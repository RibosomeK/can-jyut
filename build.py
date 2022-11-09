import subprocess, sys, shutil


def main():
    version = sys.argv[-1]
    args = [
        "--workpath",
        "E:Documents/python-build/can-jyut/build",
        "--distpath",
        f"E:Documents/python-build/can-jyut/v{version}",
        "-n",
        f"can-jyut_v{version}",
        "--clean",
        "-F",
        "./src/main.py",
    ]
    subprocess.run(["pyinstaller", *args])
    dst = f"E:Documents/python-build/can-jyut/v{version}"
    shutil.copy("./config.json", dst)
    shutil.copy("./readme.md", dst)
    shutil.copytree("./custome_dicts", f"{dst}/custome_dicts", dirs_exist_ok=True)
    shutil.copytree("./locales", f"{dst}/locales", dirs_exist_ok=True)
    
    with open(f"{dst}/plugin.txt", mode="w", encoding="shift-jis") as fp:
        text = f"name=can-jyut_v{version}\nexecute=can-jyut_v{version}"
        fp.write(text)


if __name__ == "__main__":
    main()
