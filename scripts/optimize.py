#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import argparse
import os, shutil, re, subprocess
from inspect import getsourcefile

from rosetta import *
from pyrosetta import *
from pyrosetta.toolbox import *
from rosetta.core.scoring import *
from rosetta.core.pack.task import *
from rosetta.core.pack.rotamer_set import *
from rosetta.core.pack.rotamer_set.symmetry import *
from rosetta.core.pack.interaction_graph import *
from rosetta.core.pack import *
from rosetta.protocols.relax import *
from rosetta.protocols.simple_moves.symmetry import *
from rosetta.protocols.rigid import *
from argparse import ArgumentParser

PARPATH = "./pars"
AAs = "ARNDCQEGHILKMFPSTWYV"

def energy2cost(energy,min_energy):
    return int(round(pow(10,precision)*(energy-min_energy)))

def eshow(scorefunction, pose, filen):
    with open(filen,'w') as f:
        score = scorefunction(pose)
        f.write("------------------------------------------------------------\n")
        f.write(" Scores                       Weight   Raw Score Wghtd.Score\n")
        f.write("------------------------------------------------------------\n")
        sum_weighted = 0.0
        w = scorefunction.weights()
        te = pose.energies().total_energies()
        nzwt =  scorefunction.get_nonzero_weighted_scoretypes()
        for ti in range(1,len(nzwt)+1):
            name = name_from_score_type(nzwt[ti])
            weight = w[nzwt[ti]]
            energy = te[nzwt[ti]]
            wenergy = weight*energy
            f.write("{:24s}".format(name)+' ')
            f.write("{:9.3f}".format(weight)+'   ')
            f.write("{:9.3f}".format(energy)+'   ')
            f.write("{:9.3f}".format(wenergy)+'\n')
            sum_weighted += te[nzwt[ti]]*w[nzwt[ti]]
        f.write("---------------------------------------------------\n")
        f.write(" Total weighted score:                           {:9.3f}".format(sum_weighted)+'\n')

def readm(filen):
    with open (filen, 'r') as f:
        return dict(zip(AAs, [dict(zip(AAs, map(int,line.split()))) for line in f]))

def verbosify(m,l):
    if (verbose >= l): print m

# more feedback than os.system
def execute(message, commandline):
    print message
    print commandline
    proc = subprocess.call(commandline, shell = True)

def par_name(par):
    return os.path.join(PARPATH,par)

# if opt is set use it, else find in file, else use default
def arg_read(opt,fname,default):
    if (opt): return opt
    opt = default
    try:
        with open(par_name(fname), 'r') as argf:
            return argf.readline().strip()
    except FileNotFoundError:
        return opt

def rosetta_init():
    init_line = rotamers
    if ('beta' in scorefunction):  init_line += " -beta"
    init_line += " -out:level "+str(verbose*100)
    if fixed_seed: init_line += " -run:constant_seed "
    init(init_line)
    
####################################################################
# generates a wcsp format CFN in wcsp_out for pose using resfile for
# flexibility and scorefunc as the force field. We assume the pose and
# the score function have been symmetrized

