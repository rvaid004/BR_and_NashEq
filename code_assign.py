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

    
   def payoffRandomizer(rows, cols):
       count = 1
       strategyVarP1 = list()
       print("------------------------------------")
       print ("Player: Player 1's strategies")
       print ("{", end="")
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
       payoff1 = np.random.randint(-99,99, (rows,cols))      
       temp1 = [[str(y) for y in x] for x in payoff1]

       tempPayoff1 = DataFrame(payoff1)
       print (tempPayoff1)
       count = 1
       print("------------------------------------")
       print("\n")
       print("------------------------------------")
       print ("Player: Player 2's strategies")
       print ("{", end="")
       strategyVarP2 = list()
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
       payoff2 = np.random.randint(-99,99, (rows,cols))
       temp2 = [[str(y) for y in x] for x in payoff2]
       tempPayoff2 = DataFrame(payoff2)

       print (tempPayoff2)
       print("------------------------------------")
       print ("\n")

       lists = np.array([zip(a,b) for a,b in zip(payoff1,payoff2)])
       tempLists = np.array([zip(k,l) for k,l in zip(temp1,temp2)])
       newL = list(lists)
       newTempL = list(tempLists)
       print("=======================================")
       print("Display Normal Form")
       print("=======================================")
       display1 = DataFrame(newL)
       display1.index = strategyVarP1
       display1.columns = strategyVarP2
       print(display1)
       mystring = ""

       for c in range(cols):
           max = np.max(payoff1[:,c])
           nash1 = np.argmax(payoff1[:,c])
           temp1[nash1][c] = 'H'
          
     
       for r in range(rows):
           max = np.max(payoff2[r,:])
           nash2 = np.argmax(payoff2[r,:])
           temp2[r][nash2] = 'H'

       print ("\n")
       print("=======================================")   
       print("Nash Pure Equilibrium Locations:")
       print("=======================================")
       checkNash = DataFrame(newTempL)
       checkNash.index = strategyVarP1
       checkNash.columns = strategyVarP2
       print (checkNash)
       print("\n")

       nashEqExists = False
       for row in checkNash.itertuples():
           for col in range(cols):              
               if(getattr(row, checkNash.columns[col]) == ('H', 'H')):
                   (r,c) = (row.Index, checkNash.columns[col])
                   (n1, n2) = (r,c)
                   nashEqExists = True
                   print ("Nash Equilibrium(s): ", (r, c))
      
       print("\n")
       belief1 = np.round(np.random.dirichlet(np.ones(cols),size=1), decimals = 2)
       belief1 = belief1.reshape(-1)

       expPay1 = list()
       expSum = 0
       check = 0
    
       brSum1 = list()
       maxPayoff1 = np.round(payoff1[0][0] * belief1[0], decimals=2)
       maxRow = ""
       for r in range(rows):
           for c in range(cols):
                calc = np.round(payoff1[r][c] * belief1[c], decimals= 2) 
                if(check != cols):
                    expSum = calc + expSum
                    check+= 1
                if(check == cols):
                    brSum1.append(round(expSum, 2))
                    expSum = 0
                    check = 0

                expPay1.append(calc)
       index  = np.argmax(brSum1)
       maxRow = checkNash.index[index]
       belief2 = np.round(np.random.dirichlet(np.ones(rows),size=1), decimals = 2)
       belief2 = belief2.reshape(-1)
       print("---------------------------------------------")
       print("Player1 Expected Payoffs with Player 2 Mixing")
       print("---------------------------------------------")
       
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
       maxPayoff2 = np.round(payoff2[0][0] * belief2[0], decimals=2)
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
       
       for v in range(cols):
            print("U(" + strategyVarP2[v] + ",", belief2, "=", brSum2[v])
       print("\n")
       index2 = np.argmax(brSum2)
       maxCol = checkNash.columns[index2]

       
       print("-------------------------------------------")
       print("Player2 Best Response with Player 1 mixing")
       print("-------------------------------------------")
       print("BR", belief2, "= {", maxCol, "}")
       print("\n")

       mixedPayoff1 = 0
       mixedPayoff2 = 0
       for r1 in range(rows):
           mixedPayoff1 = (brSum1[r1] * belief2[r1]) + mixedPayoff1
           mixedPayoff2 = (brSum2[r1] * belief1[r1]) + mixedPayoff2

       

       print("------------------------------------------------------")
       print("Player 1 & 2 Expected Payoffs with both Player Mixing")
       print("-------------------------------------------------------")
       print("Player 1 -> U", belief2, ",",belief1, "=", round(mixedPayoff1,2))
       print("Player 2 -> U", belief2, ",",belief1, "=", round(mixedPayoff2,2))
       print("\n")

       if(rows == 2 and cols == 2):

            if(nashEqExists):
                print("------------------------------------------------------")
                print("Nash Pure Equilibrium Location")
                print("-------------------------------------------------------")
                print (checkNash)
                print("-------------------------------------------------------")
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
                q = Symbol('q')
                p = Symbol('p')
                firstEq = solve(q * payoff1[0][0] + (1-q) * payoff1[0][1] - (q * payoff1[1][0] + (1-q) * payoff1[1][1]))
                dec1 = round(float(firstEq[0]), 2)
                diff1 = round(1-dec1 ,2)
                secondEq = solve(p * payoff2[0][0] + (1-p) * payoff2[1][0] - (p * payoff2[0][1] + (1-p) * payoff2[1][1]))
                dec2 =  round(float(secondEq[0]), 2)
                diff2 = round(1-dec2 ,2)

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
            

   def payOffManual(rows, cols):
        count = 1
        strategyVarP1 = list()
        for n in range(rows):
           strategyVarP1.append("A"+ str(count))
           count+=1
        strategyVarP2 = list()
        count = 1
        for j in range(cols):
            strategyVarP2.append("B"+ str(count))
            count+=1
        manualPay1 = list()
        for x in range(rows):
            for y in range(cols):
                print("Enter payoff for (", strategyVarP1[x], ", ", strategyVarP2[y], ") = ", end="")
                manualPay1.append(tuple(map(str,input().split(','))))
        
        tempM1 = [list(i) for i in manualPay1]

        print(manualPay1)
        print(DataFrame(manualPay1))    

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

























