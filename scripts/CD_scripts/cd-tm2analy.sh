#!/bin/sh

echo '#################################################################'
echo 'cd-tm2analy.sh 11/April/2017, Created by Hiroki Noguchi'
echo '#################################################################'

FILE1=$1
curr_dir=`pwd`
echo CurrDir: $curr_dir
echo File: $FILE1

################
#Preparation file
################

echo 'Preparation raw cd file...'

sed -e 's/,/./g' $FILE1 > /tmp/tmp_$FILE1
sed -i -e 's/\r//g' /tmp/tmp_$FILE1
sed -e '1,20d' /tmp/tmp_$FILE1 > /tmp/tmp2_$FILE1

Chn2=`cat /tmp/tmp2_$FILE1 |awk '/Channel 2/ {print NR}'`
Chn2=`expr $Chn2 - 1`

sed -n '1,'$Chn2'p' /tmp/tmp2_$FILE1 > /tmp/tmp3_$FILE1
sed -e '1 s/^/9999/g' /tmp/tmp3_$FILE1 > /tmp/$FILE1

Ts=`cat /tmp/$FILE1 |awk 'NR==1 {printf("%d\n",$2)}'`
Tsn=`cat /tmp/$FILE1 |awk 'NR==1 {printf("%d\n",2)}'`
Te=`cat /tmp/$FILE1 |awk 'NR==1 {printf("%d\n",$NF)}'`
Ten=`cat /tmp/$FILE1 |awk 'NR==1 {printf("%d\n",NF)}'`
Ws=`cat /tmp/$FILE1 |awk 'NR==2 {printf("%d\n",$1)}'`
Wsn=`cat /tmp/$FILE1 |awk 'NR==2 {printf("%d\n",1)}'`
We=`cat /tmp/$FILE1 |awk 'END {printf("%d\n",$1)}'`
Wen=`cat /tmp/$FILE1 |awk 'END {printf("%d\n",1)}'`

Tn=`expr $Ten - 1`

echo 'Start Temperature:' $Ts
echo 'Finish Temperature:' $Te
echo 'Number of measurement Temperature points:' $Tn
echo 'Start Wavelength:' $Ws
echo 'End Wavelength:' $We


echo 'done'

################################################
#Preparation gnuplot input files by cd-tm2gnu.py
################################################
echo 'Preparation gnuplot input file...'
cd /tmp
cd-tm2gnu.py $FILE1
echo 'done'

echo 'Deleting tmp files and moving gnuplot input file...'
cd "$curr_dir"
mv /tmp/Analy_"$FILE1" "$curr_dir"
rm -rf /tmp/tmp*
rm -rf /tmp/$FILE1
echo 'done'

################################################
#Drawing Heat Map by gnuplot
################################################
echo 'Drawing heatmap figure by gnuplot...'
cd "$curr_dir/Analy_$FILE1"
cd-heatmap heatmap_"$FILE1" $Te
echo 'done'

################################################
#Drawing graph of wavelength by gnuplot
################################################
echo 'Drawing wavelength figure by gnuplot...'

cd "$curr_dir/Analy_$FILE1/wavelength"
cd-tm-wave_pdf.sh
mv "$curr_dir/Analy_$FILE1/wavelength/Wave_plots.pdf" "$curr_dir/Analy_$FILE1/Wave_$FILE1.pdf"

echo 'done'

################################################
#Drawing graph of Temperature by gnuplot
################################################
echo 'Drawing temperature figure by gnuplot...'

cd "$curr_dir/Analy_$FILE1/temperature"
cd-tm-temp_pdf.sh
mv "$curr_dir/Analy_$FILE1/temperature/Temp_plots.pdf" "$curr_dir/Analy_$FILE1/Temp_$FILE1.pdf"

echo 'done'






