import os

import loguru
import pandas as pd
from slither import Slither

from config import Tool


class BugCounter:
    def __init__(self, path, bug_line, bug_type, contract, function):
        self.path = path
        self.bug_line = bug_line
        self.bug_type = bug_type
        self.contract = contract
        self.function = function
        self.voter = []

    def vote(self, voter):
        if isinstance(voter, Tool):
            self.voter.append(voter.name)
            self.voter = list(set(self.voter))  # 去重
        else:
            loguru.logger.warning("投票人不是Tool类型")


class Voter:
    def __init__(self, res_dir):
        self.res_dir = res_dir
        self.bug_counters = set()
        self.voter = {}

    def put_voter_csv(self, csv_path: str, voter_name: str):
        if not os.path.exists(csv_path):
            loguru.logger.error("输出的投票源的csv文件不存在")
        else:
            self.voter[voter_name] = csv_path
            loguru.logger.info(f"注册投票源{voter_name}成功")

    def run(self):
        for voter_name, csv_path in self.voter.items():
            df = pd.read_csv(csv_path)
            self.extract_bug_info_into_bug_counters(df, voter_name)
        for bug_counter in self.bug_counters.copy():
            if len(bug_counter.voter) <= (len(self.voter) / 2):
                self.bug_counters.remove(bug_counter)
        res_df = pd.DataFrame([bug_counter.__dict__ for bug_counter in self.bug_counters])
        res_df.to_csv(os.path.join(self.res_dir, 'res.csv'), index=False)

    def extract_bug_info_into_bug_counters(self, df, voter_name):
        for index, row in df.iterrows():
            is_contain = False
            for bug_counter in self.bug_counters:
                if bug_counter.path == row['path'] \
                        and bug_counter.bug_line == row["bug_line"] \
                        and bug_counter.bug_type == row["bug_type"] \
                        and bug_counter.contract == row["contract_name"] \
                        and bug_counter.function == row["function_name"]:
                    bug_counter.vote(Tool(voter_name))  # 投票
                    is_contain = True
                    break
            if not is_contain:
                bug_counter = BugCounter(row['path'], row["bug_line"], row["bug_type"], row["contract_name"], row["function_name"])
                bug_counter.vote(Tool(voter_name))
                self.bug_counters.add(bug_counter)
