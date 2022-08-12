# 基于投票的智能合约安全漏洞数据集生成器

### 投票源

* Slither
* Mythril
* ConFuzzius

### USAGE

安装Slither

```shell
cd slither
python setup.py install

```

安装Mythril

```shell
cd mythril
virtualenv ENV # mythril的环境与ConFuzzius冲突，所以需要创建一个新的环境
source ENV/bin/activate
python setup.py install
pip install solc-select==0.2.0
solc-select install 0.4.25
solc-select use 0.4.25
```

安装ConFuzzius

```shell
cd ConFuzzius/fuzzer
pip install -r requirements.txt

```

修改`ConFuzzius/fuzzer/utils/settings.py`文件中的`LOGGING_LEVEL = logging.ERROR`，避免日志输出过多