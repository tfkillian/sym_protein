#!/usr/bin/env python
import numpy as np
import commands
import os
import sys

print '#################################################################'
print '# cd-tm2gnu.py (Python2), 11/April/2017, Created by Hiroki Noguchi #'
print '#################################################################'

args=sys.argv

file=args[1]

print 'CD File:' + file

print 'Loading CD File...'
raw = np.loadtxt(file)
print raw
print 'done.'

raws, cols = raw.shape

raws_num = raws - 1
cols_num = cols - 1

################
# Make Directory#
################
print 'Make output directory...',

os.mkdir('Analy_'+file)
os.mkdir('Analy_'+file +'/wavelength')
os.mkdir('Analy_'+file +'/temperature')

print 'done.'


################
# HEAT MAP #####
################

print 'Generating gnuplot heatmap input file...',


g=open('Analy_'+file + '/heatmap_'+ file, 'w')
pass
g.close()

raw_0=0
raw_n=0
N=1

g=open('Analy_'+file + '/heatmap_'+file, 'a')
for n in range(raws_num):
 for i in range(cols_num):
  raw_0=N
  raw_n=i+1
  gi0=raw[raw_0][0]
  gi1=raw[0][raw_n]
  gi2=raw[raw_0][raw_n]
  g.write(str(gi0))
  g.write('\t')
  g.write(str(gi1))
  g.write('\t')
  g.write(str(gi2))
  g.write('\n')
 g.write('\n')
 N=N+1
g.close()

print 'done.'


################
# Wavelength###
################

wv_f=raw[1,0]
wv_fin=raw[raws_num,0]

wvn=wv_f
N=01

print 'Generating gnuplot wavelength analysis input file...',


for n in range(raws_num):
 wvl=np.where(raw == wvn)
 wv=wvl[0][0]
 g=open('Analy_'+file +'/wavelength/' + str('%02.f'%N) + '-' + str(raw[wv,0]) +'nm.txt', 'w')
 g.close()
 g=open('Analy_'+file +'/wavelength/' + str('%02.f'%N) + '-' + str(raw[wv,0]) +'nm.txt', 'a')
 for i in range(cols_num):
  raw_n=i+1
  gi0=raw[0][raw_n]
  gi1=raw[wv][raw_n]
  g.write(str(gi0))
  g.write('\t')
  g.write(str(gi1))
  g.write('\n')
 g.close()
 if wvn == wv_fin:
  break
 wvn=wvn - 1
 N=N+1

print 'done.'


################
# Temperature ##
################

N=01

print 'Generating gnuplot temperature analysis input file...',


for n in range(cols_num):
 temp=raw[0,N]
 #print temp
 g=open('Analy_'+file +'/temperature/' + str('%02.f'%N) + '-' + str(temp) +'C.txt', 'w')
 g.close() 
 g=open('Analy_'+file +'/temperature/' + str('%02.f'%N) + '-' + str(temp) +'C.txt', 'a')
 for i in range(raws_num):
  raw_0=i+1
  gi0=raw[raw_0][0]
  gi1=raw[raw_0][N]
  g.write(str(gi0))
  g.write('\t')
  g.write(str(gi1))
  g.write('\n')
 N=N+1

print 'done.'
