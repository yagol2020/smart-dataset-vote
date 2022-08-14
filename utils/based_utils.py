import hashlib
import os
import random
import shutil
from multiprocessing import Pool
from typing import List, Tuple

import loguru
from crytic_compile import CryticCompile
from slither import Slither
from tqdm import tqdm


def extract_sols(source_path, sample):
    error_sol_path = os.path.join(source_path, "error_sol")
    if not os.path.exists(error_sol_path):
        os.mkdir(error_sol_path)
    pool = Pool()
    sols = []
    paths = []
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(".sol") and "error_sol" not in root:  # 只处理.sol文件，并且不在error_sol文件夹中
                paths.append(os.path.join(root, file))
    random.shuffle(paths)
    if sample:
        if sample > len(paths):
            sample = len(paths)
        paths = random.sample(paths, sample)
    # md5 remove duplicate
    md5_set = set()
    paths_distinct = []
    for path in tqdm(paths, desc="remove duplicate"):
        md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
        if md5 in md5_set:
            loguru.logger.debug("remove duplicate: {}".format(path))
            continue
        md5_set.add(md5)
        paths_distinct.append(path)

    for path in tqdm(pool.imap_unordered(compile_sol, paths_distinct), total=len(paths_distinct), desc="Compiling sols"):
        if path[0]:
            sols.append(path[1])
        else:
            try:
                shutil.move(path[1], error_sol_path)  # 移动到error_sol文件夹中
                loguru.logger.warning(f"{path[1]} is not compiled, moved to {error_sol_path}")
            except Exception as e:
                loguru.logger.error(f"{path[1]} is not compiled, when move into error_dir, error happen: {e}")
    pool.close()
    pool.join()
    return sols


def compile_sol(sol_path):
    try:
        Slither(sol_path)
        open(sol_path, 'r').read()
    except Exception as e:
        exception_info_str = str(e).split("\n")[0]
        loguru.logger.error(f"{sol_path} is not compiled: {exception_info_str}")
        return False, sol_path
    return True, sol_path


def extract_contracts(sol_path: str) -> List[Tuple[str, str, Slither]]:
    ret = []
    sl = Slither(sol_path)
    cy = sl.crytic_compile
    for i in cy.compilation_units[sol_path].contracts_names_without_libraries:
        ret.append((sol_path, i, sl))
    return ret
