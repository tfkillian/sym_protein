#!/bin/sh

###############
#### GNUPLOT###
###############
gnuplot -e "
  set nokey;
  set xlabel 'Wavelength (nm)' ;
  set ylabel 'CD (milli degree)' ;
  set yrange [$YMIN:$YMAX] ;

  set terminal pdf font 'Arial, 14' enhanced size 4in, 3in;
  set output 'Temp_plots.pdf';
  
  list=system('ls *.txt');

  n0=1;
  n1=words(list);
  dn=1;
  
  f(x)=0;
  
  load '/home/noguhiro/software/CD/cd-tm-temp_pdf-loop.plt';
  
  #pause -1
  "

#  set terminal pdf font 'Arial,14' enhanced size 4in, 3in;
#  set output 'Heatmap_$FILE1.pdf';
#  splot '$FILE1';
#  plot for [i=1:words(list)] word(list, i) title word (list, i);
