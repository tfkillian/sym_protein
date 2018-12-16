#!/usr/bin/env python

import os
import optparse
import re
#from rosetta import *
from rosetta import Pose
from rosetta import pose_from_pdb
from toolbox import *

one_to_three = {'A': 'ALA',
                'R': 'ARG',
                'N': 'ASN',
                'D': 'ASP',
                'C': 'CYS',
                'E': 'GLU',
                'Q': 'GLN',
                'G': 'GLY',
                'H': 'HIS',
                'I': 'ILE',
                'L': 'LEU',
                'K': 'LYS',
                'M': 'MET',
                'F': 'PHE',
                'P': 'PRO',
                'S': 'SER',
                'T': 'THR',
                'W': 'TRP',
                'Y': 'TYR',
                'V': 'VAL',
            }

def sequence_mapping(pdb_file, sequence_file, score_file, relax, jobs):
    if os.path.exists( os.getcwd() + '/' + pdb_file ) and pdb_file:
        init()
        pose = Pose()
        score_fxn = create_score_function('talaris2013')
        if (relax):
            refinement = FastRelax(score_fxn)
        pose_from_pdb(pose, pdb_file)
        if os.path.exists( os.getcwd() + '/' + sequence_file ) and sequence_file:
            fid = open(sequence_file,'r')
            fod = open(score_file,'w')
            data = fid.readlines()
            fid.close()
            sequences = []
            read_seq = False
            for i in data:
                if not len(i):
                    continue
                elif i[0] == '>':
                    read_seq = True
                    fasta_line = re.split(':|\s+|\||\\n',i[1:])
                    name_cpt=0
                    while (name_cpt<len(fasta_line) and not fasta_line[name_cpt]):
                        name_cpt+=1
                    if name_cpt<len(fasta_line):
                        job_output = fasta_line[name_cpt]
                    else:
                        print 'Error: Please enter an identifier for sequences in your fasta file'
                        exit(1)
                elif read_seq:
                    seq=list(i)
                    resn=1
                    for j in i:
                        if j!='\n' and resn<=pose.total_residue():
                            mutator = MutateResidue( resn , one_to_three[j] )
                            mutator.apply( pose )
                            resn+=1
                        elif resn>pose.total_residue():
                            print 'WARNING: couldn\'t mutate residue number '+str(resn)+', sequence too long for backbone...'
                            resn+=1
                    if (relax):
                        jd = PyJobDistributor(job_output, jobs, score_fxn)
                        jd.native_pose = pose
                        scores = [0]*(jobs)
                        counter = 0
                        decoy=Pose()
                        while not jd.job_complete:
                            decoy.assign(pose)
                            resn=1
                            refinement.apply(decoy)
                            jd.output_decoy(decoy)
                            scores[counter]=score_fxn(decoy)
                            counter+=1
                        for i in range(0, len(scores)):
                            fod.writelines(job_output + '_' + str(i+1) + ' : '+str(scores[i])+'\n')
                    else:
                        pose_packer = standard_packer_task(pose)
                        pose_packer.restrict_to_repacking()
                        packmover = PackRotamersMover(score_fxn, pose_packer)
                        packmover.apply(pose)
                        fod.writelines(job_output+' : '+str(score_fxn(pose))+'\n')
                        pose.dump_pdb(job_output+'_1.pdb')
                else:
                    print 'Bad fasta format'
                    exit(1)
            fod.close()
        else:
            print 'Please provide a valid sequence file, '+sequence_file+' doesn\'t exist'
    else:
       print 'Please provide a valid backbone file, '+pdb_file+' doesn\'t exist' 

parser=optparse.OptionParser()
parser.add_option('--backbone', dest = 'pdb_file',
    default = '',    
    help = 'the backbone in PDB format' )

parser.add_option('--sequences', dest = 'seq_file',
    default = '',    
    help = 'the sequences to map' )

parser.add_option('--out', dest = 'score_out',
    default = 'scores.sc',    
    help = 'the score file to output' )

parser.add_option('--clean', action="store_true", dest = 'clean_pdb',
    default = False,
    help = 'makes the pdb Rosetta friendly' )

parser.add_option('--no_relax',action="store_false", dest = 'relax',
    default = True,    
    help = 'no relaxation after sequence mapping' )

parser.add_option('--nstruct', dest = 'jobs',
    default = '1',    
    help = 'number of relaxations per sequence' )

(options,args) = parser.parse_args()

pdb_file=options.pdb_file
sequence_file = options.seq_file
score_file=options.score_out
clean_pdb=options.clean_pdb
relax=options.relax
jobs=int(options.jobs)

if clean_pdb:
    cleanATOM( pdb_file )
    sequence_mapping(pdb_file[:-4]+'.clean.pdb', sequence_file, score_file, relax, jobs)
else:
    sequence_mapping(pdb_file, sequence_file, score_file, relax, jobs)

