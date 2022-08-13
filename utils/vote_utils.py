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
        else:
            loguru.logger.warning("投票人不是Tool类型")


class Voter:
    def __init__(self, slr_csv, myr_csv, cfr_csv, res_dir):
        self.slr_csv = slr_csv
        self.myr_csv = myr_csv
        self.cfr_csv = cfr_csv
        self.res_dir = res_dir
        self.run()

    def run(self):
        slr_df = pd.read_csv(self.slr_csv)
        myr_df = pd.read_csv(self.myr_csv)
        cfr_df = pd.read_csv(self.cfr_csv)
        bug_counters = set()
        for index, row in slr_df.iterrows():
            is_contain = False
            for bug_counter in bug_counters:
                if bug_counter.path == row['path'] and bug_counter.bug_line == row["bug_line"] and bug_counter.bug_type == row["bug_type"] and bug_counter.contract == row["contract_name"] and bug_counter.function == row["function_name"]:
                    bug_counter.vote(Tool("slither"))
                    is_contain = True
                    break
            if not is_contain:
                bug_counter = BugCounter(row['path'], row["bug_line"], row["bug_type"], row["contract_name"], row["function_name"])
                bug_counter.vote(Tool("slither"))
                bug_counters.add(bug_counter)
        for index, row in myr_df.iterrows():
            is_contain = False
            for bug_counter in bug_counters:
                if bug_counter.path == row['path'] and bug_counter.bug_line == row["bug_line"] and bug_counter.bug_type == row["bug_type"] and bug_counter.contract == row["contract_name"] and bug_counter.function == row["function_name"]:
                    bug_counter.vote(Tool("mythril"))
                    is_contain = True
                    break
            if not is_contain:
                bug_counter = BugCounter(row['path'], row["bug_line"], row["bug_type"], row["contract_name"], row["function_name"])
                bug_counter.vote(Tool("mythril"))
                bug_counters.add(bug_counter)
        for index, row in cfr_df.iterrows():
            is_contain = False
            for bug_counter in bug_counters:
                if bug_counter.path == row['path'] and bug_counter.bug_line == row["bug_line"] and bug_counter.bug_type == row["bug_type"] and bug_counter.contract == row["contract_name"] and bug_counter.function == row["function_name"]:
                    bug_counter.vote(Tool("confuzzius"))
                    is_contain = True
                    break
            if not is_contain:
                bug_counter = BugCounter(row['path'], row["bug_line"], row["bug_type"], row["contract_name"], row["function_name"])
                bug_counter.vote(Tool("confuzzius"))
                bug_counters.add(bug_counter)
        for bug_counter in bug_counters.copy():
            if len(bug_counter.voter) <= 1:
                bug_counters.remove(bug_counter)
        res_df = pd.DataFrame([bug_counter.__dict__ for bug_counter in bug_counters])
        res_df.to_csv(os.path.join(self.res_dir, 'res.csv'), index=False)
