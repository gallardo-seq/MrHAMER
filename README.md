# MrHAMER (Multi-read Hairpin Mediated Error-correction Reaction)

[![Available in bioRxiv](https://img.shields.io/badge/Available%20in-bioRxiv-red)](https://www.biorxiv.org/content/10.1101/2021.01.27.428469v1)

Scripts for the generation of high accuracy single molecule Nanopore reads generated using the MrHAMER pipeline (https://www.biorxiv.org/content/10.1101/2021.01.27.428469v1)

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
git clone --recursive https://github.com/gallardo-seq/MrHAMER.git racon
```

After successful downloading of the scripts, a folder named `MrHAMER` will appear in current working directory.

## Usage
Usage of `MrHAMER` is as following:

1. Combine all sequencing reads into single fastq file
2. Use Porechop to segment the concatemers based on the presence of MrHAMER hairpin sequence (this requires a custom adapters.py file, a template file is included in this repository)

        porechop -i [combined.fastq] -o [porechop.output] -t [threads] --extra_middle_trim_bad_side 0 --extra_middle_trim_good_side 0

4. Filter porechop.output with Filtlong
           
        filtlong --min_length 4000 [porechop.output] > [filtlong.output]
           
7. Demultiplexing of reads processed with Porechop and filtered with Filtlong, and filtering for minimum number of repetitive units per single molecule concatemer:

        python2 ./qfilesplitterV3.1.py -i [filtlong.output] -o [output path] -b [min. number of repetitive units]

        python qfilespliter.py [Arguments]
        
            Arguments:
            -i input file
            -o output path
            -b blocks size cutoff [optional]

        

## Contact information

For additional information, help and bug reports please send an email to christian.gallardo@seattlechildrens.org

## Acknowledgment

This work was supported by the National Institute of Allergy and Infectious Diseases [U54AI150472 to BET and ALR, P30AI036214-26 to BET, SJL and DMS]; the National Human Genome Research Institute [R01HG009622 to BET]; the Scripps Translational Science Institute [UL1TR001114-03 to BET]; and the University of Texas System Rising STARs Award to ALR.
