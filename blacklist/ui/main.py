import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog, QTableWidget, QTableWidgetItem
import mysql.connector
import pandas as pd
import ui


class ScreenChange(QDialog):
    def __init__(self):
        super().__init__()
        self.conn = mysql.connector.connect(
            user = 'ellie',
            password = 'Password',
            database = 'hubXchange_unsubscribed')
        self.cur = self.conn.cursor()        
        self.resultout = None

    def gotomainscreen(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoaddindscreen(self):
        add = AddScreen()
        widget.addWidget(add)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoremoveindscreen(self):
        remove = RemoveScreen()
        widget.addWidget(remove)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoresultscreen(self):
        result = ResultScreen()
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex()+1)
        result.resultlable.setText(self.resultout)

    def gotocheckscreen(self):
        check = CheckScreen()
        widget.addWidget(check)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotofilescreen(self):
        file = FileScreen()
        widget.addWidget(file)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoaddfilescreen(self):
        file = AddFileScreen()
        widget.addWidget(file)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoremovefilescreen(self):
        file = RemoveFileScreen()
        widget.addWidget(file)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocheckfilescreen(self):
        file = CheckFileScreen()
        widget.addWidget(file)
        widget.setCurrentIndex(widget.currentIndex()+1)
    


class MainScreen(ScreenChange):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.add.clicked.connect(self.gotoaddindscreen)
        self.remove.clicked.connect(self.gotoremoveindscreen)
        self.check.clicked.connect(self.gotocheckscreen)
            

class AddScreen(ScreenChange):
    def __init__(self):
        super().__init__()
        loadUi("addscreen.ui", self)
        self.menu.clicked.connect(self.gotomainscreen)
        self.addInd.clicked.connect(self.addind)
        self.upload.clicked.connect(self.gotoaddfilescreen)
        
    
    def addind(self):
        first_name = self.firstnamefield.text()
        last_name = self.lastnamefield.text()
        email = self.emailfield.text()
        insert_values=[first_name, last_name, email]
        
        if len(first_name)==0 or len(last_name)==0 or len(email)==0:
            self.error.setText("Please fill out all of the information")
        else:
            insert_query="INSERT IGNORE INTO unsubscribed (first_name, last_name, email) VALUES (%s, %s, %s)"
            with self.conn:
                self.cur.execute(insert_query, insert_values)
                self.conn.commit()
                self.resultout = "Person Added To Blacklist"
                self.gotoresultscreen()                    
    
class RemoveScreen(ScreenChange):
    def __init__(self):
        super().__init__()
        loadUi("removescreen.ui", self)
        self.menu.clicked.connect(self.gotomainscreen)
        self.remove.clicked.connect(self.removeind)
        self.upload.clicked.connect(self.gotoremovefilescreen)

        
    def removeind(self):
        email = self.emailfield.text()       
        if len(email)==0:
            self.error.setText("Please fill out all of the information")
        else:
            remove_query="DELETE FROM unsubscribed WHERE email=%s"
            with self.conn:
                self.cur.execute(remove_query, (email,))
                self.conn.commit()
                self.emailfield.clear()
                self.resultout = "Person Deleted From Blacklist"
                self.gotoresultscreen()                    



class CheckScreen(ScreenChange):
    def __init__(self):
        super().__init__()
        loadUi("checkscreen.ui", self)
        self.menu.clicked.connect(self.gotomainscreen)
        self.check.clicked.connect(self.checkind)
        self.upload.clicked.connect(self.gotocheckfilescreen)
        
    def checkind(self):
        email = self.emailfield.text()
        if len(email)==0:
            self.error.setText("Please fill out all of the information")
        else:
            check_query="SELECT 1 FROM unsubscribed WHERE email=%s"
            with self.conn:
                self.cur.execute(check_query, (email,))
                check = self.cur.fetchall()
            if not check:
                self.emailfield.clear()
                self.resultout = "Person Not Blacklisted"
                self.gotoresultscreen() 
            else:
                self.emailfield.clear()
                self.resultout = "Person Blacklisted"
                self.gotoresultscreen()                    
                
                  
            
class ResultScreen(ScreenChange):
    def __init__(self):
        super().__init__()
        loadUi("resultscreen.ui", self)
        self.menu.clicked.connect(self.gotomainscreen)
        
        
class FileScreen(ScreenChange):
    def __init__(self):
        super().__init__()
        loadUi("filescreen.ui", self)
        self.df = self.getdata()
        self.menu.clicked.connect(self.gotomainscreen)        
        
    def getdata(self):
        filepath = QFileDialog.getOpenFileName()[0]
        with open(filepath, 'r') as f:
            f.seek(3)
            df = pd.read_csv(f, usecols=['first_name', 'last_name', 'email']).to_dict('list') 
            return df

    def showdata(self):
        self.datatable.setRowCount(len(self.df)-1)
        horHeaders = []
        for n, key in enumerate(self.df.keys()):            
            horHeaders.append(key)
            for m, item in enumerate(self.df[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.datatable.setItem(m, n, newitem)
                self.datatable.resizeColumnsToContents()
                self.datatable.resizeRowsToContents()
        self.datatable.setHorizontalHeaderLabels(horHeaders)

class AddFileScreen(FileScreen):
    def __init__(self):
        super().__init__()
        loadUi("addfilescreen.ui", self)
        self.showdata()
        self.confirm.clicked.connect(self.addfile)
        self.menu.clicked.connect(self.gotomainscreen)
        
    def addfile(self):
        with self.conn:
            for fn, ln , em in zip((self.df["first_name"]), (self.df["last_name"]), (self.df["email"])):
                self.cur.execute("INSERT IGNORE INTO unsubscribed (first_name, last_name, email) VALUES ('"+fn+"','"+ln+"','"+em+"')")
                self.resultout = "People Added To Blacklist"
                self.gotoresultscreen()                    


class RemoveFileScreen(FileScreen):
    def __init__(self):
        super().__init__()
        loadUi("removefilescreen.ui", self)
        self.showdata()
        self.confirm.clicked.connect(self.removefile)

        
    def removefile(self):
        with self.conn:
            for em in self.df["email"]:
                self.cur.execute("DELETE FROM unsubscribed WHERE email=?", (em,))
                self.resultout = "People Removed From Blacklist"
                self.gotoresultscreen()                    

class CheckFileScreen(FileScreen):
    def __init__(self):
        super().__init__()
        loadUi("checkfilescreen.ui", self)
        self.checkfile()
        self.menu.clicked.connect(self.gotomainscreen)
        
    def checkfile(self):
        match = []
        match_dic = []
        row=0
        for em in self.df["email"]:
            match.append( self.cur.execute("SELECT * FROM unsubscribed WHERE email=?", (em,)).fetchone())               
        for i in match:
            if i is None:
                continue
            match_dic.append({'first_name': i[0], 'last_name': i[1], 'email': i[2]})
        self.datatable.setRowCount(len(match_dic))
        for person in match_dic:
            self.datatable.setItem(row, 0, QtWidgets.QTableWidgetItem(person["first_name"]))
            self.datatable.setItem(row, 1, QtWidgets.QTableWidgetItem(person["last_name"]))
            self.datatable.setItem(row, 2, QtWidgets.QTableWidgetItem(person["email"]))
            row=row+1


     

    

        

       
                
#main
app = QApplication(sys.argv)
main = MainScreen()
widget = QStackedWidget()
widget.addWidget(main)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Exiting")