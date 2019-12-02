# sym_protein

This describes a Symmetric Protein Design Pipeline using the RE^3volutionary protein design protocol using a series of Perl, Python and bash scripts. The scripts begin by accepting a *.pdb* file, consisting a manually extracted repeat motif, which will be subjected to a series of docking runs.

# RE 3 volutionary design protocol
Symmetric repeat proteins were design via the RE 3 volutionary design method developed by Voet lab: </br>
</br>
• (i) Structural and sequential information for the target protein to be designed is obtained from PDB. Inferred protein repeats are isolated and and submitted to a MSA to further refine the borders of each repeat structure. A phylogenetic tree of the repeat motifs is generated to ascertain their evolutionary relationship and sequence distance. The refined repeat motifs of the target protein are visualized in PyMol and extracted. Each repeat motif is trimmed by several amino acids bordering between each motif,
to prevent steric clashing during the subsequent symmetrical docking step. </br>
</br>
• (ii) Fitted extracted symmetrical repeats are submitted for symmetrical docking. Select criteria such as the RMSD, calculated energy scores and overall structural configuration of each of the symmetrical docking assemblies are compared. The top 5 scoring assemblies are visually inspected in PyMol. The most robust symmetrical assemble is used for generating a symmetric template. </br>
</br>
• (iii) The removed amino acids extracted during the repeat motif fitting process are re-introduced and mapped onto the backbone of the designed symmetric template via homology modeling using MOE TM. Bond making and bond breaking may be necessary to reconstruct structural elements native to the original protein, such as Velcro straps of β-propellers. </br>
</br>
• (iv) Individual FASTA sequences of the repeats are edited to an average residue count based on the consensus imputation of missing or additional residues from the repeat motif MSA of the original template protein. These new consensus imputed repeats are submitted to a new MSA, from which a new phylogenetic tree for these imputed repeats is produced. The consensus imputed repeat motifs and their phylogenetic tree are used to reconstruct a list of putative ancestral sequences for each node of the phylogenetic tree via maximum likelihood (ML) using FastML server. </br>
</br>
• (v) The putative ancestral sequences are mapped via homology modeling onto the designed protein structure template. The mapped
ancestral sequences are rescored and the RMSD, calculated energy scores and overall structural configuration of each of the symmetrical assemblies are compared to select the best sequence that is believed to present the highest probability of folding into the desired symmetrical scaffold structure. </br>
</br>
• (vi) The sequence of the candidate template scaffold is codon optimized for insertion into a recombinant plasmid and expressed in *E. coli* for further characterization </br>
