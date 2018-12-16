#!/bin/sh

#############################################################################################################
# cd-mil2mre.sh <FILE> <Molecular weight,Da> <Number of amino acid> <pathlength in millimeters> <conc. mg/ml>
#############################################################################################################

FILE1=$1
Da=$2
AA=$3
PL=$4
conc=$5

echo "Mw= $Da (Da)"
echo "Number of Amino Acid= $AA"
echo "Pathlength in millimeters= $PL"
echo "Conc.= $conc (mg/ml)"

###########
### Equ ###
###########
P=`echo "scale=4; ($Da / $AA) / ($PL * $conc)" | bc`

#echo $P
############
### FILE ###
############
sed -e 's/,/./g' $FILE1 > /tmp/tmp_$FILE1
sed -n '/^[0-9]/p' /tmp/tmp_$FILE1 > /tmp/tmp2_$FILE1
#cut -f1,2 /tmp/tmp2_$FILE1 > /tmp/tmp3_$FILE1

awk 'BEGIN{OFS="\t"}{print($1,$2*'$P')}' /tmp/tmp2_$FILE1 > MRE_$FILE1

rm -rf /tmp/tmp_$FILE1
rm -rf /tmp/tmp2_$FILE1
#rm -rf /tmp/tmp2_$FILE



