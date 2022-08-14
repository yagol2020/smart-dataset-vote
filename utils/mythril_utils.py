import json
import os
from multiprocessing import Pool
from subprocess import check_output
from typing import List

import loguru
from tqdm import tqdm
import pandas as pd

from config import BugInfo, CsvReport, BugType, Tool, MYTHRIL_ENV_PYTHON_BIN, MYTHRIL_MYTH_PY_PATH
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
        try:
            pool = Pool()
            for ret in tqdm(pool.imap_unordered(run_single, self.paths), total=len(self.paths), desc="Running Mythril"):
                self.bug_reports.extend(ret)
            pool.close()
            pool.join()
        except Exception as e:
            loguru.logger.critical(f"执行Mythril多进程任务失败，请检查错误信息: {e}")

    def report_to_csv(self):
        res = [CsvReport(r).__dict__ for r in self.bug_reports]
        df = pd.DataFrame(res)
        df.to_csv(self.csv_path, index=False)


def run_single(path) -> List[BugInfo]:
    ret = []
    try:
        path_contracts = extract_contracts(path)
        for p, c, sl in path_contracts:
            cmd = f"{MYTHRIL_ENV_PYTHON_BIN} {MYTHRIL_MYTH_PY_PATH} analyze --solv 0.4.25 --execution-timeout {1 * 5 * 60} {p}:{c} -o json"
            loguru.logger.debug(cmd)
            output = json.loads(os.popen(cmd).read())
            if output['success']:
                for issue in output['issues']:
                    bug_info = BugInfo(BugType(issue['title']), issue['title'], Tool("Mythril"), issue['lineno'], issue['description'], p, contract_name=c, sl=sl)
                    ret.append(bug_info)
            else:
                loguru.logger.error(f"Mythril failed(output) on {p}:{c}")
    except Exception as e:
        loguru.logger.error(f"Mythril failed on {path}, {e}")
    return ret
