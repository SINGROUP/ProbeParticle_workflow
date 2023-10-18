params_ini = """PBC              True  
nPBC             1         1         1
moleculeShift       0.0       0.0     0.0   
Catom            6
Oatom            8
ChargeCuUp       {ChargeCuUp} 
ChargeCuDown     {ChargeCuDown}
Ccharge          {Ccharge}    
Ocharge          {Ocharge} 
Cklat    {Cklat} #0.111    #1.11 0.50 0.111          # the bending spring constant of the harmonic spring potential of tip-C bond Now it is a bending spring constant. The units should be ev/rad^2, if I am not mistaking
Oklat    {Oklat} #0.109    #1.09 0.50 0.109          # t he bending spring constant of the harmonic spring potential of C-O bond  
CuUpshift   {CuUpshift}
useLJ            True 
rC0        0.0 0.0  {rC0}  #1.85
rO0        {rOx} {rOy}  {rO0}  #1.15  
#rC0        0.5  0.5  1.71  #1.85  
#rO0        0.3  0.3  1.06  #1.15
#Cklat   0.50 
#Oklat   0.50 
Ckrad   {Ckrad}
Okrad   {Okrad} 
tipZdisp   0.0 
tip  's' 
tipsigma  {sigma}
sigma     {sigma}
gridA 20.210000    0.000000    0.000000
gridB  0.000000   16.373000    0.000000
gridC  0.000000    0.000000   {gridz}
#gridA           20.21   0.0   0.0    # a-vector of unit cell; recomanded format (x,y,0)
#gridB           0.0   16.373  0.0    # b-vector of unit cell; recomanded format (x,y,0)
#gridC           0.0     0.0  25.0    # c-vector of unit cell; recomanded format (0,0,z)
scanMin         -2     -2      12.0    # start of scanning (x,y,z) (for tip, so PP is lower) heighest atom 12.0 + 2.7 + r0Probe[z]   
scanMax        22.0    18.0    {gridz}    # end   of scanning (x,y,z) (+4Ang)
Amplitude       {Amp}                                             # [Å] oscilation amplitude for conversion Fz->df
# gridN  300 240 672
"""

prepare = """cp -r ../../run_folder/ProbeParticleModel-complix_tip PPM-complex_tip
cp -r ../../run_folder/ProbeParticleModel-OpenCL/ PPM-OpenCL
cp ../v2xsf .
chmod +x v2xsf
./v2xsf ../data/{filename}.CHGCAR -d -o total_density.xsf
./v2xsf ../data/{filename}.LOCPOT -d -o v_hartree.xsf
ln -s ../data/{filename}.POSCAR poscar_k5.fin

python -c "from ase.io import read, write; atoms = read('poscar_k5.fin', format='vasp'); atoms = atoms[atoms.positions[:, 2] > 8.5]; write('input_plot.xyz', atoms)"
"""



def main(atoms_list, **kwargs):
    
    with open('params.ini', 'w') as fio:
        fio.write(params_ini.format(**kwargs))

    key_value_pairs = atoms_list[0].info.get('key_value_pairs', {})
    key_value_pairs.update(kwargs)
    atoms_list[0].info['key_value_pairs'] = key_value_pairs
    
    filename = atoms_list[0].info['key_value_pairs']['label']
    with open('prepare.sh', 'w') as fio:
        fio.write(prepare.format(filename=filename))
        
    return atoms_list