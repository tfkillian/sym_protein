#!/bin/sh

###############
#### GNUPLOT###
###############
gnuplot -e "
  set nokey;
  set xlabel 'Temperature (degree Celsius)' ;
  set ylabel 'CD (milli degree)' ;
  set yrange [$YMIN:$YMAX] ;

  set terminal pdf font 'Arial, 14' enhanced size 4in, 3in;
  set output 'Wave_plots.pdf';

  list=system('ls *.txt');

  n0=1;
  n1=words(list);
  dn=1;

  load '/home/noguhiro/software/CD/cd-tm-wave_pdf-loop.plt';
  
  
  #pause -1
  "

#  set terminal pdf font 'Arial,14' enhanced size 4in, 3in;
#  set output 'Heatmap_$FILE1.pdf';
#  splot '$FILE1';
