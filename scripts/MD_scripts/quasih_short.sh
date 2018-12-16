#!/bin/bash

/usr/bin/env awk 'BEGIN{

    # This script is useful for calculating the entropy from a MD simulation
    # It is set up to use the mass weighted covariance matrix from gromacs
    #
    # If you have a trajectory that goes up to 1000 ps (for example):
    #
    # for ((i=500;i<=1000;i+=50)); do
    #    g_covar -f traj_md.trr -s topol_md.tpr -mwa -o eigen$i.xvg -e $i
    #    done
    #
    # This will spit out the eigenvalues of the covariance matrix as a
    # function of time in xmgrace format (you could plot it).  This script
    # reads the .xvg file and calculated the entropy.  You can then get useful
    # data like:
    #
    # for((i=500;i<=1000;i+=50)); do echo $i `sh quasi.sh eigen$i.xvg`; done
    #

    # Tom Venken - 21 dec 09
    # problem with NAN (Not A Number) when calculating too high values, correction made
        
        
    infile = ARGV[1]
        
    # Need to convert kTe^2/hbar^2 to 1/amu/nm^2
        
    factor = 4565.9

    # Need kb in J/mol/K
    kb = 8.3144
        
    entropy = 0
	entropykcal = 0
	entropydeel = 0
    havedata = 0
	temp = 298
        
    while ((getline < infile) > 0 ) {
            
        if($1~"TYPE"){
            getline < infile
            havedata = 1
        }
        
        if(havedata == 1) {
			entropydeel = log($2*factor + 1)
			if (entropydeel != nan) {
            entropy += log($2*factor + 1) 
			}
        }
        
    }
   	
    entropykcal = -temp*0.5*kb*entropy/4184
    entropy = 0.5*kb*entropy
    printf("%g \t", entropykcal);

}' $*
