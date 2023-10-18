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
gridA {gridA}
gridB {gridB}
gridC {gridC}
#gridA           20.21   0.0   0.0    # a-vector of unit cell; recomanded format (x,y,0)
#gridB           0.0   16.373  0.0    # b-vector of unit cell; recomanded format (x,y,0)
#gridC           0.0     0.0  25.0    # c-vector of unit cell; recomanded format (0,0,z)
scanMin         -2     -2      12.0    # start of scanning (x,y,z) (for tip, so PP is lower) heighest atom 12.0 + 2.7 + r0Probe[z]   
scanMax        {scanMax}    # end   of scanning (x,y,z) (+4Ang)
Amplitude       {Amp}                                             # [Å] oscilation amplitude for conversion Fz->df
# gridN  300 240 672
"""

prepare = """cp -r ../ProbeParticleModel-complix_tip PPM-complex_tip
cp -r ../ProbeParticleModel-OpenCL/ PPM-OpenCL
cp ../v2xsf .
chmod +x v2xsf
./v2xsf ../data/{filename}.CHGCAR -d -o total_density.xsf
./v2xsf ../data/{filename}.LOCPOT -d -o v_hartree.xsf
ln -s ../data/{filename}.POSCAR poscar_k5.fin

python -c "from ase.io import read, write; atoms = read('poscar_k5.fin', format='vasp'); atoms = atoms[atoms.positions[:, 2] > {z_top_layer}]; write('input_plot.xyz', atoms)"
"""

run_PPM = """set -e

if [[ -e atomtypes.ini- ]];
then mv atomtypes.ini- atomtypes.ini
fi
if [[ -e params.ini.bak ]];
then mv params.ini.bak params.ini
fi
if [[ -e FFelTip_x.xsf ]];
then rm FFelTip_x.xsf FFelTip_y.xsf FFelTip_z.xsf
fi
python PPM-OpenCL/extract_desities.py -i "total_density.xsf" --plot
echo 1 > run.out
python PPM-OpenCL/fitPauli.py -i total_density.xsf -z {fitPauli_z} --old --plot
echo 2 >> run.out

#python2 PPM-complex_tip/generateElFF.py -i "v_hartree.cube" --prolongez 18 10
python PPM-complex_tip/generateElFF.py -i "v_hartree.xsf"
echo 3 >> run.out

cp params.ini params.ini.bak

echo "# grid" >> params.ini
cat FFel_z.xsf| head -n 8 | tail -n 1 | awk '{{print "gridN  " ($1 - 1) " " ($2 - 1) " " ($3 - 1)}}' >> params.ini

python PPM-complex_tip/generateLJFF.py -i new_xyz.xyz
echo 4 >> run.out

python PPM-complex_tip/relaxed_scan.py
echo 5 >> run.out
# python PPM-complex_tip/plot_results.py --df
echo 6 >> run.out
# python PPM-complex_tip/plot_results.py --df --atoms
echo 7 >> run.out
python PPM-complex_tip/plot_results.py --save_df
echo 8 >> run.out
# python -c "from ase.io.xsf import read_xsf; import numpy as np; data, _ = read_xsf('Qo-0.12Qc0.21K0.09/Amp3.80/df.xsf', read_data=True); data = np.copy(data, order='c'); np.save('Qo-0.12Qc0.21K0.09/Amp3.80/data.npy', data)"
echo 9 >> run.out

mv params.ini.bak params.ini
mv atomtypes.ini atomtypes.ini-
"""


def main(atoms_list, **kwargs):
    import numpy as np

    # z height for top layer for input_plot.xyz
    z_top_layer = kwargs.get("z_top_layer")
    # z height for Pauli fitting in OpenCL branch
    fitPauli_z = kwargs.get("z_top_layer")
    # xy buffer for scanning
    scan_xy_buffer = kwargs.get("scan_xy_buffer")

    # grid data
    cell = atoms_list[0].cell.array
    gridA = " ".join(map(str, cell[0, :]))
    gridB = " ".join(map(str, cell[1, :]))
    gridC = " ".join(map(str, cell[2, :]))

    # scan data
    # Probe Particle recommends heighest atom + r0Probe[z] (2.7A) for scanMin
    # but we let the tip crash
    scanMin = np.array([
        -scan_xy_buffer,
        -scan_xy_buffer,
        atoms_list[0].positions[:, 2].max()
    ])
    scanMax = cell.sum(axis=1)
    scanMax[0] += scan_xy_buffer
    scanMax[1] += scan_xy_buffer
    with open('params.ini', 'w') as fio:
        fio.write(params_ini.format(
            **kwargs,
            gridA=gridA,
            gridB=gridB,
            gridC=gridC,
            scanMin=" ".join(map(str, scanMin)),
            scanMax=" ".join(map(str, scanMax)),
        ))

    key_value_pairs = atoms_list[0].info.get('key_value_pairs', {})
    key_value_pairs.update(kwargs)
    atoms_list[0].info['key_value_pairs'] = key_value_pairs
    
    filename = atoms_list[0].info['key_value_pairs']['label']
    with open('prepare.sh', 'w') as fio:
        fio.write(prepare.format(filename=filename, z_top_layer=z_top_layer))

    with open('run_PPM.sh', 'w') as fio:
        fio.write(run_PPM.format(fitPauli_z=fitPauli_z))
        
    return atoms_list