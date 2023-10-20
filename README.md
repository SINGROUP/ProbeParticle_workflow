ProbeParticle workflow for water and CO adsorption on Calcite
=============================================================

Reusable workflow to generate ProbeParticle images, as used in::

[Heggemann, Jonas, Yashasvi S. Ranawat, Ondřej Krejčí, Adam S. Foster, and Philipp Rahe. "Differences in Molecular Adsorption Emanating from the (2× 1) Reconstruction of Calcite (104)." The Journal of Physical Chemistry Letters 14, no. 7 (2023): 1983-1989.](https://pubs.acs.org/doi/full/10.1021/acs.jpclett.2c03243)

[Heggemann, Jonas, Simon Aeschlimann, Tobias Dickbreder, Yashasvi S. Ranawat, Ralf Bechstein, Angelika Kühnle, Adam S. Foster, and Philipp Rahe. "Water adsorption lifts the (2× 1) reconstruction of calcite (104)." Physical Chemistry Chemical Physics (2023).](https://pubs.rsc.org/en/content/articlehtml/2023/cp/d3cp01408h)

Install
-------

Clone the required git repositories::

```bash
git clone --recurse-submodules https://github.com/SINGROUP/ProbeParticle_workflow.git
```

Install python dependencies, using [pipenv](https://pipenv.pypa.io/en/latest/)::

```bash
pipenv sync
```

Enter the virtual environment using::

```bash
pipenv shell
```

Usage
-----

The workflow requires POSCAR, LOCPOT and CHGCAR files from VASP simulation of the system. These files should be added to the `data` folder with the same prefix, as shown by "example" files.
The `workflow.ipynb` has the cells to add the workflow to an [ASE database](https://wiki.fysik.dtu.dk/ase/ase/db/db.html). 

> **_NOTE:_**  Add a vacuum of atleast 20Å over the system for better visualisation.

[Runner](https://runner.readthedocs.io) is used to run the workflow.
There are two ways to run the workflow once added to the database::
 * with a slurm workflow manager
 * with terminal.

Use the correct runner definition from the `workflow.ipynb` for your environment. Once added to the workflow, runner can be started by::

```bash
# for slurm runner
python run.py

# for terminal runner
python run_terminal.py
```

After the run finishes, the database is updated with the relevant data. This data can be retrieved by running the "data retrieval" cell in `workflow.ipynb`. This adds the relevant cells in the `Images` folder.

The `Images.ipynb` (in the `Images` folder) can be used to visualise the images generated from the ProbeParticle workflow.

Citation
--------

The workflow::

```
@article{heggemann2023differences,
  title={Differences in Molecular Adsorption Emanating from the (2$\times$ 1) Reconstruction of Calcite (104)},
  author={Heggemann, Jonas and Ranawat, Yashasvi S and Krejčí, Ondřej and Foster, Adam S and Rahe, Philipp},
  journal={The Journal of Physical Chemistry Letters},
  volume={14},
  number={7},
  pages={1983--1989},
  year={2023},
  publisher={ACS Publications}
}
```

ProbeParticle model::

```
@article{hapala2014mechanism,
  title={Mechanism of high-resolution STM/AFM imaging with functionalized tips},
  author={Hapala, Prokop and Kichin, Georgy and Wagner, Christian and Tautz, F Stefan and Temirov, Ruslan and Jel{\'\i}nek, Pavel},
  journal={Physical Review B},
  volume={90},
  number={8},
  pages={085421},
  year={2014},
  publisher={APS}
}
```
```
@article{hapala2014origin,
  title={Origin of high-resolution IETS-STM images of organic molecules with functionalized tips},
  author={Hapala, Prokop and Temirov, Ruslan and Tautz, F Stefan and Jel{\'\i}nek, Pavel},
  journal={Physical review letters},
  volume={113},
  number={22},
  pages={226101},
  year={2014},
  publisher={APS}
}
```

