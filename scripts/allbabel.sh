#!/bin/bash
for i in *.pdb; do
	obabel $i -O "${i%.*}".fasta
done
