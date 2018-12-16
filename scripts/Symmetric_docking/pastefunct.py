
import sys

try:
	f1 = sys.argv[1]
	f2 = sys.argv[2]

except:
	print "Sequence files required."
	sys.exit(1)

seqs1 = []
seqs2 = []

for i in open(f1):
        li1=i.strip()
        if not li1.startswith(">"):
                seqs1.append(i.strip())
		x = ''
		for u in seqs1:
			x=x+u

for j in open(f2):
        li2=j.strip()
        if not li2.startswith(">"):
                seqs2.append(j.strip())
                y = ''
                for v in seqs2:
			y=y+v

for a, i in enumerate(seqs1):
	for b, j in enumerate(seqs2):
			print ">",a+1,"_",b+1,"_"
			print i+j
