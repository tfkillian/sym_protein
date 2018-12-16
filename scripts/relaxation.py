#!/usr/bin/env python

import os
import optparse
from pyrosetta import *
from rosetta import *
from rosetta.protocols.relax import *
from rosetta.core.pose import *
from pyrosetta.toolbox import *


parser=optparse.OptionParser()
parser.add_option('--pdb', dest = 'pdb_file',
    default = '',    
    help = 'the PDB file to relax' )

parser.add_option('--pdbout', dest = 'pdbout',
    default = '',    
    help = 'the PDB file to output' )

parser.add_option('--symmetry', dest = 'symmetry',
    default = False, action="store_true",
    help = 'Are we running symmetry ?' )

parser.add_option('--justscore', dest = 'justscore',
    default = False, action="store_true",
    help = 'Just score the structure' )

parser.add_option('--flags', dest = 'flags',
    default = '',    
    help = 'Relax flags file' )

parser.add_option('--scorefxn', dest = 'scorefxn',
    default = 'beta_nov16',    
    help = 'Score function' )

parser.add_option('--scorefile', dest = 'scorefile',
    default = 'score.dat',    
    help = 'Score file' )

(options,args) = parser.parse_args()

initflags=""

if (options.flags):
    initflags="@"+options.flags
else:
    initflags="-corrections::beta_nov16 "
init(initflags)
pose = Pose()
score_fxn = create_score_function(options.scorefxn)
pose = pose_from_file(options.pdb_file)

if (options.justscore):
    with open(options.scorefile,'a') as f:
        f.write(pose.pdb_info().name()[:-4]+" "+str(score_fxn(pose))+"\n")
else:
    if (options.symmetry):
        core.pose.symmetry.make_symmetric_pose(pose)
    refinement = FastRelax(score_fxn)
    refinement.apply(pose)
    pose.dump_pdb(options.pdbout)
    with open(options.scorefile,'a') as f:
        f.write(pose.pdb_info().name()[:-4]+" "+str(score_fxn(pose))+"\n")

