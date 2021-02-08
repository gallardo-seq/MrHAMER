import os,glob
import subprocess
import sys
import time
from multiprocessing import Pool,cpu_count
from contextlib import closing
from itertools import product
from functools import partial

fastqPath = "./Qfileoutput/"
referencePath = "../HIV_Wt_Ref_NoBarcode.fa"
contigPath = "./"
consensusPAth = "./"
medaka_model = "r941_min_high"
medaka_output = "medaka_output"
n = 1

files = []
currentPath = ""
xc = 0
rc = 0

cores = 2

def print_command(arrCommand):
    strCommandData = ""
    for elm in arrCommand:
        strCommandData += elm+" "
    print (strCommandData)

def parse_config_file(filecontent):
    global xc,rc
    for line in filecontent:
        if "#" != line[0]:
            elements = line.split('=')
            if len(elements) == 2:
                if elements[0] == "XC":
                    xc = float(elements[1])
                elif elements[0] == "RC":
                    rc = float(elements[1])


def read_config_file():
    try:
        with open("protocol_config.conf") as f:
            parse_config_file(f.readlines())
    except Exception as e:
        print ("No config file found loadings default parameters {}".format(e))	

def get_fastqFiles():
    currentPath = os.getcwd()
    os.chdir(fastqPath)
    for model in glob.glob("*.fa*"):
        #files.append(os.path.join(fastqPath,model))
        files.append(model)
    os.chdir(currentPath)
    return files