"""

   def onButton(event):
       print ("Button pressed.")
  
   app = wx.App()
  
   frame = wx.Frame(None, -1, 'win.py')
   frame.SetSize(0,0,200,50)
  
   # Create text input
   dlg = wx.TextEntryDialog(frame, 'Enter (R)andom or (M)anual payoffs enteries','Text Entry')
   dlg.SetValue("")

   if dlg.ShowModal() == wx.ID_OK:
       print('You entered: %s' % dlg.GetValue())
   dlg.Destroy()

   if(dlg.GetValue() == 'R' or dlg.GetValue().lower() == 'r'):
   
        dlg2 = wx.TextEntryDialog(frame, 'Enter the number of rows', 'Text Entry')
        dlg2.SetValue("")
        dlg2.Destroy()

        dlg3 = wx.TextEntryDialog(frame, 'Enter the number of columns', 'Text Entry')
        dlg3.SetValue("")
        dlg3.Destroy()

        if dlg2.ShowModal() == wx.ID_OK and dlg3.ShowModal() == wx.ID_OK:
            p1 = dlg2.GetValue()
            p2 = dlg3.GetValue()
            payoffRandomizer(int(p1),int(p2))

   elif(dlg.GetValue()=='M' or dlg.GetValue().lower() == 'm'):

       inputRows = input()
       inputCols = input()

       payOffManual(inputRows, inputCols)
       
        # dlg2 = wx.TextEntryDialog(frame, 'Enter the number of rows', 'Text Entry')
        # dlg2.SetValue("")
        # dlg2.Destroy()

        # dlg3 = wx.TextEntryDialog(frame, 'Enter the number of columns', 'Text Entry')
        # dlg3.SetValue("")
        # dlg3.Destroy()

        # if dlg2.ShowModal() == wx.ID_OK and dlg3.ShowModal() == wx.ID_OK:
        #     p1 = dlg2.GetValue()
        #     print("Enter the number of rows: " +  p1)
        #     p2 = dlg3.GetValue()
        #     print("Enter the number of columns: " + p2)
        #     payOffManual(int(p1), int(p2))
"""

 


