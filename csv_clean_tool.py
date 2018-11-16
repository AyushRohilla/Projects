import re, sys, time, gzip
from time import gmtime, strftime

filetype = input("Enter filetype: ")

#Function 1 : for reading file
def readFile(inputfile, filetype):
    curtime=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if(filetype=="CSV" or filetype=="TXT" or filetype=="csv" or filetype=="txt"):
        try:
            file = open(inputfile,"r")
        except IOError as e:
            print(curtime+" ERROR! reading file. "+inputfile)
            sys.exit(1)
    elif(filetype=="GZ"):
        try:
            file = gzip.open(inputfile,"rb")
        except IOError as e:
            print(curtime+" ERROR! reading file. "+inputfile)
            sys.exit(1)
    else:
        print(curtime+" ERROR! Unknown Filetype. "+inputfile)
        sys.exit(1)
    return file
#--------------------------------
#Function 2 : for writing into file. 32768 is buffer size.
def writeFile(outputfile, filetype):
    curtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if(filetype=="CSV" or filetype=="TXT" or filetype=="csv" or filetype=="txt"):
        try:
            file = open(outputfile, "w", 32768)
        except IOError as e:
            print(curtime+" ERROR! writing File. "+outputfile)
            sys.exit(1)
    elif(filetype=="GZ"):
        try:
            file = gzip.open(outputfile, "wb")
        except IOError as e:
            print(curtime+" ERROR! writing File. "+outputfile)
            sys.exit(1)
    else:
        print("ERROR! Unknown Filetype. "+outputfile)
        sys.exit(1)
    return file
#--------------------------------
#Function 3 : for removing non ASCII characters.
def rmNoASCII(parameters=[], *args):
    line = parameters[0]
    regex = re.compile(r"[\x80-\xFF]")
    newRegex = re.sub(regex, " ", line)
    return newRegex
#--------------------------------
#Function 4 : for removing all Backslashes, inverted commas and invalid separator.
def rmBackslashCommas(parameters=[], *args):
    line = parameters[0]
    separator = parameters[2]
    if(separator is not None):
        regex = re.compile(r"([\\]) (?=([\"]) (?=([" + re.escape(separator) + "])))")
        newRegex = re.sub(regex, "", line)
    else:
        newRegex = line
    return newRegex

#--------------------------------
#Function 5 : for removing Backslash.
def rmBackslash(parameters=[], *args):
    line = parameters[0]
    regex = re.compile(r"[\\]")
    newRegex = re.sub(regex, "", line)
    return newRegex
#--------------------------------
#Function 6 : for removing CRLF from specific lines \n and \r both.
def rmCRLFboth(parameters=[], *args):
    line = parameters[0]
    line_no = parameters[1]
    lineList = parameters[3]
    newRegex = line
    if(lineList is not None):
        regex = re.compile(r"(\r)(\n)")
        if((line_no+1) in lineList):
            newRegex = re.sub(regex, "", line)
    return newRegex
#Function 7 : for removing CRLF from specific lines \r only.
def rmCRLFr(parameters=[], *args):
    line = parameters[0]
    line_no = parameters[1]
    line_list = parameters[3]
    newRegex = line
    if(line_list is not None):
        regex = re.compile(r"(\r)")
        if((line_no+1) in line_list):
            newRegex = re.sub(regex, "", line)
    return newRegex
#Function 8 : for removing LF from specific lines \n only.
def rmCRLFn(parameters=[], *args):
    line = parameters[0]
    line_no = parameters[1]
    line_list = parameters[3]
    newRegex = line
    if(line_list is not None):
        regex = re.compile(r"(\n)")
        if((line_no+1) in line_list):
            newRegex = re.sub(regex, "", line)
    return newRegex
#Function 9 : for removing all CR characters not followed by LF.
def rmCRnoLF(parameters=[], *args):
    line = parameters[0]
    regex = re.compile(r"\r[^\n]")
    regexm = re.compile(r"^[\r]",re.MULTILINE)
    first_new_regex = re.sub(regex, r"",line)
    newRegex = re.sub(regexm, r"",first_new_regex)
    return newRegex
#Function 10 : for removing all LF characters not preceeded by CR
def rmLFnoCR(parameters=[], *args):
    line = parameters[0]
    regex = re.compile(r"([^\r])(\n)")
    regexm = re.compile(r"^[\n]",re.MULTILINE)
    first_new_regex = re.sub(regex, r"\1", line)
    newRegex = re.sub(regexm, r"", first_new_regex)
    return newRegex
#Function 11 : for removing LF characters not preceeded by ""
def rmLFnoQuotes(parameters=[], *args):
    line = parameters[0]
    regex = re.compile(r"([^\"|])(\n)")
    regexm = re.compile(r"^[\n]",re.MULTILINE)
    first_new_regex = re.sub(regex, r"\1", line)
    newRegex = re.sub(regexm, r"", first_new_regex)
    return newRegex
