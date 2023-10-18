cp -r ../../run_folder/ProbeParticleModel-complix_tip PPM-complex_tip
cp -r ../../run_folder/ProbeParticleModel-OpenCL/ PPM-OpenCL
ln -s ../total_density.cube .
ln -s ../v_hartree.cube .
ln -s ../poscar_k5.fin .

python -c "from ase.io import read, write; atoms = read('poscar_k5.fin', format='vasp'); atoms = atoms[atoms.positions[:, 2] > 8.5]; write('input_plot.xyz', atoms)"
