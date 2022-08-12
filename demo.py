import os

os.popen("/bin/bash -c source /home/yy/PycharmProjects/smart-ast-deeper/smart-dataset-vote/mythril/ENV/bin/activate;myth analyze --solv 0.4.25 --execution-timeout 120 /home/yy/PycharmProjects/smart-ast-deeper/smart-dataset-vote/dataset/E.sol:MY_BANK -o json").read()
