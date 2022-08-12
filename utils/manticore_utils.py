import json
from multiprocessing import Pool
from subprocess import check_output
from typing import List

import loguru
from tqdm import tqdm

from config import BugInfo, Tool, BugType, CsvReport
import pandas as pd

from utils.based_utils import extract_contracts


class ManticoreRunner:
    def __init__(self, paths, csv_path):
        self.bug_reports: List[BugInfo] = []
        self.paths = paths
        self.csv_path = csv_path
        self.run()
        self.report_to_csv()

    @loguru.logger.catch()
    def run(self):
        pool = Pool()
        for ret in tqdm(pool.imap_unordered(run_single, self.paths), total=len(self.paths), desc="Running Manticore"):
            self.bug_reports.extend(ret)

    def report_to_csv(self):
        res = [CsvReport(r).__dict__ for r in self.bug_reports]
        df = pd.DataFrame(res)
        df.to_csv(self.csv_path, index=False)


def run_single(path) -> List[BugInfo]:
    ret = []
    try:
        pass
    except Exception as e:
        loguru.logger.error(f"Manticore failed on {path}")
    return ret
