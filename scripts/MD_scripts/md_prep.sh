#!/bin/bash
#This script will do the preperations for a standard md run on gromacs
#It will look for a pdb file starting with md_ and create all the necessary files for the final run


#make new directory with name and additional directories for clarity

#pdb to gmx 
pdb2gmx -f md_*.pdb -o pdb2gmx.pdb -p topol.top -ff amber99sb -water tip3p -ignh

#editconf with -d 0.8
editconf -f pdb2gmx.pdb -o editconf.pdb -bt cubic -d 1.0

#genbox
genbox -cp editconf.pdb -cs spc216.gro -o genbox.pdb -p topol.top

#creation of conter ions
grompp -f ~/Scripts/MDP_files/MD_standard/genion.mdp -c genbox.pdb -p topol.top -o genion.tpr
genion -s genion.tpr -o genion.pdb -p topol.top -neutral -conc 0.00001 << EOF
13	
EOF

#energy minimalization
grompp -f ~/Scripts/MDP_files/MD_standard/em.mdp -c genion.pdb -p topol.top -o em.tpr 
mdrun -deffnm em -v

#Equilibration NVT MD
grompp -f ~/Scripts/MDP_files/MD_standard/NVT_eq.mdp -c em.gro -p topol.top -o NVT.tpr -t em.trr 
mdrun -deffnm NVT -v

#Equilibration NPT MD
grompp -f ~/Scripts/MDP_files/MD_standard/NPT_eq.mdp -c NVT.gro -p topol.top -o NPT.tpr -t NVT.trr
mdrun -deffnm NPT -v

