# Modify line 260 and 335 if this doesn't work.
import tkinter as tk
import tkinter.font as ft
import numpy as np
import random
import matplotlib.pyplot as plt
####################preWindow#################################################
'''
preWindow is to choose between the three modes:
                    2-player
                    1-player with pretrained weights, instantiating and passing an aiAgent
                    1-player with initial weights, " "
An aiAgent is passed to preWindow so that it can pass it to the single-player games.
'''
class preWindow:
    def __init__(self):

        self.title = "AKB's Tic-Tac-Toe with Basic RL" # Hyperparameters
        self.buttonWidth = 35
        self.buttonHeight = 5
        self.labelText = "This is an implementation of \nthe algorithm described in\n the first chapter of \nReinforcement Learning: An Introduction\n by Sutton and Barto.\nModify lines 260 and 335\nbefore you begin."

        self.window = tk.Tk() # Create the window
        self.window.title(self.title)
        self.mainFrame = tk.Frame(self.window)
        self.mainFrame.grid(row = 0, column = 0)

        self.buttons = [] # The three buttons
        self.buttons.append(tk.Button(self.mainFrame, text = "Single-Player (pretrained)", command = lambda : self.initializeGame(players = 1, train = False), height = self.buttonHeight, width = self.buttonWidth))
        self.buttons.append(tk.Button(self.mainFrame, text = "Single-Player (training mode)", command = lambda : self.initializeGame(players = 1, train = True), height = self.buttonHeight, width = self.buttonWidth))
        self.buttons.append(tk.Button(self.mainFrame, text = "Two-Player", command = lambda: self.initializeGame(players = 2, train = False), height = self.buttonHeight, width = self.buttonWidth))

        for i in range(len(self.buttons)): #Grid the buttons
            self.buttons[i].grid(row = i, column = 0)

        self.label = tk.Label(self.mainFrame, text = self.labelText) # Label for helpful info
        self.label.grid(row = 0, column = 1, rowspan = 3)

        self.window.mainloop() # Run the window

    def initializeGame(self, players, train): #Game initializer
        self.window.destroy()
        if(players == 1):
            onePlayerGame(0, None, train, True)
        elif(players == 2):
            twoPlayerGame(0)
####################preWindow#################################################

#####CHECKPOINT 22:38:9.5.2020 ########################################################################
###################cell#######################################################

class cell:
    def __init__(self, board, row, column, width = 3, height = 1):
        self.board = board
        self.row = row
        self.column = column
        self.button = tk.Button(self.board.root, text = '', width = width, height = height, command = lambda : self.board.click(row, column))
        self.button.grid(row = self.row, column = self.column)
        self.active = True
        self.button['font'] = ft.Font(size = 50)
    def overwrite(self, actorID):
        if(actorID == 0):
            self.button['text'] = 'X'
        else:
            self.button['text'] = 'O'
    def invoke(self):
        self.button.invoke()
#####CHECKPOINT 23:15:9.5.2020 ########################################################################

###################cell#######################################################
###################twoPlayerGame##################################################


'''
twoPlayerGame implements the following:
Grid label reset mainmenu
1) The board itself: Consisting of:
    i)      A top-level window.
    ii)     A flag gameStateFlag, describing if anyone has won or if the game is drawn.
    iii)    An array gameStateArray, describing the state of each square in ttt game.
    iv)     A flag actorID, describing whose move it is.
    v)      A label which tells us whose move it is / if a player has won/drawn.
    vi)     A reset button, which when pressed, resets the board and starts a fresh game, and reset = 0.
    vii)    A main menu button, which when pressed, stops the game and calls preWindow.
    viii)   A 3x3 grid of buttons, called gameButtons.
            a)  gameButtons are initially blank.
            b)  when a gameButton is clicked:
                    i)      If the gameButton has already been pressed, do nothing.
                    ii)     If the gameButton has not yet been pressed:
                                a)  If the actorID is 0, change the label to X.
                                b)  If the actorID is 1, change the label to O.
                    iii)    Update the board states array and swap the actorID.
                    iv)     Call the gameState evaluator.
                                0) Irrespective of win/draw/loss, toggle the actorID.
                                a) Call the winChecker function.
                                b) If actor0 has won, print this and deactivate all gameButtons.
                                c) If actor1 has won, print this and deactivate all gameButtons.
                                d) If neither actor has won, but all buttons are deactivated, print draw.
'''

