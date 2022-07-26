import os
import time

import loguru

from utils.based_utils import extract_sols
from utils.confuzzius_utils import ConFuzziusRunner
from utils.mythril_utils import MythrilRunner
from utils.slither_utils import SlitherRunner
from utils.vote_utils import Voter

THIS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATASET_DIR = os.path.join(THIS_FILE_DIR, "dataset")  # 如果你的源代码数据集不在这里，请自行更改
DATASET_DIR = "/home/yy/Dataset/smart-contract-sanctuary-ethereum/contracts/mainnet"
loguru.logger.remove()  # 移除标准输出log
loguru.logger.add("./logs/INFO.log", level="INFO", mode="w", format="{time} | {level} | {process} | {thread} | {message}")
loguru.logger.add("./logs/ERROR.log", level="ERROR", mode="w", format="{time} | {level} | {process} | {thread} | {message}")
loguru.logger.add("./logs/WARNING.log", level="WARNING", mode="w", format="{time} | {level} | {process} | {thread} | {message}")
loguru.logger.add("./logs/DEBUG.log", level="DEBUG", mode="w", format="{time} | {level} | {process} | {thread} | {message}")
loguru.logger.add("./logs/CRITICAL.log", level="CRITICAL", mode="w", format="{time} | {level} | {process} | {thread} | {message}")

if __name__ == '__main__':
    res_dir = os.path.join(THIS_FILE_DIR, "results", str(time.time()))  # 绝对路径
    os.makedirs(res_dir)
    sols_paths = extract_sols(DATASET_DIR, 100)
    slr = SlitherRunner(sols_paths, os.path.join(res_dir, "slither.csv"))
    cfr = ConFuzziusRunner(sols_paths, os.path.join(res_dir, "confuzzius.csv"))
    myr = MythrilRunner(sols_paths, os.path.join(res_dir, "mythril.csv"))
    voter = Voter(res_dir)
    voter.put_voter_csv(csv_path=os.path.join(res_dir, "slither.csv"), voter_name="slither")
    voter.put_voter_csv(csv_path=os.path.join(res_dir, "confuzzius.csv"), voter_name="confuzzius")
    voter.run()
    loguru.logger.info(f"Done: {len(sols_paths)}")