def generate_wcsp(pose, resfile, wcsp_out, shft_out, scorefunc,bias,mat):
    f = open(wcsp_out,'w')
    domainsizes = []
    min_energy1 =[]
    min_energy2 =[]
    shift = 0.0
    maxdomainsize = 0
    nb_energies = 0
    ub = 0.0
    nb_costfunctions = 0
    nmut = 0

    varseq2rot = []
    verbosify("\nGenerating wcsp file for "+pose.pdb_info().name()[:-4],1)
    task_design = TaskFactory.create_packer_task(pose)
    task_design.initialize_from_command_line()
    parse_resfile(pose, task_design, resfile)
    symmpack = protocols.simple_moves.symmetry.SymPackRotamersMover(scorefunc, task_design)
    pose.update_residue_neighbors()
    verbosify("Generating packer graph",1)
    symtask = symmpack.make_symmetric_task(pose, task_design)
    rotsets = SymmetricRotamerSets()
    pack_scorefxn_pose_handshake(pose, scorefunc)
    ig = pack_rotamers_setup( pose, scorefunc, symtask, rotsets )

    verbosify("Extracting one body terms",1)
    for res1 in range(1,ig.get_num_nodes()+1):
        min_energy = float("inf")
        max_energy = float("-inf")
        seq2rot = []
        mutable = False
        natAA = pose.residue(res1).name1()
        irotAA =  rotsets.rotamer_set_for_moltenresidue(res1).rotamer(1).name1()
        for i in range(1, rotsets.rotamer_set_for_moltenresidue(res1).num_rotamers()+1):
            rotAA = rotsets.rotamer_set_for_moltenresidue(res1).rotamer(i).name1()
            if (rotAA != irotAA): mutable = True
            energy = ig.get_one_body_energy_for_node_state(res1,i)
            if (bias != 0.0):
                energy -= mat[natAA][rotAA]*bias
            nb_energies += 1
            if (energy < min_energy):
                min_energy = energy
            if (energy > max_energy):
                max_energy = energy
            seq2rot.append(tuple([rotsets.rotamer_set_for_moltenresidue(res1).rotamer(i).name1(), i-1]))
        varseq2rot.append(seq2rot)
        if (mutable): nmut+= 1
        min_energy1.append(min_energy)
        domainsizes.append(rotsets.rotamer_set_for_moltenresidue(res1).num_rotamers())
        ub += max_energy
        shift += min_energy
        nb_costfunctions += 1
        if (domainsizes[res1-1] > maxdomainsize):
            maxdomainsize = domainsizes[res1-1]

    verbosify("Extracting two bodies terms",1)
    for res1 in range(1,ig.get_num_nodes()+1):
        for res2 in range(res1+1,ig.get_num_nodes()+1):
            min_energy = float("inf")
            max_energy = float("-inf")
            if (ig.get_edge_exists(res1, res2)):
                for i in range(1, rotsets.rotamer_set_for_moltenresidue(res1).num_rotamers()+1):
                    for j in range(1, rotsets.rotamer_set_for_moltenresidue(res2).num_rotamers()+1):
                        energy = ig.get_two_body_energy_for_edge(res1,res2,i,j)
                        nb_energies += 1
                        if (energy < min_energy):
                            min_energy = energy 
                        if (energy > max_energy):
                            max_energy = energy
                ub += max_energy
                min_energy2.append(min_energy)
                shift += min_energy
                nb_costfunctions += 1
    
#    tb2_default_cost = energy2cost(0,min_energy)
    ub = energy2cost(ub,shift)+1

    # Writing wcsp file
    verbosify("Saving wcsp file",1)
    nbvars = len(varseq2rot)

    f.write("pose "+str(nbvars)+" "+str(maxdomainsize)+" "+str(nb_costfunctions)+" "+str(ub)+'\n')
    # domains
    for i in range(0, len(domainsizes)-1):
        f.write(str(domainsizes[i])+" ")
    f.write(str(domainsizes[len(domainsizes)-1])+'\n')

    # unary cost functions
    discarded = 0
    for res1 in range(1,ig.get_num_nodes()+1):
        tuples = ""
        nbtuples = 0
        min_energy = min_energy1.pop(0)
        tb2_default_cost =  max(0,energy2cost(0,min_energy))
        for i in range(1, rotsets.rotamer_set_for_moltenresidue(res1).num_rotamers()+1):
            energy = ig.get_one_body_energy_for_node_state(res1,i)
            tb2energy = energy2cost(energy,min_energy)
            if (tb2energy != tb2_default_cost):
                tuples += str(i-1)+" "+str(tb2energy)+'\n'
                nbtuples += 1
            else:
                discarded += 1
        f.write("1 "+str(res1-1)+" "+str(tb2_default_cost)+" "+str(nbtuples)+'\n')
        f.write(tuples)

    #binary cost functions    
    for res1 in range(1,ig.get_num_nodes()):
        for res2 in range(res1+1,ig.get_num_nodes()+1):
            tuples = ""
            nbtuples = 0
            if (ig.get_edge_exists(res1, res2)):
                min_energy = min_energy2.pop(0)
                tb2_default_cost =  max(0,energy2cost(0,min_energy))
                for i in range(1, rotsets.rotamer_set_for_moltenresidue(res1).num_rotamers()+1):
                    for j in range(1, rotsets.rotamer_set_for_moltenresidue(res2).num_rotamers()+1):
                        energy = ig.get_two_body_energy_for_edge(res1,res2,i,j)
                        tb2energy = energy2cost(energy,min_energy)
                        if (tb2energy != tb2_default_cost):
                            tuples += str(i-1)+" "+str(j-1)+" "+str(tb2energy)+'\n'
                            nbtuples += 1
                        else:
                            discarded += 1
                f.write("2 "+str(res1-1)+" "+str(res2-1)+" "+str(tb2_default_cost)+" "+str(nbtuples)+'\n')
                f.write(tuples)

    # rotamers for CPD wcsp  format
    for seqrots in varseq2rot:
        for seqrot in seqrots:
            f.write(seqrot[0]+" ")
        f.write('\n')
    f.close()
    verbosify("Saving energy shift file",1)
    with open(shft_out,'w') as f:
        f.write(str(shift)+" "+str(precision)+" "+str(nmut))
    verbosify("done.",1)


