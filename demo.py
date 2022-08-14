import os

from utils.vote_utils import Voter

res_dir = "/home/yy/PycharmProjects/smart-ast-deeper/smart-dataset-vote/results/1660470986.719603"

voter = Voter(res_dir)
voter.put_voter_csv(csv_path="/home/yy/PycharmProjects/smart-ast-deeper/smart-dataset-vote/results/1660470986.719603/slither.csv", voter_name="slither")
voter.put_voter_csv(csv_path="/home/yy/PycharmProjects/smart-ast-deeper/smart-dataset-vote/results/1660470986.719603/confuzzius.csv", voter_name="confuzzius")
voter.put_voter_csv(csv_path="/home/yy/PycharmProjects/smart-ast-deeper/smart-dataset-vote/results/1660470986.719603/mythril.csv", voter_name="mythril")
voter.run()
