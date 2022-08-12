import os
import random
import shutil
from multiprocessing import Pool
from typing import List, Tuple

import loguru
from crytic_compile import CryticCompile
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
            if file.endswith(".sol") and "error_sol" not in root:
                paths.append(os.path.join(root, file))
    random.shuffle(paths)
    if sample:
        if sample > len(paths):
            sample = len(paths)
        paths = random.sample(paths, sample)
    for path in tqdm(pool.imap_unordered(compile_sol, paths), total=len(paths), desc="Compiling sols"):
        if path[0]:
            sols.append(path[1])
        else:
            shutil.move(path[1], error_sol_path)
            loguru.logger.warning(f"{path[1]} is not compiled, moved to {error_sol_path}")
    pool.close()
    pool.join()
    return sols


def compile_sol(sol_path):
    try:
        CryticCompile(sol_path)
    except Exception as e:
        loguru.logger.error(f"{sol_path} is not compiled, {e}")
        return False, sol_path
    return True, sol_path


def extract_contracts(sol_path: str) -> List[Tuple[str, str]]:
    ret = []
    cy = CryticCompile(sol_path)
    for i in cy.compilation_units[sol_path].contracts_names_without_libraries:
        ret.append((sol_path, i))
    return ret