class twoPlayerGame:
    ##### INITIAL SETUP ######################################################
    def __init__(self, gameNumber):

        self.title = "AKB's Tic-Tac-Toe"
        self.root = tk.Tk() #Initialize the window
        self.root.title(self.title)

        self.gameStateArray = np.zeros((3, 3)) # Stores the state of the buttons, 3x3
        self.buttons = [] # Stores the 3x3 grid of buttons

        # Initialize buttons and gameStateArray
        for i in range(3):
            self.buttons.append([])
            for j in range(3):
                self.buttons[i].append(cell(self, i, j))

        self.gameStateFlag = 0 # 0 : P1 to play, 1: P2 to play, 2: P1 wins, 3: P2 wins, 4: draw
        self.actorID = 0 # Who is to play

        #Label describing the state of the game
        self.gameStateTexts = ["Player 1 to play.", "Player 2 to play.", "Player 1 wins.", "Player 2 wins.", "Draw."]
        self.gameStateLabel = tk.Label(self.root, text = self.gameStateTexts[0])
        self.gameStateLabel.grid(row = 3, column = 0, columnspan = 3)

        # To reset the game
        self.resetButton = tk.Button(self.root, text = "Reset", command = self.reset)
        self.resetButton.grid(row = 4, column = 0)

        # To go back
        self.mainMenuButton = tk.Button(self.root, text = "Main Menu", command = self.mainmenu)
        self.mainMenuButton.grid(row = 4, column = 2)

        #How many games have been played so far?
        self.gameNumber = gameNumber
        self.gameNumberLabel = tk.Label(self.root, text = "Game number " + str(self.gameNumber) + ".")
        self.gameNumberLabel.grid(row = 5, column = 0, columnspan = 3)

    ##### INITIAL SETUP ######################################################
    ##### HELPER FUNCTIONS ###################################################
    def reset(self): # To reset the game
        self.root.destroy()
        self.__init__(self.gameNumber + 1)

    def mainmenu(self): # To go back to the main menu
        self.root.destroy()
        preWindow()

    def updateLabel(self): # Change the text of the label
        self.gameStateLabel['text'] = self.gameStateTexts[self.gameStateFlag]

    def updateGameStateArray(self, row, column): #Update the state of the game
        if(self.actorID == 0):
            self.gameStateArray[row][column] = 1
        elif(self.actorID == 1):
            self.gameStateArray[row][column] = -1

    def hasActorWon(self, gameStateArray, actorID):
        hasWon = False

        if(actorID == 0):
            toCheck = 1
        else:
            toCheck = -1

        #Rows and columns:
        for i in range(3):
            rowsum = np.sum(gameStateArray[i, :])
            colsum = np.sum(gameStateArray[:, i])
            if (rowsum == 3*toCheck or colsum == 3*toCheck):
                hasWon = True
        #Diagonals:
        d1sum = gameStateArray[0][0] + gameStateArray[1][1] + gameStateArray[2][2]
        d2sum = gameStateArray[2][0] + gameStateArray[1][1] + gameStateArray[0][2]
        if(d1sum == 3*toCheck or d2sum == 3*toCheck):
            hasWon = True
        return hasWon

    def updateGameStateFlag(self):
        # 0 : P1 to play, 1: P2 to play, 2: P1 wins, 3: P2 wins, 4: draw
        hasWon = self.hasActorWon(self.getGameStateArray(), self.actorID)
        if(hasWon):
            # 0 : P1 to play, 1: P2 to play, 2: P1 wins, 3: P2 wins, 4: draw
            if(self.actorID == 0):
                self.gameStateFlag = 2
            elif(self.actorID == 1):
                self.gameStateFlag = 3
        else:
            isFull = True
            for i in range(3):
                for j in range(3):
                    if(self.gameStateArray[i][j] == 0):
                        isFull = False
            if(isFull):
                self.gameStateFlag = 4
            else:
                self.gameStateFlag = (self.actorID + 1)%2

    def getGameStateArray(self):
        return np.copy(self.gameStateArray)

    def getGameStateFlag(self):
        return self.gameStateFlag
    def getButton(self, i, j):
        return self.buttons[i][j]
    ##### HELPER FUNCTIONS ###################################################
    #####CLICK FUNCTION ######################################################

    def click(self, row, column): # Process a click of one of the boxes
        '''
        i)      If the gameButton has already been pressed, do nothing.
        ii)     If the gameButton has not yet been pressed:
                    a)  If the actorID is 0, change the label to X.
                    b)  If the actorID is 1, change the label to O.
                    iii)    Update the board states array.
                    iv)     Call the gameState evaluator.
                        a) Call the winChecker function.
                        b) If actor0 has won, print this and deactivate all gameButtons.
                        c) If actor1 has won, print this and deactivate all gameButtons.
                        d) If neither actor has won, but all buttons are deactivated, print draw.
                        e) Swap the actorID.
        '''
        if(self.gameStateArray[row][column] == 0 and (self.gameStateFlag == 0 or self.gameStateFlag == 1)): # ii)
            self.buttons[row][column].overwrite(self.actorID) #ii)
            self.updateGameStateArray(row, column) #iii)
            self.updateGameStateFlag()
            self.gameStateLabel['text'] = self.gameStateTexts[self.gameStateFlag]
            self.actorID = (self.actorID + 1)%2

    #####CLICK FUNCTION ######################################################

