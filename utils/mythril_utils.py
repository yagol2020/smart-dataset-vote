import json
from multiprocessing import Pool
from subprocess import check_output
from typing import List

import loguru
from tqdm import tqdm
import pandas as pd

from config import BugInfo, CsvReport, BugType, Tool
from utils.based_utils import extract_contracts


class MythrilRunner:
    def __init__(self, paths, csv_path):
        self.bug_reports: List[BugInfo] = []
        self.paths = paths
        self.csv_path = csv_path
        self.run()
        self.report_to_csv()

    @loguru.logger.catch()
    def run(self):
        pool = Pool()
        for ret in tqdm(pool.imap_unordered(run_single, self.paths), total=len(self.paths), desc="Running Mythril"):
            self.bug_reports.extend(ret)

    def report_to_csv(self):
        res = [CsvReport(r).__dict__ for r in self.bug_reports]
        df = pd.DataFrame(res)
        df.to_csv(self.csv_path, index=False)


def run_single(path) -> List[BugInfo]:
    ret = []
    try:
        path_contracts = extract_contracts(path)
        for p, c in path_contracts:
            cmd = f"myth analyze --solv 0.4.25 --execution-timeout {1 * 2 * 60} {p}:{c} -o json"
            loguru.logger.debug(cmd)
            output = json.loads(check_output(cmd, shell=True).decode("UTF-8"))
            if output['success']:
                for issue in output['issues']:
                    ret.append(BugInfo(BugType(issue['title']), Tool("Mythril"), issue['lineno'], issue['description'], p, c))
            else:
                loguru.logger.error(f"Mythril failed(output) on {p}:{c}")
    except Exception as e:
        loguru.logger.error(f"Mythril failed on {path}")
    return ret
