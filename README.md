# MrHAMER (Multi-read Hairpin Mediated Error-correction Reaction)

[![Available in bioRxiv](https://img.shields.io/badge/Available%20in-bioRxiv-red)](https://www.biorxiv.org/content/10.1101/2021.01.27.428469v1)

Scripts for the generation of high accuracy single molecule Nanopore reads using the MrHAMER pipeline (https://www.biorxiv.org/content/10.1101/2021.01.27.428469v1)

## Dependencies

We recommend installing in a Python or Conda environment to ensure recommended versions are installed. Pipeline is compatible with Ubuntu 16 and 18 LTS.

1. Python 2.7.12
2. Python 3.5.2
3. Guppy basecaller v3.6.0
4. Porechop v0.2.4
5. Filtlong v0.2.0
6. minimap2 v2.17-r954-dirty
7. Racon v1.4.3
8. samtools v1.9 (with htslib 1.9)
9. Medaka v1.0.1
10. Pomoxis v0.2.3
11. CoVaMa v0.7
12. MAFFT v7.471
13. CliqueSNV v1.5.4

## Installation
To install these MrHAMER scripts run the following commands:

```bash
git clone --recursive https://github.com/gallardo-seq/MrHAMER.git
```

After successful downloading of the scripts, a folder named `MrHAMER` will appear in current working directory.

## Usage
Usage of `MrHAMER` is as following:

1. Combine all sequencing reads into single FASTQ file
2. Use Porechop to segment the concatemers based on the presence of MrHAMER hairpin sequence (this requires a custom adapters.py file, a template file is included in this repository)

        porechop -i [combined.fastq] -o [porechop.output] -t [threads] --extra_middle_trim_bad_side 0 --extra_middle_trim_good_side 0

3. Filter porechop.output with Filtlong
           
        filtlong --min_length 4000 [porechop.output] > [filtlong.output]
           
4. Demultiplexing of reads processed with Porechop and filtered with Filtlong, and filtering for minimum number of repetitive units per single molecule concatemer. This results in a folder that contains single FASTQ files, each containing a multiple number of repetitive units used for error correction in the next step.

        python2 ./qfilesplitterV3.1.py -i [filtlong.output] -o [output path] -b [min. number of repetitive units]

        python qfilespliter.py [Arguments]
        
            Arguments:
            -i input file
            -o output path
            -b blocks size cutoff [optional]

5. Running parallel instances of minimap2 > racon > medaka to polish each FASTQ file, resulting in high accuracy single molecule sequences. This step has been optimized for a system running 40 threads.

        python3 protocolV3.3.py -q [path to output folder from previous step] -r [path to reference sequence] -m r941_min_high_g360
        
        python protocol.py [Arguments]
        
        Arguments:
        -q fastq files
        -r reference
        -n number of iterations [Default 1]
        -m model for medaka [Default r941_min_high]
        -noMedaka if the parameter is present exclude medaka from the process
        -noRacon if the parameter is present exclude racon from the process

6. High accuracy single molecule sequences are output in new directory called "medaka_output", with high accuracy single molecule sequences concatenated in a single medaka_consensus.fasta file within this directory.

**A note about reference sequence used for Step 5. This pipeline is optimized for reference-based alignment. For a de-novo based approach, the outputs of Step 4 can be used with the "medaka smolecule" module, which used SPOA to generate a reference assembly for each originating FASTQ file (https://github.com/nanoporetech/medaka). 

## Contact information

For additional information, help and bug reports please send an email to christian.gallardo@seattlechildrens.org

## Acknowledgment

This work was supported by the National Institute of Allergy and Infectious Diseases [U54AI150472 to BET and ALR, P30AI036214-26 to BET, SJL and DMS]; the National Human Genome Research Institute [R01HG009622 to BET]; the Scripps Translational Science Institute [UL1TR001114-03 to BET]; and the University of Texas System Rising STARs Award to ALR.
