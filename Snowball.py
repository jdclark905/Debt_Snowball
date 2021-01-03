# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:05:59 2020

@author: jdcla
"""


import sys, math
from PyQt5 import QtWidgets

from DebtSnowBallGUI import Ui_MainWindow

debts = []
months = 1 #time tracker
leftOver = 0 #tracks debt amount to roll over after overpayment
snowBall = 0 #tracks the payments after debts are paid off to snowball
totalInterest = 0 #tracks the total interest paid over the life of the loans
totalInterestNoSnow = 0 #tracks the total interest paid over the life of the loans

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btnClicked)
    
    #this is manually added cause I haven't figured out how to loop through yet
    def createDataTables(self):
        """Creates arrays of the debts to be calculated out"""
        if self.p1.text() != "":
            debts.append([float(self.p1.text()), 
                          float(self.i1.text()), 
                          float(self.m1.text())])
        if self.p2.text() != "":
            debts.append([float(self.p2.text()), 
                          float(self.i2.text()), 
                          float(self.m2.text())])
        if self.p3.text() != "":
            debts.append([float(self.p3.text()), 
                          float(self.i3.text()), 
                          float(self.m3.text())])       
        if self.p4.text() != "":
            debts.append([float(self.p4.text()), 
                          float(self.i4.text()), 
                          float(self.m4.text())])
        if self.p5.text() != "":
            debts.append([float(self.p5.text()), 
                          float(self.i5.text()), 
                          float(self.m5.text())])
        if self.p6.text() != "":
            debts.append([float(self.p6.text()), 
                          float(self.i6.text()), 
                          float(self.m6.text())])
        if self.p7.text() != "":
            debts.append([float(self.p7.text()), 
                          float(self.i7.text()), 
                          float(self.m7.text())])
        if self.p8.text() != "":
            debts.append([float(self.p8.text()), 
                          float(self.i8.text()), 
                          float(self.m8.text())])
        if self.p9.text() != "":
            debts.append([float(self.p9.text()), 
                          float(self.i9.text()), 
                          float(self.m9.text())])
        if self.p10.text() != "":
            debts.append([float(self.p10.text()), 
                          float(self.i10.text()), 
                          float(self.m10.text())])

    def activeDebt(self, currentBalance, interest, minPayment):
        global snowBall, months, leftOver, totalInterest
        print("Starting Current Balance for Active", '${:,.2f}'.format(currentBalance))
        print("Starting Snowball Amount", '${:,.2f}'.format(snowBall))
        while currentBalance > 0:
            interestCharged = currentBalance * interest / 12
            totalInterest += interestCharged
            balanceAndInterest = currentBalance + interestCharged
            currentBalance = balanceAndInterest - minPayment - snowBall
            months += 1
            if months % 12 == 0:
                snowBall = snowBall + float(self.extraCash.text())/12 #increase payments by $ each year
                #print("Snowball updated!", '${:,.2f}'.format(snowBall))
            if currentBalance < 0:
                leftOver = -currentBalance
                #print("Got leftovers", leftOver)
                break
        snowBall += minPayment

    def passiveDebt(self, currentBalance, interest, minPayment):
        global totalInterest
        for i in range(1,months+1):
            interestCharged = currentBalance * interest / 12
            totalInterest += interestCharged
            #print(interestCharged)
            balanceAndInterest = currentBalance + interestCharged
            currentBalance = balanceAndInterest - minPayment
        return currentBalance

    def goThroughDebts(self):
        for j in debts:
            print("Staring Debt Amount", '${:,.2f}'.format(j[0]))
            if months == 1:
                self.activeDebt(j[0], j[1], j[2])
            else:
                j[0] = self.passiveDebt(j[0], j[1], j[2])
                print("Leftover to use", '${:,.2f}'.format(leftOver))
                j[0] = j[0] - leftOver
                #print("After taking out leftovers", '${:,.2f}'.format(j[0]))
                self.activeDebt(j[0], j[1], j[2])
            print("Months passed", months)
            print("Snowball amount:", '${:,.2f}'.format(snowBall))
            print("Next Debt!~~~~~~~~~~~~~~~~")
        print("This takes ", math.floor(months / 12), " years ", months % 12, " months.")
        time = "This takes " + str(math.floor(months / 12)) + " years " + \
                "and " + str(months % 12) + " months to complete."
        self.textBrowser.append(time)
        print("Total interest paid:", '${:,.2f}'.format(totalInterest))
        interestPaidSnow = "Total interest paid: " + '${:,.2f}'.format(totalInterest)
        self.textBrowser.append(interestPaidSnow)

    def noSnowballDebt(self, currentBalance, interest, minPayment):
        global snowBall, leftOver, totalInterestNoSnow
        while currentBalance > 0:
            interestCharged = currentBalance * interest / 12
            totalInterestNoSnow += interestCharged
            balanceAndInterest = currentBalance + interestCharged
            currentBalance = balanceAndInterest - minPayment
        
    def noSnowballGoThroughDebts(self):
        for j in debts:
            self.noSnowballDebt(j[0], j[1], j[2])
        #print("Total Interest if No snowball", '${:,.2f}'.format(totalInterestNoSnow))
        interestPaidNoSnow = "Total Interest paid if no snowball: " + '${:,.2f}'.format(totalInterestNoSnow)
        self.textBrowser.append(interestPaidNoSnow)
        #print("Saved a total of", '${:,.2f}'.format(totalInterestNoSnow - totalInterest))
        moneySaved = "You will save a total of: " + '${:,.2f}'.format(totalInterestNoSnow - totalInterest)
        self.textBrowser.append(moneySaved)
        #print("We have",'${:,.2f}'.format(snowBall),"extra cash each month now.")
        extraCash = "You will have " + '${:,.2f}'.format(snowBall) + " extra cash each month."
        self.textBrowser.append(extraCash)

    def btnClicked(self):
        self.createDataTables()
        self.goThroughDebts()
        self.noSnowballGoThroughDebts()
        #self.label.setText("Button Clicked")
        #self.textBrowser.append("Testing THis Out!")
        #for i in debts:
            #self.textBrowser.append(str(i[0]))
        #self.textBrowser.append(str(self.p1.text()))
        #self.textBrowser.append(str(self.p2.text()))
        #if self.p2.text() == "":
            #self.textBrowser.append("NOthing")


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
