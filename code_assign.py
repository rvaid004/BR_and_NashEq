"""=============================================================================
//Group Number: 21
//PROGRAMMER1: Rishabh Vaidya
//  PANTHER ID1: 5918963
//
//PROGRAMMER2: Raj Kapadia
//  PANTHER ID2: 5704911
//
//  CLASS: CAP4506  
//  SECTION: U01
//  SEMESTER: Spring 2018
//  CLASSTIME:  M/W 6:15 to 7:40
//
//  Project: Randomizing payoffs of players in a game to find best response, expected payoffs, and Nash Equilibriums
//  DUE: 04/07/2019                         
//
//  CERTIFICATION: I certify    that    this    work    is  my  own and that
//  none    of  it  is  the work    of  any other   person.
//============================================================================="""

import wx
import itertools
import random
import numpy as np
from pandas import *
from sympy.solvers import solve
from sympy import Symbol

class randomizer:

   #function for random mode 
   def payoffRandomizer(rows, cols):
       count = 1
       strategyVarP1 = list() #list of player 1's variables
       print("------------------------------------")
       print ("Player: Player 1's strategies")
       print ("{", end="")

       #adds player 1's strategies to the list
       for n in range(rows):
           strategyVarP1.append("A"+ str(count))
           print ("A", count, sep ="", end="")
           print (" ", end="")
           count+=1
       print ("}")
      
       print("------------------------------------")
       print ("\n")
       print("------------------------------------")
       print("Player: Player 1's payoffs")

       payoff1 = np.random.randint(-99,99, (rows,cols))    #random payoff values for player1
       temp1 = [[str(y) for y in x] for x in payoff1]     #copy of payoffs as strings    


       tempPayoff1 = DataFrame(payoff1) #pandas library function that formats the payoffs in a table
       print (tempPayoff1) #player 1's payoffs

       print("------------------------------------")
       print("\n")
       print("------------------------------------")
       print ("Player: Player 2's strategies")
       print ("{", end="")
       count = 1
       strategyVarP2 = list() #list of player 2's strategies

       #adds each strategy for player 2 in the list
       for m in range(cols):
           strategyVarP2.append("B"+ str(count))
           print ("B", count, sep ="", end="")
           print (" ", end="")
           count+=1
       print ("}")

       print("------------------------------------")
       print ("\n")
       print("------------------------------------")
       print("Player: Player 2's payoffs")

       payoff2 = np.random.randint(-99,99, (rows,cols))  #random payoff values for player 2
       temp2 = [[str(y) for y in x] for x in payoff2]    #payoff values converted to strings

       tempPayoff2 = DataFrame(payoff2) #pandas library function that formats the payoffs in a table
       print (tempPayoff2) 
       print("------------------------------------")
       print ("\n")
       
       #zips the two integer payoff lists to create tuples of payoffs
       #zips the two string payoff lists to create tuples of payoffs
       lists = np.array([zip(a,b) for a,b in zip(payoff1,payoff2)])
       tempLists = np.array([zip(k,l) for k,l in zip(temp1,temp2)])
       newL = list(lists)
       newTempL = list(tempLists)

       print("====================================================================")
       print("Display Normal Form")
       print("====================================================================")

       display1 = DataFrame(newL)           #pandas library function that formats the payoff tuples in a table
       display1.index = strategyVarP1       #labels rows as player 1's strategies
       display1.columns = strategyVarP2     #labels columns as player 2's strategies
       print(display1)                     
       print("---------------------------------------------------------------------")

       #goes through each column for player 1's payoffs and finds the max values
       #and replaces them with 'H' to setup a nash equilibrium
       for c in range(cols):
           max = np.max(payoff1[:,c])
           nash1 = np.argmax(payoff1[:,c])
           temp1[nash1][c] = 'H'
       
       #goes through each row for player 2's payoffs and finds the max values
       #and replaces them with 'H' to setup a nash equilibrium   
       for r in range(rows):
           max = np.max(payoff2[r,:])
           nash2 = np.argmax(payoff2[r,:])
           temp2[r][nash2] = 'H'

       print ("\n")
       print("====================================================================")   
       print("Nash Pure Equilibrium Locations:")
       print("====================================================================")

       checkNash = DataFrame(newTempL)      #creates table with nash equilibrums
       checkNash.index = strategyVarP1      #labels rows with player 1's strategies
       checkNash.columns = strategyVarP2    #labels columns with player 2's strategies
       print (checkNash)
       print("---------------------------------------------------------------------")
       print("\n")

       nashEqExists = False         #boolean variable to check if a nash equilibrium exists

       #loops through all the tuples in the table and prints out nash equilibriums if two
       #H's are found for the same tuple
       for row in checkNash.itertuples():
           for col in range(cols):              
               if(getattr(row, checkNash.columns[col]) == ('H', 'H')):
                   (r,c) = (row.Index, checkNash.columns[col])
                   (n1, n2) = (r,c)
                   nashEqExists = True
                   print ("Nash Equilibrium(s): ", (r, c))

       if(nashEqExists == False):
            print("Nash Equlibrium(s): None")
       print("\n")

       #uses a random distribution to create beliefs for player 1 that add up to 1
       belief1 = np.round(np.random.dirichlet(np.ones(cols),size=1), decimals = 2)
       belief1 = belief1.reshape(-1)

       expPay1 = list()
       expSum = 0
       check = 0
       brSum1 = list()
       maxPayoff1 = np.round(payoff1[0][0] * belief1[0], decimals=2)   #sets up max variabele for comparison
       maxRow = ""
       
       #loops through payoffs for player 1 and multiplies it with player 1's beliefs
       #to calculate expected payoffs for player 1
       for r in range(rows):
           for c in range(cols):
                calc = np.round(payoff1[r][c] * belief1[c], decimals= 2)   #calculates expected payoffs for player 1
                if(check != cols):
                    expSum = calc + expSum
                    check+= 1
                if(check == cols):
                    brSum1.append(round(expSum, 2))
                    expSum = 0
                    check = 0
                expPay1.append(calc)

       index  = np.argmax(brSum1)           #finds index of the max payoff for player 1 to find best response
       maxRow = checkNash.index[index]      #sets maxRow to the strategy of player1 with the best response
       
       #uses a random distribution to create beliefs for player 2 that add up to 1
       belief2 = np.round(np.random.dirichlet(np.ones(rows),size=1), decimals = 2)
       belief2 = belief2.reshape(-1)

       print("---------------------------------------------")
       print("Player1 Expected Payoffs with Player 2 Mixing")
       print("---------------------------------------------")
       
       #prints the best respose for player 1
       for var in range(rows):
            print("U(" + strategyVarP1[var] + ",", belief1, "=", brSum1[var])
       print("\n")
    
       print("-------------------------------------------")
       print("Player1 Best Response with Player 2 Mixing")
       print("-------------------------------------------")
       print("BR", belief1, "= {",maxRow,  "}")
       print("\n")

       expPay2 = list()
       brSum2 = list()
       expSum = 0
       check = 0
       maxPayoff2 = np.round(payoff2[0][0] * belief2[0], decimals=2)  #sets up max variable for comparison

       #loops through payoffs for player 1 and multiplies it with player 1's beliefs
       #to calculate expected payoffs for player 1
       for c in range(cols):
           for r in range(rows):
                calc = np.round(payoff2[r][c] * belief2[r], decimals= 2) 
                if(check != rows):
                    expSum = calc + expSum
                    check+= 1
                if(check == rows):
                    brSum2.append(round(expSum, 2))
                    expSum = 0
                    check = 0
                expPay2.append(calc)

       print("---------------------------------------------")
       print("Player2 Expected Payoffs with Player 1 mixing")
       print("---------------------------------------------")
       
       #prints the best respose for player 2
       for v in range(cols):
            print("U(" + strategyVarP2[v] + ",", belief2, "=", brSum2[v])
       print("\n")

       index2 = np.argmax(brSum2)           #finds index of the max payoff player 2 to find best response
       maxCol = checkNash.columns[index2]   #sets maxCol to the strategy of player 2 with the best response

       
       print("-------------------------------------------")
       print("Player2 Best Response with Player 1 mixing")
       print("-------------------------------------------")
       print("BR", belief2, "= {", maxCol, "}")
       print("\n")

       mixedPayoff1 = 0
       mixedPayoff2 = 0

       #loops through the rows and finds the payoffs when both player's mix
       for r1 in range(rows):
           mixedPayoff1 = (brSum1[r1] * belief2[r1]) + mixedPayoff1
           mixedPayoff2 = (brSum2[r1] * belief1[r1]) + mixedPayoff2

       print("------------------------------------------------------")
       print("Player 1 & 2 Expected Payoffs with both Players Mixing")
       print("-------------------------------------------------------")
       print("Player 1 -> U", belief2, ",",belief1, "=", round(mixedPayoff1,2))
       print("Player 2 -> U", belief2, ",",belief1, "=", round(mixedPayoff2,2))
       print("\n")

       #checks for a 2x2 matrix and finds indifference mix probabilities
       #if there is no nash equlibrium found 
       if(rows == 2 and cols == 2):

            if(nashEqExists):
                print("=======================================")   
                print("Nash Pure Equilibrium Locations:")
                print("=======================================")
                print (checkNash)
                print("---------------------------------------")
                print("Nash Equilibriums: ", (n1,n2))
                print("\n")
                print("----------------------------------------------")
                print("Player 1 & 2 Indifferent Mix Probabilities")
                print("----------------------------------------------")
                print("Normal Form has Pure Strategy Equilibrium\n")
            else:
                print("------------------------------------------------------")
                print("Player 1 & 2 Indifferent Mix Probabilities")
                print("-------------------------------------------------------")

                q = Symbol('q')     #python library that uses symbols for math equations
                p = Symbol('p')    

                #solves for q using python library in order to find indifferent mix probability
                firstEq = solve(q * payoff1[0][0] + (1-q) * payoff1[0][1] - (q * payoff1[1][0] + (1-q) * payoff1[1][1]))
                dec1 = round(float(firstEq[0]), 2)      #rounds to two places
                diff1 = round(1-dec1 ,2)                #finds 1-q

                #solves for p using python library in order to find indifferent mix probability
                secondEq = solve(p * payoff2[0][0] + (1-p) * payoff2[1][0] - (p * payoff2[0][1] + (1-p) * payoff2[1][1]))
                dec2 =  round(float(secondEq[0]), 2)    #rounds to two places
                diff2 = round(1-dec2 ,2)                #finds 1-p

                print ("Player 1 probability of strategies (" + strategyVarP1[0] + ") =", dec1)
                print ("Player 1 probability of strategies (" + strategyVarP1[1] + ") =", diff1)
                print ("Player 2 probability of strategies (" + strategyVarP2[0] + ") =", dec2)
                print ("Player 2 probability of strategies (" + strategyVarP2[1] + ") =", diff2)
                print("\n")
                print("------------------------------------------------------")
                print("Nash Pure Equilibrium Location")
                print("-------------------------------------------------------")
                print (checkNash)
                print("-------------------------------------------------------")
                print ("Nash Equilibrium(s): None\n")
            
   #function for manual mode
   def payOffManual(rows, cols):
        count = 1
        strategyVarP1 = list()      #list of player 1's strategies

        #loops through rows and adds each one of player 1's strategies to the list
        for n in range(rows):
           strategyVarP1.append("A"+ str(count))
           count+=1
        
        strategyVarP2 = list()       #list of player 1's strategies
        list1 = list()
        count = 1

        #loops through columns and adds each one of player 1's strategies to the list
        for j in range(cols):
            strategyVarP2.append("B"+ str(count))
            count+=1

        manualPay1 = np.empty((rows,cols), object) #creates empty np array

        #loops through 2d array and adds tuples of payoffs
        for x in range(rows):
            for y in range(cols):
                print("Enter payoff for (", strategyVarP1[x], ", ", strategyVarP2[y], ") = ", end="")
                manualPay1[x,y] = tuple(map(str,input().split(',')))
            print("--------------------------------")
            
        normForm = DataFrame(manualPay1)    #uses pandas library to create table of payoffs
        normForm.index = strategyVarP1      #labels rows with player 1's strategies 
        normForm.columns = strategyVarP2    #labels columns with player 2's strategies
    
        tempPay1 = manualPay1.copy()    
        indexMax1 = 0
        
        #loops through rows and cols to look for max payoff for player 1 and replace it with an H
        for n in range(rows):
            max1= 0
            for m in range(cols):
                x,y = manualPay1[n,m]
                newV = int(y)
                if(newV > max1):
                    max1 = newV
                    index = m
                if(m == cols-1):
                    for a in range(cols):
                            newX, newY = manualPay1[n,a] 
                            newV2 = int(newY)
                            if(newV2 == max1):
                                value1, value2 =  tempPay1[n,a]
                                indexMax1 = a
                                tempPay1[n,indexMax1] = value1, 'H'

        indexMax = 0
        indexMax1 = 0

        #loops through rows and cols to look for max payoff for player 2 and replace it with an H
        for m in range(cols):
            max2 = 0
            for n in range(rows):
                x,y = manualPay1[n,m]
                newV = int(x)
                if(newV > max2):
                    max2 = newV
                    val1, val2 = tempPay1[n,m]
                    indexMax = n
                if(n == rows-1):
                    tempPay1[indexMax,m] = 'H', val2
                    for a in range(rows):
                        newX, newY = manualPay1[a,m] 
                        newV1 = int(newX)
                        if(newV1 == max2): 
                            value1, value2 =  tempPay1[a,m]
                            indexMax1 = a
                            tempPay1[indexMax1,m] = 'H', value2


        print("====================================================================")
        print("Display Normal Form")
        print("====================================================================")
        print(normForm)
        print("--------------------------------------------------------------------")
        print("\n")
        

        nashForm = DataFrame(tempPay1)      #creates table of nash equlibriums 
        print("====================================================================")   
        print("Nash Pure Equilibrium Locations:")
        print("====================================================================")
        nashForm.index = strategyVarP1      #labels rows with strategies of player 1
        nashForm.columns = strategyVarP2    #labels columns with strategies of player 2
        print(nashForm)
        print("--------------------------------------------------------------------")

        nashEqExists = False

        #loops through all the tuples in the table and prints out nash equilibriums if two
        #H's are found for the same tuple
        for row in nashForm.itertuples():
           for col in range(cols):              
               if(getattr(row, nashForm.columns[col]) == ('H', 'H')):
                   (r,c) = (row.Index, nashForm.columns[col])
                   (n1, n2) = (r,c)
                   nashEqExists = True
                   print ("Nash Equilibrium(s): ", (r, c))
        print("\n")
        
        if(nashEqExists == False):
            print("Nash Equlibrium(s): None\n")
        
        #checks for a 2x2 matrix and finds indifference mix probabilities
        #if there is no nash equlibrium found 
        if(rows == 2 and cols == 2):
            if(nashEqExists):
                print("----------------------------------------------")
                print("Player 1 & 2 Indifferent Mix Probabilities")
                print("----------------------------------------------")
                print("Normal Form has Pure Strategy Equilibrium\n")
            else:
                print("------------------------------------------------------")
                print("Player 1 & 2 Indifferent Mix Probabilities")
                print("------------------------------------------------------")

                q = Symbol('q') #python library that uses symbols for math equations
                p = Symbol('p')

                #sets variables equal to all the tuples in the 2x2 matrix
                x1,y1  = manualPay1[0,0]
                newx1 = int(x1)
                newy1 = int(y1)
                x2,y2 = manualPay1[0,1]
                newx2 = int(x2)
                newy2 = int(y2)
                x3,y3 = manualPay1[1,0]
                newx3 = int(x3)
                newy3 = int(y3)
                x4,y4 = manualPay1[1,1]
                newx4 = int(x4)
                newy4 = int(y4)

                #solves for q using python library in order to find indifferent mix probability
                firstEq = solve(q * newx1 + (1-q) * newx2 - (q * newx3 + (1-q) * newx4))
                dec1 = round(float(firstEq[0]), 2)      #rounds to two places
                diff1 = round(1-dec1 ,2)                #gets 1-q

                #solves for p using python library in order to find indifferent mix probability
                secondEq = solve(p * newy1 + (1-p) * newy2 - (p * newy3 + (1-p) * newy4))
                dec2 =  round(float(secondEq[0]), 2)    #rounds to two places
                diff2 = round(1-dec2 ,2)                #gets 1-p

                print ("Player 1 probability of strategies (" + strategyVarP1[0] + ") =", dec1)
                print ("Player 1 probability of strategies (" + strategyVarP1[1] + ") =", diff1)
                print ("Player 2 probability of strategies (" + strategyVarP2[0] + ") =", dec2)
                print ("Player 2 probability of strategies (" + strategyVarP2[1] + ") =", diff2)
                print("\n")

        

   #getting input for random or manual mode
   print("Enter (R)andom or (M)anual payoffs enteries")
   inputName = input()
   if(inputName == 'R' or inputName == 'r'):
        print("Enter the number of rows: ", end="")
        inputRows = input()
        print("Enter the number of columns: ", end="")
        inputCols = input()
        payoffRandomizer(int(inputRows), int(inputCols))
   elif(inputName == 'M' or inputName == 'm'):
       print("Enter the number of rows: ", end="")
       inputRows = input()
       print("Enter the number of columns: ", end="")
       inputCols = input()
       payOffManual(int(inputRows), int(inputCols))


























 


