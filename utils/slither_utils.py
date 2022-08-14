import inspect
import json
import os
from multiprocessing import Pool
from typing import List

import loguru
from slither import Slither
from slither.detectors import all_detectors
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from tqdm import tqdm

from config import BugInfo, Tool, BugType, CsvReport
import pandas as pd


class SlitherRunner:
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
            for ret in tqdm(pool.imap_unordered(run_single, self.paths), total=len(self.paths), desc="Running slither"):
                self.bug_reports.extend(ret)
            pool.close()
            pool.join()
        except Exception as e:
            loguru.logger.critical(f"执行Slither多进程任务失败，请检查错误信息: {e}")

    def report_to_csv(self):
        res = [CsvReport(r).__dict__ for r in self.bug_reports]
        df = pd.DataFrame(res)
        df.to_csv(self.csv_path, index=False)


def run_single(path) -> List[BugInfo]:
    ret = []
    try:
        if os.path.exists(f"/tmp/slither_res_{os.getpid()}.json"):
            os.remove(f"/tmp/slither_res_{os.getpid()}.json")
        os.popen(f"slither {path} --json /tmp/slither_res_{os.getpid()}.json").read()
        if not os.path.exists("/tmp/slither_res.json"):
            loguru.logger.error("/tmp/slither_res.json文件不存在，请检查slither是否正常运行")
        else:
            res = json.load(open(f"/tmp/slither_res_{os.getpid()}.json"))
            if res['success']:
                for l in res['results']['detectors']:
                    for e in l['elements']:
                        if e['type'] == 'node':
                            bug_info = BugInfo(BugType(l['check']), l['check'], Tool("slither"), e['source_mapping']['lines'], l['description'], path)
                            if e['type_specific_fields']['parent']['type'] == "function":
                                bug_info.function_name = e['type_specific_fields']['parent']['name']
                                if e['type_specific_fields']['parent']['type_specific_fields']['parent']['type'] == "contract":
                                    bug_info.contract_name = e['type_specific_fields']['parent']['type_specific_fields']['parent']['name']
                            ret.append(bug_info)
            else:
                loguru.logger.error("slither执行失败，请检查错误信息")
    except Exception as e:
        loguru.logger.error(f"Error running slither on {path}, {e}")
    return ret
