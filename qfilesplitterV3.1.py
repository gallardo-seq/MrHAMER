import os
import time
import sys


#inputFile = "porechop.fastq"
inputFile = "porechop.test.fastq"
outputFile = "./"
blockSize = 0
file_type = ""

def get_identifier(block):
        ids = 0
        ide = block.find(' runid', ids)
        if ide > 0 and  ide < 50:
            return block[ids:ide].split('_')[0][1:]

def get_identifier_fasta(block):
    header = block.split('\n')[0]
    header = header.replace(';','')
    id_index = header.find(' ')
    if(id_index == -1):
        id_index = len(header)
    #print("header:{}; index {} ".format(header, id_index))
    return block[1:id_index].split('_')[0]

def create_output_folder():
    global outputFile
    outputFile = "{}output/".format(outputFile)
    if not os.path.exists(outputFile):
        os.mkdir(outputFile)

def test_block(block):
    #print "Block Test"
    lines = block.split('\n')
    if len(lines)==5:
        if "runid" in lines[0] and "sampleid" in lines[0] and "read" in lines[0]:
            if len(lines[1]) == len(lines[3]):
                return False
            else:
                print (lines[0])
                print ("Error: lengths doesn't match")
        else:
            print (lines[0])
            print("Error: Bad Identifier")
    else:
        print (lines[0])
        print ("Error: Block with wrong format")
    return True

def process_block_fastaq(block):
    if test_block(block):
        return "Error"

    identifier = get_identifier(block)

    if identifier in identifiers.keys():
        identifiers[identifier] += block
        identifiers_blockCount[identifier] += 1
    else:
        identifiers[identifier] = block
        identifiers_blockCount[identifier] = 1


def process_block_fasta(block):
    identifier = get_identifier_fasta(block)
   # print("Processign block:{} \n {}".format(identifier,block))
    #print("Processign block:{} ".format(identifier))
	
    if identifier in identifiers.keys():
        identifiers[identifier] += block
        identifiers_blockCount[identifier] += 1
    else:
        identifiers[identifier] = block
        identifiers_blockCount[identifier] = 1


def save_files():
    create_output_folder()
    for id, value in identifiers.items():
        print id, identifiers_blockCount[id]
        if identifiers_blockCount[id] >= int(blockSize):
            with open("{1}{0}.{2}".format(id, outputFile, file_type), 'w') as f:
                f.write(value)


def split_operation():
    block = ""
    totLines = 0
    with open(inputFile) as infile:
        for line in infile:
            totLines += 1
	    identify_file_type(line)
	    if file_type == "fastq":
               if line[0] == '@' and "runid" in line:
                   if block == "":
                       block += line
                   else:
                       process_block_fastaq(block)
                       block = line
               else:
                   block += line
	    elif file_type == "fasta":
                if line[0] == '>':
			if block == "":
				block += line
			else:
				process_block_fasta(block)
				block = line
   #                             print ("*****************")
   #                             print(block)
   #                             exit() 
		else:
			block += line
	
			
        if file_type == "fastq":
		process_block_fastaq(block)
        elif file_type == "fasta":
		process_block_fasta(block)
    print("Lines found:{}".format(totLines))
    save_files()


def identify_file_type(line):
	global file_type
	if file_type == "":
		if line[0] == '@' and "runid" in line:
			file_type = "fastq"
                        print("File type:{}".format(file_type))
		elif line[0]== '>':
			file_type = "fasta"
                        print("File type:{}".format(file_type))
		else:
			file_type = "Error"
                        print("File type:{}".format(file_type))


start_time = time.time()
identifiers = {}
identifiers_blockCount = {}
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-i":
            inputFile = sys.argv[i+1]
        elif sys.argv[i] == "-o":
            outputFile = sys.argv[i + 1]
        elif sys.argv[i] == "-b":
            blockSize = sys.argv[i + 1]
    split_operation()
else:
    print """ 
        No arguments given
        
        python qfilespliter.py [Arguments]
        
        Arguments:
        -i input file
        -o output path
        -b blocks size cutoff [optional]
    """

print("--- %s seconds ---" % (time.time() - start_time))
