import os

import pandas as pd

from config import Tool


class BugCounter:
    def __init__(self, path, bug_line, bug_type):
        self.path = path
        self.bug_line = bug_line
        self.bug_type = bug_type
        self.voter = []


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
            for bug_counter in bug_counters:
                if bug_counter.path == row['path'] and bug_counter.bug_line == row["line"] and bug_counter.bug_type == row["bug_type"]:
                    bug_counter.voter.append(Tool("slither"))
                    break
        for index, row in myr_df.iterrows():
            for bug_counter in bug_counters:
                if bug_counter.path == row['path'] and bug_counter.bug_line == row["line"] and bug_counter.bug_type == row["bug_type"]:
                    bug_counter.voter.append(Tool("mythril"))
                    break
        for index, row in cfr_df.iterrows():
            for bug_counter in bug_counters:
                if bug_counter.path == row['path'] and bug_counter.bug_line == row["line"] and bug_counter.bug_type == row["bug_type"]:
                    bug_counter.voter.append(Tool("confuzzius"))
                    break
        for bug_counter in bug_counters:
            if len(bug_counter.voter) <= 1:
                bug_counters.remove(bug_counter)
        res_df = pd.DataFrame([bug_counter.__dict__ for bug_counter in bug_counters])
        res_df.to_csv(os.path.join(self.res_dir, 'res.csv'), index=False)
