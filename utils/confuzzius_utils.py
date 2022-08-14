"""
ConFuzzius utils

@author: yagol
"""
import json
import os
from multiprocessing import Pool
from typing import List

import loguru
import pandas as pd
from tqdm import tqdm

from config import BugInfo, BugType, Tool, CONFUZZIUS_MAIN_PY_PATH, CsvReport
from utils.based_utils import extract_contracts


class ConFuzziusRunner:
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
            for ret in tqdm(pool.imap_unordered(run_single, self.paths), total=len(self.paths), desc="Running ConFuzzius"):
                self.bug_reports.extend(ret)
            pool.close()
            pool.join()
        except Exception as e:
            loguru.logger.critical(f"执行ConFuzzius多进程任务失败，请检查错误信息: {e}")

    def report_to_csv(self):
        res = [CsvReport(r).__dict__ for r in self.bug_reports]
        df = pd.DataFrame(res)
        df.to_csv(self.csv_path, index=False)


def run_single(path) -> List[BugInfo]:
    ret = []
    try:
        path_contracts = extract_contracts(path)
        for p, c, sl in path_contracts:
            if os.path.exists(f"/tmp/confuzzius_result_{os.getpid()}.json"):
                loguru.logger.debug(f"Remove /tmp/confuzzius_result_{os.getpid()}.json")
                os.remove(f"/tmp/confuzzius_result_{os.getpid()}.json")
            cmd = f"python {CONFUZZIUS_MAIN_PY_PATH} -s {p} -c {c} --solc v0.4.25 --evm byzantium -g 50 --result /tmp/confuzzius_result_{os.getpid()}.json"
            loguru.logger.debug(cmd)
            os.popen(cmd).read()
            if not os.path.exists(f"/tmp/confuzzius_result_{os.getpid()}.json"):
                loguru.logger.error(f"ConFuzzius: {p} {c} has no result")
                continue
            output = json.load(open(f"/tmp/confuzzius_result_{os.getpid()}.json"))
            if c in output.keys():
                errors = output[c]['errors']
                for swc_id, error in errors.items():
                    for e in error:
                        bug_info = BugInfo(BugType(e['type']), e['type'], Tool("ConFuzzius"), e['line'], e['type'], p, contract_name=c, sl=sl)
                        ret.append(bug_info)
            else:
                loguru.logger.error(f"ConFuzzius failed(output) on {p}:{c}")
    except Exception as e:
        loguru.logger.error(f"ConFuzzius failed on {path}, {e}")
    return ret
