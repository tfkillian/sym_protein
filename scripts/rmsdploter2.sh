#!/bin/bash

#input rmsdlist and score.fasc be unsorted, as produced by the Rosetta Docking and Ranker protocols
awk '{print $2}' rmsdlist > 1
awk '{print $2}' rescore_ref2015.fasc > 2
sed -i 1,2d 2
paste -d, 1 2 > rmsdplot.csv
rm 1
rm 2

#store current folder name
i=${PWD##*/}

#Retrieving minimum Energy and RMSD from RMSDplot.csv
 #      {a[$1]=$1;next}
  #      END{min(a)}' rmsdplot.csv}

#Making a script to plot rmsdplot.csv using gnuplot
echo > gnuplot.in
    echo "set datafile separator ','" >> gnuplot.in
    echo "set xlabel 'RMSD'" >> gnuplot.in
    echo "set ylabel 'Energy'" >> gnuplot.in
    echo "set xrang [0:6]" >> gnuplot.in
    echo "set yrang [-400:0]" >> gnuplot.in
    echo "set term png" >> gnuplot.in
    echo "set grid" >> gnuplot.in
    echo "set output '${i}_RMSD_plot.png'" >> gnuplot.in
    echo "plot 'rmsdplot.csv'" >> gnuplot.in

gnuplot gnuplot.in