#Function 12 : for removing all CR characters
def rmCR(parameters=[], *args):
    line = parameters[0]
    regex = re.compile(r"[\r]")
    newRegex = re.sub(regex, r" ",line)
    return newRegex
#End of functions-------------------------------
#Initializing list
parameters = [None]*10
InErr = 0
Row_List = False
Separator_val = False
num_pattern = re.compile(r"[^0-9]")
pattern_1 = re.compile(r"([|])\1+")
pattern_2 = re.compile(r"(^[|])|([|]$)")
#Buffer size
buffer_size = 200000
#args[6]
try:
    curtime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    print(curtime+" Filetype is: "+filetype)
except IndexError as e:
    curtime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    print(curtime+" ERROR! void filetype "+filetype)
    filetype = None
#args[1]
#args[2]
try:
    input_file = input("Enter the filename: ")
    filein = readFile(input_file, filetype)
    try:
        output_file = input("Enter the name of output file: ")
        if(input_file==output_file):
            output_file_name = str(output_file)+".clean"
        else:
            output_file_name = str(output_file)
        fileout = writeFile(output_file_name, filetype)
    except IndexError as e:
        curtime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
        print(curtime+" ERROR! Output File not provided. ")
except IndexError as e:
    curtime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    print(curtime+" ERROR! input file not provided. ")
#Separator
Separator = input("Enter the separator: ")
if(Separator):
    parameters[2]=Separator
    Separator_val=True
#List of cleaning options
print("\nPress following to remove:\n1. Non ASCII chars.\n2. Back Slashes,commas and separator.\n3. Backslash.\n4. CRLF both.\n5. CRLF 'r' only.")
print("6. CRLF 'n' only.\n7. Chars not followed by LF chars.\n8. LF not preceeded by CR chars.\n9. LF chars not preceeded by quotes.\n10. All CR chars.")
cleanOptionsArray=("rmNoASCII","rmBackslashCommas","rmBackslash","rmCRLFboth","rmCRLFr","rmCRLFn","rmCRnoLF","rmLFnoCR","rmLFnoQuotes","rmCR")

choice=input()
if choice==1:
    CleanValue=cleanOptionsArray[0]
elif choice==2:
    CleanValue=cleanOptionsArray[1]
elif choice==3:
    CleanValue=cleanOptionsArray[2]
elif choice==4:
    CleanValue=cleanOptionsArray[3]
elif choice==5:
    CleanValue=cleanOptionsArray[4]
elif choice==6:
    CleanValue=cleanOptionsArray[5]
elif choice==7:
    CleanValue=cleanOptionsArray[6]
elif choice==8:
    CleanValue=cleanOptionsArray[7]
elif choice==9:
    CleanValue=cleanOptionsArray[8]
elif choice==10:
    CleanValue=cleanOptionsArray[9]
else:
    print("Please enter valid option.")
    

cleaningParams = re.sub(pattern_2,"",re.sub(pattern_1,"|",CleanValue))
cleaningList = cleaningParams.split("|")
i = 0
while i < len(cleaningList):
    cleaningList[i] = cleaningList[i].upper()
    i = i + 1



#List of specific line numbers 
if(str(1)):
    rowsNums = re.sub(pattern_2,"",re.sub(pattern_1,"|",re.sub(num_pattern,"",str(1))))
    if(rowsNums):
        line_list = [int(n) for n in rowsNums.split("|")]
        parameters[3]=line_list
        Row_List=True
    else:
        curtime=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print (curtime+"-WARN- CSVCleanTool - No right line numbers provided")

start_time=time.time()
#------------------
"""j=0
while (j < len(cleaningList)):
    cleanOpt=cleaningList[j]
    print("Clean Opt is: ",cleanOpt)
    if (cleanOpt not in cleanOptionsArray):
        cleaningList.pop(j)
        j=j-1
    j=j+1"""
print("Used option is: ",cleaningList)
#------------------
for index, line in enumerate(filein):
    parameters[0]=line
    parameters[1]=index 
    wline=line
    lineBuffer=""
    counter=0
    for cleanOpt in cleaningList:
        wline= (eval(CleanValue)(parameters))  #cleaningOptions[cleanOpt](paramsList)
        parameters[0]=wline
        counter = counter + 1
    lineBuffer=lineBuffer+wline
    if(counter==buffer_size):
        fileout.write(lineBuffer)
        lineBuffer=""
        counter=0
    fileout.write(lineBuffer)
elapsed_time = time.time() - start_time
curtime=strftime("%Y-%m-%d %H:%M:%S", gmtime())
print (curtime+"-INFO- CSVCleanTool - CSVCleanTool took "+str(elapsed_time)+" seconds.")


filein.close()
fileout.close()
