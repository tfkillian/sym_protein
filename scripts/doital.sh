#!/bin/bash

for i in *.pdb
    do
    grep " CA " $i > tmp && mv tmp "$i"_CA.pdb
    done

sed -i -- 's/ A /   /g' *CA.pdb
sed -i -- 's/ B /   /g' *CA.pdb
sed -i -- 's/ C /   /g' *CA.pdb
sed -i -- 's/ D /   /g' *CA.pdb
sed -i -- 's/ E /   /g' *CA.pdb
sed -i -- 's/ F /   /g' *CA.pdb
sed -i -- 's/ G /   /g' *CA.pdb
sed -i -- 's/ H /   /g' *CA.pdb 
sed -i -- 's/ I /   /g' *CA.pdb

ls *CA.pdb > rankerlist

/opt/durandal_QCP_released/ranker rankerlist > rmsdlist

sed s/.pdb:/" "/g rmsdlist > tmp && mv tmp rmsdlist
