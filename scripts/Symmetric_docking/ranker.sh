#!/bin/bash
#Script for calculating rmsd with ranker after symmetrical docking - Staf 2016

for i in *.pdb
    do
    grep " CA " $i > "$i"_CA.pdb
    done

sed -i -- 's/ A /   /g' *CA.pdb
sed -i -- 's/ B /   /g' *CA.pdb
sed -i -- 's/ C /   /g' *CA.pdb
sed -i -- 's/ D /   /g' *CA.pdb
sed -i -- 's/ E /   /g' *CA.pdb
sed -i -- 's/ F /   /g' *CA.pdb
sed -i -- 's/ G /   /g' *CA.pdb  #7 blades
sed -i -- 's/ H /   /g' *CA.pdb #8 blades
#sed -i -- 's/ I /   /g' *CA.pdb #9 blades


ls *CA.pdb > rankerlist

/opt/durandal_QCP_released/ranker rankerlist > rmsdlist

sed -i s/.pdb:/" "/g rmsdlist 