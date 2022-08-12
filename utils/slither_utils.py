import inspect
import os
from multiprocessing import Pool
from typing import List

import loguru
from slither import Slither
from slither.detectors import all_detectors
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from tqdm import tqdm

from voter.config import BugInfo, Tool, BugType, CsvReport
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
        pool = Pool()
        for ret in tqdm(pool.imap_unordered(run_single, self.paths), total=len(self.paths), desc="Running slither"):
            self.bug_reports.extend(ret)

    def report_to_csv(self):
        res = [CsvReport(r).__dict__ for r in self.bug_reports]
        df = pd.DataFrame(res)
        df.to_csv(self.csv_path, index=False)


def run_single(path) -> List[BugInfo]:
    ret = []
    try:
        sl = Slither(path)
        loguru.logger.debug(f"Running slither on {path}")
        detectors = [getattr(all_detectors, name) for name in dir(all_detectors)]
        detectors = [d for d in detectors if inspect.isclass(d) and issubclass(d, AbstractDetector)]
        for detector in detectors:
            if detector.IMPACT != DetectorClassification.INFORMATIONAL or detector.IMPACT != DetectorClassification.OPTIMIZATION:
                sl.register_detector(detector)
        res = sl.run_detectors()
        for r in res:
            if len(r) > 0:
                for l in r:
                    for e in l['elements']:
                        if e['type'] == 'node':
                            bug_info = BugInfo(BugType(l['check']), Tool("slither"), e['source_mapping']['lines'], l['description'], path)
                            if e['type_specific_fields']['parent']['type'] == "function":
                                bug_info.function_name = e['type_specific_fields']['parent']['name']
                                if e['type_specific_fields']['parent']['type_specific_fields']['parent']['type'] == "contract":
                                    bug_info.contract_name = e['type_specific_fields']['parent']['type_specific_fields']['parent']['name']
                            ret.append(bug_info)
    except Exception as e:
        loguru.logger.error(f"Error running slither on {path}, {e}")
    return ret
