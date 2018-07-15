import sys
from parser import Parser
#make the parser object
parserObject = Parser("liftr")

#cleans the input of the name of the program
def cleanInput(list_arg):
        result = []
        i = 0
        while i < len(sys.argv):
                if i > 0:
                        result.append(sys.argv[i])
                i+=1
        return result

sanitizedInput = cleanInput(sys.argv)
print("-----raw system argument-----")
print sys.argv
print("-----raw system argument-----")
print("\n")
print("-----sliced system argument-----")
print(sanitizedInput)
print("-----sliced system argument-----")
parserObject.currentCommand = sanitizedInput
currentCommand = parserObject.parseString(sanitizedInput)
print("current command --> {0}".format(currentCommand))
if currentCommand == 'help':
        print("-----current commands available-----")
        print("help --> display all commands")
        print("display --> display all files in the liftr directory")
        print("send --> send file specified in argument")
        print("-----current commands available-----")


