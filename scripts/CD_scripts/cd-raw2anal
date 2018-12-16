#!/bin/sh

#############################################################################################################
# cd-raw2anal.sh <FILE> <Molecular weight,Da> <Number of amino acid> <pathlength in millimeters> <conc. mg/ml>
#############################################################################################################

FILE1=$1
Da=$2
AA=$3
PL=$4
conc=$5

echo "*****"
echo "Mw(Da) = $Da"
echo "Num. of A.A.= $AA"
echo "Path.(mm) = $PL"
echo "Conc.(mg/ml) = $conc"
echo "*****"

echo "[θ]in deg cm2 dmol-1 = (millidegree x mean residue weight(Mw/A.A))/(pathlength in millimeters x concentration in mg/ml)"
echo "[θ] = millidegrees / (pathlength in millimeters x the molar concentration of protien x the number or residue)"
echo "Δε = [θ]/3298"
echo "*****"
###########
### Equ ###
###########
M=`echo "scale=10; ($Da / $AA) / ($PL * $conc)" | bc`
T=`echo "scale=10; ($conc / $Da) * $PL * AA" | bc`
E=3298

#echo $M
#echo $T
#echo $E
############
### FILE ###
############
sed -e 's/,/./g' $FILE1 > /tmp/tmp_$FILE1
sed -n '/^[0-9]/p' /tmp/tmp_$FILE1 > /tmp/tmp2_$FILE1
cut -f1,2 /tmp/tmp2_$FILE1 > /tmp/tmp2_Mildg_$FILE1

mkdir ./Anal_$FILE1

## Millidegree
cat /tmp/tmp2_Mildg_$FILE1 > ./Anal_$FILE1/Mildg_$FILE1

## 1nm step calc for Millidegree
Ns=`cat /tmp/tmp2_Mildg_$FILE1 |awk 'NR==1 {printf("%d\n",$1)}'`
Ne=`cat /tmp/tmp2_Mildg_$FILE1 |awk 'END {printf("%d\n",$1)}'`
n=$Ns
 for ((n; n>=$Ne; n--))
  do
  i=`cat /tmp/tmp2_Mildg_$FILE1 |awk '/'$n'.0000/ {print $2}'`
  echo "$n	$i" >> /tmp/tmp2_Mildg_1nm_$FILE1
 done
cat /tmp/tmp2_Mildg_1nm_$FILE1 > ./Anal_$FILE1/Mildg_1nm_$FILE1


## MRE
awk 'BEGIN{OFS="\t"}{print($1,$2*'$M')}' /tmp/tmp2_$FILE1 > /tmp/tmp2_MRE_$FILE1 
cat /tmp/tmp2_MRE_$FILE1 > ./Anal_$FILE1/MRE_$FILE1

## 1nm step calc for MRE
n=$Ns
 for ((n; n>=$Ne; n--))
  do
  i=`cat /tmp/tmp2_MRE_$FILE1 |awk '/'$n'.0000/ {print $2}'`
  echo "$n      $i" >> /tmp/tmp2_MRE_1nm_$FILE1
 done
cat /tmp/tmp2_MRE_1nm_$FILE1 > ./Anal_$FILE1/MRE_1nm_$FILE1


## [Theta]
awk 'BEGIN{OFS="\t"}{print($1,$2/'$T')}' /tmp/tmp2_$FILE1 > /tmp/tmp2_Theta_$FILE1
cat /tmp/tmp2_Theta_$FILE1 > ./Anal_$FILE1/Theta_$FILE1

## 1nm step calc for Theta
n=$Ns
 for ((n; n>=$Ne; n--))
  do
  i=`cat /tmp/tmp2_Theta_$FILE1 |awk '/'$n'.0000/ {print $2}'`
  echo "$n      $i" >> /tmp/tmp2_Theta_1nm_$FILE1
 done
cat /tmp/tmp2_Theta_1nm_$FILE1 > ./Anal_$FILE1/Theta_1nm_$FILE1


## Del-Epsilon
awk 'BEGIN{OFS="\t"}{print($1,$2/'$E')}' /tmp/tmp2_Theta_$FILE1 > /tmp/tmp2_DelEps_$FILE1
cat /tmp/tmp2_DelEps_$FILE1 > ./Anal_$FILE1/DelEps_$FILE1

## 1nm step calc for Del-Epsilon
n=$Ns
 for ((n; n>=$Ne; n--))
  do
  i=`cat /tmp/tmp2_DelEps_$FILE1 |awk '/'$n'.0000/ {print $2}'`
  echo "$n      $i" >> /tmp/tmp2_DelEps_1nm_$FILE1
 done
cat /tmp/tmp2_DelEps_1nm_$FILE1 > ./Anal_$FILE1/DelEps_1nm_$FILE1


rm -rf /tmp/tmp_*
rm -rf /tmp/tmp2_*