###################twoPlayerGame##################################################
###################onePlayerGame##################################################
'''
onePlayerGame has an AI agent (lol) for actor1.
There a train flag and a reset flag which is passed through the constructor.
If reset == True, aiAgent.reset(train) is called.
If reset == False, do nothing.
There is also a difference in the gameState evaluator.
Apart from the other functions as described in gameBoard,
    a)  If actorID == 1:
        call the aiStep method of the aiActor to obtain the next move, passing the gameStateArray.
        Based on the result of the aiStep method, generate the appropriate event designating the click
When the reset button is pressed, pass the aiAgent along to the new game. reset = 0
'''
class onePlayerGame(twoPlayerGame):
    def __init__(self,gameNumber, ai, train, resetPin):
        super().__init__(gameNumber)
        if(ai is None):
            ai = aiAgent(self, train)
        self.ai = ai
        self.ai.setGameBoard(self)
        if(resetPin):
            self.ai.hardReset()
        else:
            self.ai.softReset()

        self.saveRewards = tk.Button(self.root, text = "Save rewards table", command = self.save)
        self.saveRewards.grid(row = 4, column = 0, columnspan = 3)
        self.savePath = "C:/Users/aniru/Desktop/output.csv"
    def save(self):
        rewardsDict = self.ai.aiRewards
        with open(self.savePath, "w") as file:
            for i in rewardsDict.keys():
                file.write(i + "," + str(rewardsDict[i]) + "\n")

    def reset(self):
        self.root.destroy()
        onePlayerGame(self.gameNumber + 1,self.ai, self.ai.train, False)

    def click(self, row, column):
        super().click(row, column)
        if(self.actorID == 1):
            self.ai.step()
