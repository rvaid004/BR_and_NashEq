"""=============================================================================
//Group	Number: 21
//PROGRAMMER1: Rishabh Vaidya
//	PANTHER	ID1: 5918963
//
//PROGRAMMER2: Raj Kapadia
//	PANTHER	ID2: 5704911
//
//	CLASS: CAP4506	
//	SECTION: U01
//	SEMESTER: Spring 2018
//	CLASSTIME:	M/W 6:15 to 7:40
//
//	Project: Randomizing payoffs of players in a game to find best response, expected payoffs, and Nash Equilibriums
//	DUE: 04/07/2019							
//
//	CERTIFICATION: I certify	that	this	work	is	my	own	and	that
//  none	of	it	is	the	work	of	any	other	person.
//============================================================================="""

import wx
import itertools
import random
import numpy as np
from pandas import *

class randomizer:

    def onButton(event):
        print ("Button pressed.")
    
    app = wx.App()
    
    frame = wx.Frame(None, -1, 'win.py')
    frame.SetSize(0,0,200,50)
    
    # Create text input
    dlg = wx.TextEntryDialog(frame, 'Enter (R)andom or (M)anual payoffs enteries','Text Entry')
    dlg.SetValue("")
    if dlg.ShowModal() == wx.ID_OK:
        print('You entered: %s\n' % dlg.GetValue())
    dlg.Destroy()

    def payoffRandomizer(rows, cols):
        count = 1
        print ("Player: Player 1's strategies")
        print ("{", end="")
        for n in range(rows):
            print ("A", count, sep ="", end="")
            print (" ", end="")
            count+=1
        print ("}")
        print ("\n")
        print("Player: Player 1's payoffs")
        payoff1 = np.random.randint(-99,99, (rows,cols))
        #temp1 = [[]]

        temp1 = [[str(y) for y in x] for x in payoff1]

        print (temp1) 

        print (DataFrame(payoff1))
        count = 1

        print("\n")
        print ("Player: Player 2's strategies")
        print ("{", end="")
        for m in range(cols):
            print ("B", count, sep ="", end="")
            print (" ", end="")
            count+=1
        print ("}")
        print ("\n")
        print("Player: Player 2's payoffs")
        payoff2 = np.random.randint(-99,99, (rows,cols))
        temp2 = [[str(y) for y in x] for x in payoff2]
        print (DataFrame(payoff2))
        print ("\n")

        lists = np.array([zip(a,b) for a,b in zip(payoff1,payoff2)])
        tempLists = np.array([zip(k,l) for k,l in zip(temp1,temp2)])
        newL = list(lists)
        newTempL = list(tempLists)
        print("Display Normal Form")
        display1 = DataFrame(newL)
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
        print("Nash Pure Equilibrium Locations:")
        checkNash = DataFrame(newTempL)
        print (checkNash)
        print("\n")
       
        #nashArr = [[0 for x in range(rows)] for y in range(cols)] 
        
        # for index, row in checkNash.iterrows():
        #     print(row[index], row[index+1])

        for row in checkNash.itertuples():
            for col in range(cols):
                if(checkNash.iloc[row.Index][col] == ('H', 'H')):
                    (r,c) = (row.Index, col)
                    print ("Nash Equilibrium(s): ", (r, c))
                print(checkNash.iloc[row.Index][col])
        

        belief1 = np.round(np.random.dirichlet(np.ones(cols),size=1), decimals = 2)
        belief1 = belief1.reshape(-1)
        print (belief1)

        expPay1 = list()
        maxPayoff = np.round(payoff1[0][0] * belief1[0], decimals=2)

        #print (payoff1)
        for r in range(rows):
            for c in range(cols):
                calc = np.round(payoff1[r][c] * belief1[c], decimals=2)
                if(calc > maxPayoff):
                    maxPayoff = calc
                expPay1.append(calc)

        belief2 = np.round(np.random.dirichlet(np.ones(rows),size=1), decimals = 2)
        belief2 = belief2.reshape(-1)
        print (belief2)
        print(expPay1)

        expPay2 = list()
        maxPayoff2 = np.round(payoff2[0][0] * belief2[0], decimals=2)
        for c in range(cols):
            for r in range(rows):
                calc = np.round(payoff2[r][c] * belief2[r], decimals=2)
                if(calc > maxPayoff2):
                    maxPayoff2 = calc
                expPay2.append(calc)

        print (expPay2)
        print (maxPayoff2)


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

    

   
