set -e

if [[ -e atomtypes.ini- ]];
then mv atomtypes.ini- atomtypes.ini
fi
if [[ -e params.ini.bak ]];
then mv params.ini.bak params.ini
fi
if [[ -e FFelTip_x.xsf ]];
then rm FFelTip_x.xsf FFelTip_y.xsf FFelTip_z.xsf
fi
python PPM-OpenCL/extract_desities.py -i "total_density.xsf"
echo 1 > run.out
python PPM-OpenCL/fitPauli.py -i total_density.xsf -z 9 --old
echo 2 >> run.out

#python2 PPM-complex_tip/generateElFF.py -i "v_hartree.cube" --prolongez 18 10
python PPM-complex_tip/generateElFF.py -i "v_hartree.xsf"
echo 3 >> run.out

cp params.ini params.ini.bak

echo "# grid" >> params.ini
cat FFel_z.xsf| head -n 8 | tail -n 1 | awk '{print "gridN  " ($1 - 1) " " ($2 - 1) " " ($3 - 1)}' >> params.ini

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
