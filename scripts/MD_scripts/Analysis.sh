#!/bin/bash 

#This script does some basic analysis of a md: 
#   -convert the trajectory to fix boundary jumps
#   -rmsd of backbone
#   -rmsf of Ca
#   -PCA

#convert trajectory
trjconv -f md*.xtc -o md_pbc.xtc -s md*.tpr -pbc mol << EOF
1          
1
EOF

#RMSD
g_rms -s md*.tpr -f md_pbc.xtc -o rmsd_bb.xvg << EOF
4          
4         
EOF

#RMSF
g_rmsf -s md*.tpr -f md_pbc.xtc -o rmsf.xvg -fit << EOF
3          
EOF

PCA
need pdb with only ca called Ca_*
eliminate rotations and translations only keep Ca

trjconv -f md_pbc.xtc -o md_Ca.xtc -s md.tpr -fit rot+trans << EOF
3
3
EOF

g_covar -f md_Ca.xtc -s Ca_* << EOF
3
3
EOF

g_anaeig -v eigenvec.trr -f md_Ca.xtc -s Ca_* -2d 2dproj_1_2.xvg -first 1 -last 2 << EOF
3
3
EOF

prepare for gnuplot palette
sed '/^#/ d' rmsd_bb.xvg > hulp
sed '/^@/ d' hulp > rmsd_bb.xvg

sed '/^#/ d' 2dproj_1_2.xvg > hulp
sed '/^@/ d' hulp > 2dproj_1_2.xvg

awk '{$2="";print}' rmsd_bb.xvg > time.xvg
paste 2dproj_1_2.xvg time.xvg | column -s $'\t' -t > 2d_PCA.xvg 
rm hulp

