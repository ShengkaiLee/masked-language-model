binary_name = ""

def removeDuplicateSpace(theStr):
    spaceFlag = 0
    result = ''
    for i in theStr:
        if i == ' ':
            if (not spaceFlag):
                result += i
                spaceFlag = 1
        elif i == '\n':
            if (not spaceFlag):
                result += ' '
                spaceFlag = 1
        elif i != ' ':
            result += i
            spaceFlag = 0
    return result

def saveFunctionInstr(FuncInstr, directory):

    funName = directory+"assembly/"+FuncInstr[0][18:-3]+'.assembly'+"."+binary_name
    if(funName[:2] == "__"):
        return
    result = ""
    for i in FuncInstr[1:]:
        instr = i.split('\t')[1] # take only hex represented instructions
        result += instr
    result = removeDuplicateSpace(result)
    with open(funName,'w') as f:
         f.write(result)
         print(funName)
         f.close()
    return

def parseFileAssembly(filename, directory):
    with open(filename,'r', errors='ignore') as f:
        Lines = f.readlines()
        parsingFlag = 0
        FuncInstr = []
        for line in Lines:
            if("Disassembly of section" in line):
                if('.text' in line): # only parse .text section. expect no other sections, but if has, skip.
                    parsingFlag = 1
                    continue
                else:
                    parsingFlag = 0
            if(not parsingFlag):
                continue
            
            if((line == Lines[-1]) and (line != '\n')): # in case last line is not \n
                FuncInstr.append(line)
                line = '\n'

            if('\n' == line):
                if(len(FuncInstr) <= 1):
                    continue
                saveFunctionInstr(FuncInstr, directory)
                FuncInstr = []
                parsingFlag = 0
            else:
                FuncInstr.append(line)
        f.close()
    return

def assemblyParsing_main(filename):
    ret = dict()
    to_remove = set()
    with open(filename,'r', errors='ignore') as f:
        Lines = f.readlines()
        parsingFlag = 0
        FuncInstr = []
        for idx, line in enumerate(Lines):

            if("Disassembly of section" in line):
                if('.text' in line): # only parse .text section. expect no other sections, but if has, skip.
                    parsingFlag = 1
                    continue
                else:
                    parsingFlag = 0
            if(not parsingFlag):
                continue
            
            if((idx == len(Lines) - 1) and (line != '\n')): # in case last line is not \n
                FuncInstr.append(line)
                line = '\n'

            if('\n' == line):
                if(len(FuncInstr) <= 1):
                    continue
                funName = FuncInstr[0][18:-3]
                result = ""
                for i in FuncInstr[1:]:
                    instr = i.split('\t')[1] # take only hex represented instructions
                    result += instr
                result = removeDuplicateSpace(result)
                if ret.get(funName, None) is not None:
                    to_remove.add(funName)
                ret[funName] = result
                FuncInstr = []
                parsingFlag = 0
            else:
                FuncInstr.append(line)
        f.close()
    for key in to_remove:
        ret.pop(key, None)
    return ret


import sys
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 assemblyParsing.py filePath fileSaveDir")
    else:
        binary_name = (sys.argv[1].split("/"))[-1]
        parseFileAssembly(sys.argv[1], sys.argv[2])
