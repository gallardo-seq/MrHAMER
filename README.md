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

Demultiplexing of reads processed with Porechop, and filtering for minimum number of repetitive units per single molecule concatemer:

    python2 ./qfilesplitterV3.1.py -i <sequences> -o <output path> -b <min. number of repetitive units>

        python qfilespliter.py [Arguments]
        
            Arguments:
            -i input file
            -o output path
            -b blocks size cutoff [optional]

        

## Contact information

For additional information, help and bug reports please send an email to one of the following: ivan.sovic@irb.hr, robert.vaser@fer.hr, mile.sikic@fer.hr, nagarajann@gis.a-star.edu.sg

## Acknowledgment

This work has been supported in part by Croatian Science Foundation under the project UIP-11-2013-7353. IS is supported in part by the Croatian Academy of Sciences and Arts under the project "Methods for alignment and assembly of DNA sequences using nanopore sequencing data". NN is supported by funding from A*STAR, Singapore.
