作者：RibosomeK
版本：0.2b


# 更新日志

## 0.2b
1. 移除了第三方模组 pycantonese，```-p``` 参数不可用。
2. 修正了其他粤语方案转换失败的 bug
3. 依照个人习惯修改了粤语字典中的部分发音。

## 0.1b
1. 添加了简体中文和繁体中文（香港）的翻译，由程序自动检测，暂不支持手动设置。
2. 移除了第三方模组 pyutau

## 0.5a
1. 支持自定义字典，可以通过参数 ```--set-default-dict``` 和``` --set-user-dict``` 
   分别改变默认和当前的字典。**使用自定义字典时不可以使用 ```-p``` 和 ```-l``` 参数**
2. 添加了普通话字典，默认仍为粤语拼音

## 0.4a
1. 行为改变，之前的 convert 模式现在分为 convert 和 export，
分别对应直接修改源文件和保留源文件导出修改后的文件副本。
两个模式现在皆可在 UTAU 中调用时和单独使用作为参数。
convert 模式在 UTAU 中表现为转换选中的字符，单独使用时转换整个工程。
export 模式无论在 UTAU 中还是单独使用时，都会导出整个转换后的工程副本。
工程路径中可以包含中文，但是**不能包含空格**
2. 修正了上一版本更换 Python 版本时忘记改字典的路径的 bug

## 0.3a
1. 正式支持转换模式，测试工程为在 Synthesizer V 中填好词导出的 ust 工程。
支持延音符号 [-], [+]，不会调用 autoCVVC 进行拆音，请自行调用。
可以双击插件文件夹中的 can-jyut.bat 输入 ```-c ./要/转换的/UTAU工程的/文件路径.ust``` 
或者直接打开要转换的工程文件，选中任意音符调用插件，输入 -c 
转换成功的工程文件默认保存为源目录下后缀为 ```-c.ust``` 的工程。
2. 更换了 Python 版本为 3.11.0

## 0.2a
1. 修正了 python 运行环境错误
2. 增加了调用 autoCVVC 插件的功能（默认调用）
3. 增加了新的工作方式，速度更快（默认调用）

## 0.1a
初版本


# 描述：
用来输入汉字并转换为粤语拼音方案的 UTAU 插件，界面为命令行
输入的文字中，标点符号会被忽略，数字和英文会被保留
如果包含英文的话最好不要调用 autoCVVC 避免出现拆音错误


# 用法：
> [-h] [-s] [-p] [-ska] [-sch SCHEME] [-l]
  [--set-default-dict SET_DEFAULT_DICT]
  [--set-user-dict SET_USER_DICT]
  [-c] [-e] [-q] [TEXT ...]

```
位置参数:
  TEXT（即输入的汉字，或者单独使用的 ust 文件路径）

选项:
  -h, --help            列出帮助信息
  -s, --skip            跳过空行或者延音符号 -, +
  -p, --precise         使用 pycantonese 模组进行分词和取得拼音，准确但是速度慢。目前不可用
  -ska, --skip-auto-cvvc
                        不使用 autoCVVC 进行拆音
  -sch SCHEME, --scheme SCHEME
                        使用其他粤语拼音方案，默认为粤拼，可选项为耶鲁式（yale）和教堂式（church）
  -l, --lazy            部分发音使用懒音，如将 oi, ok, au 变为 ngoi, ngok, ngau
  --set-default-dict SET_DEFAULT_DICT
                        设置默认字典
  --set-user-dict SET_USER_DICT
                        设置当前的字典，不会改变默认字典
  -c, --convert         转换原有音符的汉字为拼音
  -e, --export          转换并导出修改后文件的副本
  -q, --quit            退出程序
```


# 使用例：
1. 直接输入汉字
  ```
    >>> 广东话
    结果：gwong dung waa
  ```

2. 跳过空行或者延音符号
  ```
    >>> -s 广东话  
    结果：gwong - dung waa（如果延音符号在“广”和“东”之间）
  ```

3. 使用其他粤语拼音方案
  ```
  >>> -sch yale 春天
  结果：ceun tin（耶鲁式，粤拼为 ceon tin）

  >>> -sch church 春天
  结果：cheon tin（教堂式，粤拼为 ceon tin）
  ```

4. 使用懒音
  ```
    >>> -l 牛肉
    结果：ngou juk（非懒音为 ou juk）
  ```

5. 转换模式
  ```
    >>> -c ./要/转换的/UTAU工程的/文件路径.ust
    或 在 UTAU 中选中相应音符：
    >>> -c
  ```

6. 导出模式
  ```
    >>> -e ./要/转换/并导出的/UTAU工程的/文件路径.ust
    或 在 UTAU 中选中任意音符：
    >>> -e
  ```

7. 使用自定义字典
    自定义字典应为 json 格式，一个完整的字典格式要求为
  ```json
  {
       "汉字词": "该汉字词的拼音",
       "声调跟在拼音后面": "拼音之间不用空格分隔",
       "除了汉字词外": "所有的标点符号都为半角",
       "编写时注意最外层的大括号": "以及发音后的逗号",
       "但是最后一条发音后面": "不要有逗号",

       "自定义": "zi4ding4yi4",
       "字典": "zi4dian3"
   }
  ```
自定义字典应当存放在存放插件目录下的 ```./custome_dicts``` 中，而且应该添加在插件目录下的 ```config.json``` 中。

如自定义字典的文件名为 ```hakka.json```，则应在 ```dict_type``` 中添加 ```hakka```，两相对应，如：

```json
  {
      {
          "dict_type": ["cantonese", "mandarin", "hakka"],
          "default_dict": "cantonese"
      }
  }
```

添加并设置好自定义字典后，可以如下使用：

  ```
  >>> --set-default-dict mandarin
  改变默认字典为 mandarin

  >>> --set-user-dict mandarin
  改变当前字典为 mandarin
  ```

8. 混合使用
  ```
    >>> -sch yale -s -l 我好想食牛肉
    结果：ngo hau seung sik ngou juk
  ```


# 引用和致谢
1. [pyutau](https://github.com/UtaUtaUtau/pyUtau) MIT License
2. [pycantonese](https://github.com/jacksonllee/pycantonese) MIT License
3. [opencc](https://github.com/BYVoid/OpenCC) Apache License
3. [fenci](https://github.com/a358003542/fenci) MIT license
4. [autoCVVC](https://delta-kimigatame.hatenablog.jp/entry/ar591802)
4. [Rime 粤语拼音方案](https://github.com/rime/rime-cantonese) CC BY 4.0
4. [CC-CEDICT](https://cc-cedict.org/wiki/start) CC BY-SA 3.0

