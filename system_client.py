import sys
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
print("\n")
print("-----raw system argument-----")
print sys.argv
print("-----raw system argument-----")
print("\n")
print("-----sliced system argument-----")
print(sanitizedInput)
print("-----sliced system argument-----")
print("\n")
if sanitizedInput[0] == 'help':
        print("-----current commands available-----")
        print("help --> display all commands") 
        print("send --> send file specified in argument")
        print("-----current commands available-----")
print("\n")
elif sanitizedInput[0] == 'send':
        pass


        