###################onePlayerGame##############################################
###################aiAgent####################################################
'''
    Contains a dictionary of states (string) to rewards (float).
    A currstate which is a string designating the current state.
    a) __init__(train, epsilon = 0.1, path = ):
            instantiate the dictionary of states using the dictInit method, remembering to read from the appropriate .csv
    b) aiStep(nextStateArray, nextStateFlag):
        i)  nextState is a 2D array. First, we convert it to a string by calling stateString.
        ii) if nextStateFlag designates a win/loss, update rewards[currstate] accordingly.
        iii)if nextStateFlag designates a continuation,
'''
class aiAgent:
    def __init__(self,gameBoard, train, epsilon = 0.1, alpha = 0.1, dictPath = "dict_trained.csv"):
        self.setGameBoard(gameBoard)
        self.train = train
        self.epsilon = epsilon
        self.alpha = alpha
        self.dictPath = dictPath
        self.hardReset()

    def setGameBoard(self, gameBoard):
        self.gameBoard = gameBoard

    def softReset(self):
        self.prevStateArray = np.zeros((3, 3))
        self.gameEnded = False
    def hardReset(self):
        self.softReset()
        if(self.train):
            self.aiRewards = self.defaultRewards()
        else:
            self.aiRewards = self.loadRewards()

    def defaultRewards(self):
        print("Loading rewards table.")
        rewardsDict = {}
        initial = np.ones((9))
        initial[0] = 2
        while(True):
            i = 0
            initial[i] -= 1
            while(initial[i] == -2 and i < 9):
                initial[i] = 1
                i += 1
                if(i < 9):
                    initial[i] -= 1
                else:
                    break
            if(i == 9):
                break
            stateString = self.stateToString(initial)
            if(self.gameBoard.hasActorWon(initial.reshape(3, 3), 0)):
                rewardsDict[stateString] = -1
            elif(self.gameBoard.hasActorWon(initial.reshape(3, 3), 1)):
                rewardsDict[stateString] = 1
            else:
                rewardsDict[stateString] = 0
        return rewardsDict
    def loadRewards(self):
        loadPath = "C:/Users/aniru/Desktop/output.csv"
        with open(loadPath, "r") as file:
            rewardsList = file.readlines()
        rewardsList2 = [i.split(',') for i in rewardsList]
        rewardsDict = {}
        for j in rewardsList2:
            rewardsDict[j[0]] = float(j[1])
        print("Loading of rewardsDict successful.")
        return rewardsDict

    def stateToString(self, gameState):
        gameState = gameState.reshape(-1).tolist()
        stateString = ""
        for item in gameState:
            if(item == 0):
                stateString = stateString + '.'
            elif(item == 1):
                stateString = stateString + 'X'
            elif(item == -1):
                stateString = stateString + 'O'
        return stateString


    def printAIRewardsDict(self):
        print("AI Dict Rewards:")
        for i in list(self.aiRewards.keys()):
            if(self.aiRewards[i] != 1 and self.aiRewards[i] != -1 and self.aiRewards[i] != 0):
                print(i[0:3])
                print(i[3:6])
                print(i[6:9], self.aiRewards[i])


    def step(self):
        '''
        1) Print the prevStateArray and prevStateList
        2) Print the currStateArray and currStateList
        3) If not gameEnded:
            a) If the currState is a win/loss, prevStateArray's reward is updated appropriately. gameEnded.
            b) Else:
                Find the reachables.
                Find epsilonHat.
                If epsilonHat < epsilon,
                    choose a random reachable from reachables.
                    Print the chosen reachable, in both numeric and array form.
                    Print the reward for the chosen reachable.
                Else:
                    Choose the reachable for which reward is maximum. Do this by:
                        a) Set currentReward to -2. Print it
                        b) For every reachable point,
                            i)print the reachable point both in numeric and char form
                            ii)print the reward for that reachable point
                            iii) If the reward for that reachable point is higher,
                                a) Update chosenPoint, currentReward,
                                b) print that you have updated.
                            iv) Else:
                                a) print that you have not updated.
                    print prevStateArray in char form, update the reward for prevStateArray and print it.
                    print currStateArray in char form, update the reward for currStateArray and print it.
                    print newStateArray in char form, and its reward.
                    invoke the appropriate button.
        '''
        print("NEW ITERATION.")
        print("prevStateArray = ", self.prevStateArray)
        prevStateString = self.stateToString(self.prevStateArray)
        print("prevStateString = ")
        print(prevStateString[0:3])
        print(prevStateString[3:6])
        print(prevStateString[6:9])

        currStateArray = self.gameBoard.getGameStateArray()
        print("currStateArray = ", currStateArray)
        currStateString = self.stateToString(currStateArray)
        print("currStateString = ")
        print(currStateString[0:3])
        print(currStateString[3:6])
        print(currStateString[6:9])
        if not self.gameEnded:
            gameStateFlag = self.gameBoard.getGameStateFlag()
            if(gameStateFlag != 0 and gameStateFlag != 1):
                print("Game has now ended.")
                self.gameEnded = True
                self.aiRewards[prevStateString] = (1 - self.alpha)*self.aiRewards[prevStateString] + self.alpha*self.aiRewards[currStateString]
                print("Prevstate reward updated to " ,self.aiRewards[prevStateString])
            else:
                reachables = []
                for i in range(3):
                    for j in range(3):
                        if(currStateArray[i][j] == 0):
                            reachables.append((i, j))
                currentReward = -2
                print("Current reward = ", currentReward)
                for point in reachables:
                    (i, j) = point
                    print("Considering point ", point)
                    pointList = [c for c in currStateString]
                    pointList[3*i + j] = 'O'
                    pointString = "".join(pointList)
                    print(pointString[0:3])
                    print(pointString[3:6])
                    print(pointString[6:9])
                    pointReward = self.aiRewards[pointString]
                    print("The reward for this point is ", pointReward)
                    if(pointReward > currentReward):
                        print("This is a better point.")
                        currentReward = pointReward
                        chosenPoint = point
                        chosenString = pointString
                    else:
                        print("This is not a better point.")
                print("The point that was chosen in the end is", chosenPoint)
                print(chosenString[0:3])
                print(chosenString[3:6])
                print(chosenString[6:9])
                print("The reward for this point is: " , pointReward)
                self.aiRewards[prevStateString] = (1-self.alpha)*self.aiRewards[prevStateString] + self.alpha*self.aiRewards[chosenString]
                self.aiRewards[currStateString] = (1-self.alpha)*self.aiRewards[currStateString] + self.alpha*self.aiRewards[chosenString]
                print("The previous state reward is ", self.aiRewards[prevStateString])
                print(prevStateString[0:3])
                print(prevStateString[3:6])
                print(prevStateString[6:9])

                print("The current state reward is", self.aiRewards[currStateString])
                print(currStateString[0:3])
                print(currStateString[3:6])
                print(currStateString[6:9])
                self.gameBoard.getButton(*chosenPoint).invoke()
                self.prevStateArray = self.gameBoard.getGameStateArray()
                print("The new prev_state is " , self.prevStateArray)
        else:
            print("Game has already ended!")
###################aiAgent####################################################
###################main#######################################################
preWindow()
