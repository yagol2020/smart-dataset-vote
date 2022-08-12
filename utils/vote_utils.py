import pandas as pd


class Voter:
    def __init__(self, slr_csv, myr_csv):
        self.slr_csv = slr_csv
        self.myr_csv = myr_csv
        self.run()

    def run(self):
        slr_df = pd.read_csv(self.slr_csv)
        myr_df = pd.read_csv(self.myr_csv)
        slr_set = set()
        for index, row in slr_df.iterrows():
            slr_set.add((row['path'], row['bug_line'], row['bug_type']))
        myr_set = set()
        for index, row in myr_df.iterrows():
            myr_set.add((row['path'], row['bug_line'], row['bug_type']))
        res_set = slr_set & myr_set
        res_df = pd.DataFrame(list(res_set), columns=['path', 'line', 'bug_type'])
        res_df.to_csv('res.csv', index=False)