def minimap_command(fileName, iteration):
    outputConcensusFile = "{}/consensus".format(fastqPath)
    if iteration > 1:
        reference = "{}/{}_consensus{}.fasta".format(outputConcensusFile, str(files[i])[:-6], iteration-1)
    else:
        reference = referencePath

    strCommandName = "minimap2"
    arrCommand = [strCommandName, reference, "{}{}".format(fastqPath, fileName)]

    print_command(arrCommand)

    proc = subprocess.Popen(arrCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    print (e.decode('ascii'))
    return o.decode('ascii')


def minimap_samtools_command_for_medaka(fileName, iteration):

    outputConcensusFile = "{}consensus".format(fastqPath)
    if iteration > 1:
        reference = "{}/{}_consensus{}.fasta".format(outputConcensusFile, str(files[i])[:-6], iteration-1)
    else:
        reference = referencePath

    #if not medaka_quality_filiter("{}/{}_consensus{}.fasta".format(outputConcensusFile, str(fileName)[:-6], n)):
    #    return "Quality fail"

    strCommandName = "minimap2"
    #arrCommand = [strCommandName, "-ax", "map-ont", "--MD", reference, "{}{}".format(fastqPath, fileName),
    #              "|", "samtools", "view", "-bS", "-", "|", "samtools", "sort", "-"]

    arrCommand = [strCommandName, "-ax", "map-ont", "--MD", reference, "{}{}".format(fastqPath, fileName)]
    print_command(arrCommand)
    proc = subprocess.Popen(arrCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    arrCommand = ["samtools", "view", "-bS", "-"]
    print_command(arrCommand)
    proc1 = subprocess.Popen(arrCommand, stdin=proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    arrCommand = ["samtools", "sort", "-"]
    print_command(arrCommand)
    proc2 = subprocess.Popen(arrCommand, stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    o, e = proc2.communicate()
    print (e.decode('ascii'))
    return o


def samtools_command_for_medaka(fileName):

    bamFilePath = "{}medaka_output".format(fastqPath)
    bamFile = "{}/{}.bam".format(bamFilePath, str(fileName)[:-6])

    strCommandName = "samtools"
    arrCommand = [strCommandName, "index", bamFile]
    print_command(arrCommand)

    proc = subprocess.Popen(arrCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    print (e.decode('ascii'))
    return o


def racon_command(fileName, iteration):
    outputMinmapFile = "{}contig/".format(fastqPath)
    outputConcensusFile = "{}/consensus".format(fastqPath)
    
    if iteration > 1:
        reference = "{}/{}_consensus{}.fasta".format(outputConcensusFile, str(files[i])[:-6], iteration - 1)
    else:
        reference = referencePath

    strCommandName = "racon"
    arrCommand = [strCommandName, "-m 8 -x -6 -g -8 -w 500" , "{}{}".format(fastqPath, fileName), "{}{}_contig{}.paf".format(outputMinmapFile, str(fileName)[:-6], iteration), reference]

    print_command(arrCommand)

    proc = subprocess.Popen(arrCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    print (e.decode('ascii'))
    return o.decode('ascii')


def parse_consensus_output(firstline):
    fxc=0
    frc=0
    print (firstline)
    items = firstline.split(' ')
    for itm in items:
        if "XC" in itm:
            fxc = float(itm.split(':')[2])
        elif "RC" in itm:
            frc = int(itm.split(':')[2])
    return fxc, frc


def medaka_quality_filter(filename1):
    with open(filename1) as f:
        firstline = f.readline()
        fxc, frc = parse_consensus_output(firstline)
    print (xc, fxc, rc, frc)
    if fxc >= xc and frc >= rc:
        return False
    return True


def medaka_consensus_command(fileName):

    bamFilePath = "{}medaka_output".format(fastqPath)
    bamFile = "{}/{}.bam".format(bamFilePath, str(fileName)[:-6])
    hdfFile = "{}/{}.hdf".format(bamFilePath, str(fileName)[:-6])
    
    strCommandName = "medaka"
    arrCommand = [strCommandName, "consensus", "--model", medaka_model, "--threads", "8",bamFile, hdfFile]

    print_command(arrCommand)

    proc = subprocess.Popen(arrCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    print (e.decode('ascii'))
    return o.decode('ascii')


def medaka_stich_command(fileName):
    hdfFilePath = "{}medaka_output".format(fastqPath)
    hdfFile= "{}/{}.hdf".format(hdfFilePath, str(fileName)[:-6])
    OutputFile = "{}/{}.fasta".format(hdfFilePath, str(fileName)[:-6])

    strCommandName = "medaka"
    arrCommand = [strCommandName, "stitch", hdfFile, OutputFile]

    print_command(arrCommand)

    proc = subprocess.Popen(arrCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    print (e.decode('ascii'))
    changeFastaHeader(OutputFile)
    return o.decode('ascii')

def changeFastaHeader(fileName):
	content = []
	if os.path.isfile(fileName):
		with open(fileName,"r") as f:
			content = f.readlines()
		#print(fileName,content)
		with open(fileName,"w") as f:
			if len(content) > 0:
				content[0] = ">{}\n".format(os.path.basename(fileName)[:-6])
				for line in content:
					f.write(line)
					#print(line)
			else:
				print("No content {}".format(fileName))
				print(content)
	else:
		print ("No file {}".format(fileName))


def combine_outputs():
    outputFile = "{}{}".format(fastqPath,medaka_output)
    strCommandName = "find"
    arrCommand = [strCommandName,outputFile, "-type", "f", "-name","*.fasta","-exec", "cat", "{}","+"]
    print_command(arrCommand)
    proc = subprocess.Popen(arrCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    print  (e.decode('ascii'))
    return o.decode('ascii')


def write_medaka_consensus_file(filecontent):
    outputFile = "{}{}".format(fastqPath,medaka_output)
    with open("{}/medaka_consensus.fasta".format(outputFile ), 'w') as f:
        print(filecontent)
       	f.write(filecontent)


def write_files_minimap(outputArray,iteration):
    outputFile = "{}contig".format(fastqPath)
    if not os.path.exists(outputFile):
        os.mkdir(outputFile)
    for i, outf in enumerate(outputArray):
        if len(outf) > 0:
            with open("{}/{}_contig{}.paf".format(outputFile, str(files[i])[:-6],iteration), 'w') as f:
                f.write(outf)


def write_files_racon(outputArray,iteration):
    outputFile = "{}/consensus".format(fastqPath)
    if not os.path.exists(outputFile):
        os.mkdir(outputFile)

    for i, outf in enumerate(outputArray):
        with open("{}/{}_consensus{}.fasta".format(outputFile, str(files[i])[:-6],iteration), 'w') as f:
            if len(outf) > 0:
                strcontent = ">{}{}".format(str(files[i])[:-6], outf[8:])
                f.write(strcontent)
                #print (strcontent)


def write_files_bam(outputArray):
    outputFile = "{}/medaka_output".format(fastqPath)
    if not os.path.exists(outputFile):
        os.mkdir(outputFile)
    for i, outf in enumerate(outputArray):
        with open("{}/{}.bam".format(outputFile, str(files[i])[:-6]), 'wb') as f:
            if len(outf) > 0:
                f.write(outf)
                #print (outf)


def medaka_process():

    with closing(Pool(processes=cores)) as pool:
        outputBam = pool.map(partial(minimap_samtools_command_for_medaka, iteration=n), files, 1)
        pool.terminate()
    write_files_bam(outputBam)

    with closing(Pool(processes=cores)) as pool:
        outputBam = pool.map(samtools_command_for_medaka, files, 1)
        pool.terminate()
    #write_files_bam(outputBam)

    #with closing(Pool(processes=int(cores/2))) as pool:
    with closing(Pool(processes=5)) as pool:
        outputMedaka = pool.map(medaka_consensus_command, files, 1)
        pool.terminate()

    with closing(Pool(processes=cores)) as pool:
        outputMedaka = pool.map(medaka_stich_command, files, 1)
        pool.terminate()

def process():
    global cores
    cores = cpu_count()
    get_fastqFiles()

    outputMinmap = []
    outputRacon = []

    for iteration in range(0, n):
        with closing(Pool(processes=cores)) as pool:
            outputMinmap = pool.map(partial(minimap_command,iteration=(iteration+1)), files, 1)
            pool.terminate()
        write_files_minimap(outputMinmap, iteration+1)

        with closing(Pool(processes=cores)) as pool:
            outputRacon = pool.map(partial(racon_command,iteration=(iteration+1)), files, 1)
            pool.terminate()
        write_files_racon(outputRacon, iteration+1)

    medaka_process()


read_config_file()
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-q":
            fastqPath = sys.argv[i + 1]
        elif sys.argv[i] == "-r":
            referencePath = sys.argv[i + 1]
        elif sys.argv[i] == "-n":
            n = int (sys.argv[i + 1])
        elif sys.argv[i] == "-m":
            medaka_model = sys.argv[i + 1]

    start_time = time.time()
    process()
    write_medaka_consensus_file(combine_outputs())
    print("--- %s seconds ---" % (time.time() - start_time))
else:
    print (""" 
	No arguments given
        
        python protocol.py [Arguments]
        
        Arguments:
        -q fastq files
        -r reference
	-n number of iterations [Default 1]
	-m model for medaka [Default r941_min_high]       
""")