#################################################
# creates a pdb out_file that represents the toulbar2 solution stored
# in mat. If pwa is set to True, dumps statistics about the toulbar2
# solution and stores them in out_file. The pose must be the exact one 
# that one used to create energy matrices for toulbar2.
def load_assign(pose, mat, out_file, resfile, scorefunc):
    task_design = TaskFactory.create_packer_task(pose)
    task_design.initialize_from_command_line()
    parse_resfile(pose, task_design, resfile)
    symmpack = protocols.simple_moves.symmetry.SymPackRotamersMover(scorefunc, task_design)
    pose.update_residue_neighbors()
    symtask = symmpack.make_symmetric_task(pose, task_design)
    rotsets = SymmetricRotamerSets()
    pack_scorefxn_pose_handshake(pose, scorefunc)
    ig = pack_rotamers_setup( pose, scorefunc, symtask, rotsets )
    
    for i in range(0, len(mat)):
        res = rotsets.rotamer_set_for_moltenresidue(i+1).rotamer(int(mat[i]+1))
        pose.replace_residue(rotsets.moltenres_2_resid(i+1), res, False)
    pose.dump_pdb(out_file)
    return pose
    
##################################################    
# extracts the optimum cost from toulbar2 output and computes the cost
# threshold for the required energy threshold. Return None if no solution.
def get_optimum(tb2log):
    for line in open(tb2log):
        if "Optimum:" in line:
            s = re.split(' ',line)
            return int(s[1])
    return None
 
##################################################    
# extracts the GMEC from toulbar2 output and computes the cost
# threshold for the required energy threshold
def get_enum_threshold(tb2log, enum):
    cost = get_optimum(tb2log)
    return int(cost+enum*pow(10,precision))
    
###########################################################################
parser = ArgumentParser()

parser.add_argument("--pymol", dest="pymol", action='store_true',
                      default = False, help = "Activate PyMOLmover")

parser.add_argument("--sym", dest="symfile",
                      default = "Dode1.sym", help = "Symmetry file")

parser.add_argument("--out", dest="out",
                      default = None, help = "Output PDB file")

parser.add_argument("--verbose", dest="verbose", type=int,
                      default = 2, help = "Speak me !")

parser.add_argument('pdb', metavar='pdb', type=str, nargs='?',
                    help='Assymetric subunit PDB')

parser.add_argument('--resfile', dest="resfile", type=str,
                    default= "fulld.resfile",help='Rosetta resfile')

options = parser.parse_args()
verbose = options.verbose
###############################################################################

init("-ex1 false -ex1aro false -ex2 false -ex2aro false -ex3 false -packing:use_input_sc -corrections:beta_nov16 -out:level "+str(options.verbose*100))
pypath="/opt/toulbar2/toulbar2/build/bin/Linux/"
precision = 8
scpbranch = False #True
pdbcode=options.pdb[:-4]
pose = pose_from_file(options.pdb)

sd = core.conformation.symmetry.SymmData(pose.total_residue(), pose.num_jump())
sd.read_symmetry_data_from_file(options.symfile)
smover = protocols.simple_moves.symmetry.SetupForSymmetryMover(sd)
smover.apply(pose)

dofs = sd.get_dofs()
rmover = protocols.rigid.RigidBodyDofSeqRandomizeMover(dofs)
rmover.apply(pose)
        
scoref = create_score_function("beta_nov16")
sscoref = rosetta.core.scoring.symmetry.symmetrize_scorefunction(scoref)

if options.pymol:
    pymover = rosetta.protocols.moves.PyMolMover()
    pymover.apply(pose)

#print(sscoref(pose))
#eshow(sscoref,pose,"out.show")
        
generate_wcsp(pose, options.resfile, pdbcode+".wcsp", pdbcode+".shft", sscoref, 0.0, None) #readm(psimatrix))
with open(pdbcode+".shft") as f:
    shift,precision,nmut = f.readline().split()
    shift = float(shift)
    precision = int(precision)

    tb2cmd= os.path.join(pypath,"toulbar2")+" "+pdbcode+".wcsp -dee: -O=-3 -B=1 -A -s -w="+pdbcode+".gmec"+" --cpd "
    if scpbranch:
        tb2cmd += "--scpbranch "
    tb2cmd += ("| tee " if (verbose > 1) else "> ")+pdbcode+".log"
    execute("Looking for GMEC with toulbar2",tb2cmd)
    gmec = get_optimum(pdbcode+".log")
    
with open(pdbcode+".gmec") as f:
    for last in f: pass
    conf = [int(x) for x in last.split()]

np = load_assign(pose, conf, pdbcode+"-gmec.pdb", options.resfile, sscoref)

#print(sscoref(np))
eshow(sscoref,np,pdbcode+".show")

        
if (options.pymol):
    pymover.apply(pose)

if (options.out):   
    pose.dump_file(options.out)

