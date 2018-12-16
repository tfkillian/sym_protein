#!/bin/sh
for i in *.pdb; do
	relax.linuxgccrelease -database /opt/rosetta_2017.45.59812/main/database/ -in:file:s $i -in:file:fullatom -relax:thorough -overwrite -nstruct 100 -out:file:scorefile "${i%.*}".sc
        awk '{print $20}' "${i%.*}".sc > 1
        awk '{print $2}' "${i%.*}".sc > 2
        sed -i 1,2d 2
        sed -i 1,2d 1
        paste -d, 1 2 >> score.csv
        rm 1 2 
done