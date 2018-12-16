#!/bin/sh

FILE1=$1
YMAX=$2
ZMIN=$3
ZMAX=$4

#YMIN=$3

###############
#### GNUPLOT###
###############
gnuplot -e "
  set nokey;
  set xlabel 'Wavelength (nm)' ;
  set ylabel 'Temperature (degrees Celsius)' ;
  set yrange [$YMIN:$YMAX] ;
  set title '$FILE1';

  set ticslevel 0;
  set palette rgbformula 22,13,-31;
  set pm3d map;
  set cbrange[$ZMIN:$ZMAX];
 
  set terminal pngcairo font 'Arial, 20' enhanced size 1000,800;
  set output 'Heatmap_$FILE1.png';
  splot '$FILE1';  

  #pause -1
  "

#  set terminal pdf font 'Arial,14' enhanced size 4in, 3in;
#  set output 'Heatmap_$FILE1.pdf';
#  splot '$FILE1';
