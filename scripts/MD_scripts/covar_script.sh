#!/bin/bash
touch entropy.xvg

for ((i=5000;i<=100000;i+=5000)); do
g_covar -f md_pbc.xtc -s md.tpr -mwa -o eigen$i.xvg -e $i -dt 10 <<EOL
Protein
C-alpha
EOL

%calculate entropy with quasi harmonic approximation
bash quasih_short.sh eigen$i.xvg >> entropy.xvg
done

rm eigenvec.trr average.pdb covar.log \#*
