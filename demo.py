import os

from utils.vote_utils import Voter

res_dir = "/home/yy/PycharmProjects/smart-ast-deeper/smart-dataset-vote/results/1660352486.162336"

voter = Voter(os.path.join(res_dir, "slither.csv"), os.path.join(res_dir, "mythril.csv"), os.path.join(res_dir, "confuzzius.csv"), res_dir)
