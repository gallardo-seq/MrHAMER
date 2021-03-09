import gzip
from re import findall
Pads = ['S', 'H']
Bases = ['A','T','G','C']
import numpy as np

def Chunks(l, n):
    #l is list
    #n is chunksize.
    for i in range(0, len(l), n):
        yield l[i:i + n]

def FindNuc(line, Coords):
    Output = []
    Read = line[9]
    CurrPosition = int(line[3])
    Cigar = list(Chunks(findall(r"[^\W\d_]+|\d+", line[5]), 2))
    #print Cigar
    #while CurrPosition < cfg.NtFinish:
    if Cigar[0][1] in Pads:
        #Remove 5' pad:
        Read = Read[int(Cigar[0][0]):]
        ##Don't correct position, as position is reported from first mapped Nt, not including Pad
        ##Position = str(int(Position) + int(Cigar[0][0]))
        Cigar = Cigar[1:]
    else:
        #No 5' Pad
        pass
    for i in Cigar:
        if i[1] == 'D' or i[1] == 'N':
                #"D" or "N" is a deletion: 
                for n in range(int(i[0])):
                    Coord = CurrPosition + n
                    if Coord in Coords:
                        Output.append([Coord, '*'])
                    else:
                        pass
                    #print [Coord, '*']
                CurrPosition += int(i[0])
                #Don't change Read
        elif i[1] == 'I':
                #"I" is an insertion 
                Insertion = Read[:int(i[0])]
                for n in range(int(i[0])):
                    if CurrPosition in Coords:
                        Output.append([str(Coord) + 'I', Insertion[n]])
                    else:
                        pass
                    #print [Coord, [Coord, 'I' + Insertion[n]]]
                Read = Read[int(i[0]):]
                #Don't change Ref Position
        elif i[1] == 'M':
                #"M"
                Segment = Read[:int(i[0])]
                Read = Read[int(i[0]):]
                for n in range(int(i[0])):
                    Coord = CurrPosition + n
                    if Coord in Coords:
                        Output.append([Coord, Segment[n]])
                    else:
                        pass
                    #print [Coord, Segment[n]]
                CurrPosition += int(i[0])
        else:
                pass
    return Output

def RemakeTag(Output):
    Tag = ''
    for i in Output:
        if i[1] in Bases:
            Tag += i[1]
    return Tag
    
Coords1 = range(316, 330, 1)
Coords2 = range(4459, 4473, 1)

Tags1 = {}
Tags2 = {}

Dict = {}
Input = '/home/torbett-seq/Desktop/Shiyi/Template_Switch_Plasmid/b4consensus_2.sam.gz'
print Input
with gzip.open(Input) as In:
    Data = In.readline()
    while Data:
        Data = Data.split()
        if Data[1] == '0':
            Name = Data[0]
            Tag1 = FindNuc(Data, Coords1)
            Tag1 = RemakeTag(Tag1)
            Tag2 = FindNuc(Data, Coords2)
            Tag2 = RemakeTag(Tag2)
            if Tag1 in Tags1:
                Tags1[Tag1] += 1
            else:
                Tags1[Tag1] = 1
            if Tag2 in Tags2:
                Tags2[Tag2] += 1
            else:
                Tags2[Tag2] = 1
            Dict[Name] = [Tag1,Tag2]
        Data = In.readline()

T1A = 'CAGATCC'
T1B = 'AAATATA'
T2A = 'GAAGAAAA'
T2B = 'AGGAGTGG'
T2B2 = 'AAAGGTGG'

def Distance(Query, Ref):
    Alts = ['A','T','C','G', '']
    Count = 0
    if Query in Ref:
        return Count
    else:
       # count = 0
        #if len(Query) == len(Ref):
        for i in range(len(Query)):
            for j in Alts:
                NewQuery = Query[:i] + j + Query[i+1:]
                if NewQuery in Ref:
                    Count = 1
    #elif len(Query) == len(Ref) - 1:
        for i in range(len(Query)):
            for j in Alts[:-1]:
                NewQuery = Query[:i] + j + Query[i:]
                if NewQuery in Ref:
                    Count = 1
    #elif len(Query) == len(Ref) + 1:
        for i in range(len(Query)):
            for j in Alts[:-1]:
                NewQuery = Query[:i] + Query[i+1:]
                if NewQuery in Ref:
                    Count = 1
    if Count:
        return Count
    else:
        return 2
        
    
Coords = [T1A, T1B, T2A, T2B]
        
Array = [0,0,0,0] ##[T1A, T1B, T2A, T2B]
#for i in Dict: 
#    if T1A in Dict[i][0] and T2A in Dict[i][1]:
#        Array[0] += 1
#    elif T1B in Dict[i][0] and T2A in Dict[i][1]:
#        Array[1] += 1
#    if T1A in Dict[i][0] and T2B in Dict[i][1]:
#        Array[2] += 1
#    elif T1B in Dict[i][0] and T2B in Dict[i][1]:
#        Array[3] += 1
for i in Dict: 
    if Distance(T1A, Dict[i][0]) <= 1 and Distance(T2A, Dict[i][1]) <= 1:
        Array[0] += 1
    elif Distance(T1B, Dict[i][0]) <= 1 and Distance(T2A, Dict[i][1]) <= 1:
        Array[1] += 1
    if Distance(T1A, Dict[i][0]) <= 1 and Distance(T2B, Dict[i][1]) <= 1:
        Array[2] += 1
    elif Distance(T1A, Dict[i][0]) <= 1 and Distance(T2B2, Dict[i][1]) <= 1:
        Array[2] += 1
    elif Distance(T1B, Dict[i][0]) <= 1 and Distance(T2B, Dict[i][1]) <= 1:
        Array[3] += 1
    elif Distance(T1B, Dict[i][0]) <= 1 and Distance(T2B2, Dict[i][1]) <= 1:
        Array[3] += 1
        
print Array
TSrate = (Array[1] + Array[2]) / float(Array[0] + Array[3])

print 'Template Switching rate =', TSrate
        
        
        
        
        
        
        
