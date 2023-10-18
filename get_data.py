from ase.io.xsf import read_xsf
import numpy as np
import os


class Cd:
    """Context manager for changing the current working directory
    :meta private:"""
    def __init__(self, new_path, mkdir=False):
        self.new_path = os.path.expanduser(new_path)
        self.saved_path = None

        if not os.path.exists(new_path) and mkdir:
            os.mkdir(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def main(atoms_list):
    for i in os.listdir():
        if i.startswith('Qo'):
            with Cd(i):
                for j in os.listdir():
                    if j.startswith('Amp'):
                        with Cd(j):
                            data, _ = read_xsf('df.xsf', read_data=True)
                        break
            break
    atoms = atoms_list[0]
    atoms.info['box'] = data
    
    return atoms
    