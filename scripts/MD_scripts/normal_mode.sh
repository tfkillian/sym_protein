#!/bin/bash
#This script will do the preperations for a normal mode md run on gromacs
#It will look for a pdb file starting with nm_ and do the normal mode 

#pdb to gmx 
pdb2gmx_d -f nm_*.pdb -o pdb2gmx.pdb -p topol.top -ff amber99sb -water tip3p -ignh -renum

#editconf with -d 0.8
editconf_d -f pdb2gmx.pdb -o editconf.pdb -bt cubic -d 1.4

#energy minimalization with steep
grompp_d -f ~/Scripts/MDP_files/NM_standard/steep.mdp -c editconf.pdb -p topol.top -o steep.tpr 
mdrun_d -deffnm steep -v

#energy minimization with cg
grompp_d -f ~/Scripts/MDP_files/NM_standard/cg.mdp -c steep.gro -p topol.top -o cg.tpr -t steep.trr 
mdrun_d -deffnm cg -v

#energy minimization with bfgs
grompp_d -f ~/Scripts/MDP_files/NM_standard/bfgs2.mdp -c cg.gro -p topol.top -o bfgs.tpr -t cg.trr
mdrun_d -deffnm bfgs -v


#normal mode run
grompp_d -f ~/Scripts/MDP_files/NM_standard/nm.mdp -c bfgs.gro -p topol.top -o nm.tpr -t bfgs.trr
mdrun_d -deffnm nm -v 

#calculate eigenvalues from hessian
g_nmeig_d -f nm.mtx -s nm.tpr 

mkdir steep
mv steep.* steep
mdkir cg
mv cg.* cg
mkdir bfgs
mv bfgs.* bfgs
mkdir nm
mv nm.* nm
mkdir results 
mv eigenval.xvg eigenvec.trr eigenfreq.xvg results
S