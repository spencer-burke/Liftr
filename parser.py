class Parser(object):
    #boolean for print statements
    debugMode = False
    #current command that the parser needs to analyze
    currentCommand = []
    #list of commands currently available
    commandList = ['send','display','help']
    #"constructor" for the Parser object
    #flag is the word to invoke commands
    def __init__(self, flag):
        self.FLAG = flag
    #breaks entered command into parts with a white space delimeter
    def parseString(self, arg): 
            if(len(self.currentCommand) >= 2 and self.currentCommand[0] == self.FLAG):
                #returns "send" and tells the client to send files
                if(self.currentCommand[1] == self.commandList[0]):
                        if(self.isInDebugMode == True):
                                print("Item in command list " + commandList[0] + "send command detected")
                        return self.commandList[0]
                #returns "display" and tells the client to display all the files
                if(self.currentCommand[1] == self.commandList[1]):
                        if(self.isInDebugMode == True):
                                print("Item in command list " + commandList[1] + "display command detected")
                        return self.commandList[1]
                #returns "help" and tells the client to display all of the commands
                if(self.currentCommand[1] == self.commandList[2]):
                        if(self.isInDebugMode == True):
                                print("Item in command list " + commandList[2] + "display command detected")
                        return self.commandList[2]
    #updates the current command
    def update(self, arg): 
           self.currentCommand.append(arg)
    #enables debug mode
    def enableDebugMode(self):
           self.debugMode = True
    #disables debug mode
    def disableDebugMode(self):
           self.debugMode = False
    #returns the status of debugMode
    def isInDebugMode(self):
            return self.debugMode
