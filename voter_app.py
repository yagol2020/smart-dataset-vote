import os
import time

import loguru

from utils.based_utils import extract_sols
from utils.mythril_utils import MythrilRunner
from utils.slither_utils import SlitherRunner
from utils.vote_utils import Voter

THIS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = "./dataset"
loguru.logger.remove()  # 移除标准输出log
loguru.logger.add("./logs/INFO.log", level="INFO", mode="w")
loguru.logger.add("./logs/ERROR.log", level="ERROR", mode="w")
loguru.logger.add("./logs/WARNING.log", level="WARNING", mode="w")
loguru.logger.add("./logs/DEBUG.log", level="DEBUG", mode="w")

if __name__ == '__main__':
    csv_dir = os.path.join(THIS_FILE_DIR, "results", str(time.time()))  # 绝对路径
    os.makedirs(csv_dir)
    # sols_paths = extract_sols(DATASET_DIR, 5000)
    # slr = SlitherRunner(sols_paths, os.path.join(csv_dir, "slither.csv"))
    # myr = MythrilRunner(sols_paths, os.path.join(csv_dir, "mythril.csv"))
    # voter = Voter(os.path.join(csv_dir, "slither.csv"), os.path.join(csv_dir, "mythril.csv"))
    loguru.logger.info("Done")
