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
cd MrHAMER
```

After successful installation, an executable named `racon` will appear in `build/bin`.

Optionally, you can run `sudo make install` to install racon executable to your machine.

***Note***: if you omitted `--recursive` from `git clone`, run `git submodule update --init --recursive` before proceeding with compilation.

To build unit tests add `-Dracon_build_tests=ON` while running `cmake`. After installation, an executable named `racon_test` will be created in `build/bin`.

To build the wrapper script add `-Dracon_build_wrapper=ON` while running `cmake`. After installation, an executable named `racon_wrapper` (python script) will be created in `build/bin`.

### CUDA Support
Racon makes use of [NVIDIA's GenomeWorks SDK](https://github.com/clara-parabricks/GenomeWorks) for CUDA accelerated polishing and alignment.

To build `racon` with CUDA support, add `-Dracon_enable_cuda=ON` while running `cmake`. If CUDA support is unavailable, the `cmake` step will error out.
Note that the CUDA support flag does not produce a new binary target. Instead it augments the existing `racon` binary itself.

```bash
cd build
cmake -DCMAKE_BUILD_TYPE=Release -Dracon_enable_cuda=ON ..
make
```

***Note***: Short read polishing with CUDA is still in development!

### Packaging
To generate a Debian package for `racon`, run the following command from the build folder -

```bash
make package
```

## Usage
Usage of `racon` is as following:

    racon [options ...] <sequences> <overlaps> <target sequences>

        # default output is stdout
        <sequences>
            input file in FASTA/FASTQ format (can be compressed with gzip)
            containing sequences used for correction
        <overlaps>
            input file in MHAP/PAF/SAM format (can be compressed with gzip)
            containing overlaps between sequences and target sequences
        <target sequences>
            input file in FASTA/FASTQ format (can be compressed with gzip)
            containing sequences which will be corrected

    options:
        -u, --include-unpolished
            output unpolished target sequences
        -f, --fragment-correction
            perform fragment correction instead of contig polishing (overlaps
            file should contain dual/self overlaps!)
        -w, --window-length <int>
            default: 500
            size of window on which POA is performed
        -q, --quality-threshold <float>
            default: 10.0
            threshold for average base quality of windows used in POA
        -e, --error-threshold <float>
            default: 0.3
            maximum allowed error rate used for filtering overlaps
        --no-trimming
            disables consensus trimming at window ends
        -m, --match <int>
            default: 3
            score for matching bases
        -x, --mismatch <int>
            default: -5
            score for mismatching bases
        -g, --gap <int>
            default: -4
            gap penalty (must be negative)
        -t, --threads <int>
            default: 1
            number of threads
        --version
            prints the version number
        -h, --help
            prints the usage

    only available when built with CUDA:
        -c, --cudapoa-batches <int>
            default: 0
            number of batches for CUDA accelerated polishing per GPU
        -b, --cuda-banded-alignment
            use banding approximation for polishing on GPU. Only applicable when -c is used.
        --cudaaligner-batches <int>
            default: 0
            number of batches for CUDA accelerated alignment per GPU
        --cudaaligner-band-width <int>
            default: 0
            Band width for cuda alignment. Must be >= 0. Non-zero allows user defined
            band width, whereas 0 implies auto band width determination.

`racon_test` is run without any parameters.

Usage of `racon_wrapper` equals the one of `racon` with two additional parameters:

    ...
    options:
        --split <int>
            split target sequences into chunks of desired size in bytes
        --subsample <int> <int>
            subsample sequences to desired coverage (2nd argument) given the
            reference length (1st argument)
        ...

## Contact information

For additional information, help and bug reports please send an email to one of the following: ivan.sovic@irb.hr, robert.vaser@fer.hr, mile.sikic@fer.hr, nagarajann@gis.a-star.edu.sg

## Acknowledgment

This work has been supported in part by Croatian Science Foundation under the project UIP-11-2013-7353. IS is supported in part by the Croatian Academy of Sciences and Arts under the project "Methods for alignment and assembly of DNA sequences using nanopore sequencing data". NN is supported by funding from A*STAR, Singapore.
