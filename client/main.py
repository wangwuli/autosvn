#coding=UTF-8 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from mainui import *
import sys
import socket

class Sdeploy(QDialog):
 def __init__(self):  
   super(Sdeploy,self).__init__()
   self.OK=Ui_Sdeploy()
   self.OK.setupUi(self)
   self.retAll=''
   
 def send(self): 
  self.ip=self.OK.lineEdit.text()
  IP=self.ip                
  
  who=Sdeploy.who()  
  
  if self.OK.checkBox.isChecked():    
   self.SVN=1
  else:
   self.SVN=0
  
  if self.OK.checkBox_2.isChecked():
   self.samba=1
  else:
   self.samba=0
  
  if self.OK.checkBox_4.isChecked():
   self.Mysql=1
  else:
   self.Mysql=0
  
  self.project=self.OK.lineEdit_2.text()        
  
  if IP == '':
   self.ret = "error : 请输入服务器IP"  
  elif self.project == '':
   self.ret = "error : 请输入项目名"
  elif self.SVN==0 and self.samba==0 and self.Mysql==0:
   self.ret = "error : 请勾选一个功能"
  else: 
   self.ret = Sdeploy.linkA(IP, svn=self.SVN, clientip=who, project=self.project, mysql=self.Mysql, samba=self.samba)     #传值到服务端
   
  self.retAll=self.ret+'\n'+self.retAll
  self.OK.plainTextEdit.setPlainText(self.retAll)  
  
 def linkA(IP,**other):   
  print (str(other))    
  target_host = IP
  target_port = 9999
  client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  try:
   client.connect((target_host,target_port))
   client.send(str(other).encode())   
   response = client.recv(4096)
   return response.decode('gb2312')   
   
  except TimeoutError:
   return "error:connect %s timeout" %IP
  except ConnectionRefusedError:
   return "error:%s reject" %IP
   
 def who():             
  hostname = socket.getfqdn(socket.gethostname())
  isaddr = socket.gethostbyname(hostname)
  return isaddr
  
class Sadd(QDialog):                  #用户添加
 def __init__(self):            
  super(Sadd,self).__init__()
  self.OK=Ui_Sadd()
  self.OK.setupUi(self)
  self.retAll=''
 
 def send(self):              
 
  self.ip=self.OK.lineEdit.text()     
  IP=self.ip
  
  self.rname=self.OK.lineEdit_2.text()   
  
  self.username=self.OK.lineEdit_3.text()      
  
  who=Sdeploy.who() 
 
  if self.OK.checkBox.isChecked():    
   self.SVNrw=1
  else:
   self.SVNrw=0
   
  if self.OK.checkBox_2.isChecked(): 
   self.SVNr=1
  else:
   self.SVNr=0
  
  if self.SVNrw==1 and self.SVNr==1:
   self.ret = "error : 请只选择一种权限类型"
  elif self.SVNrw==0 and self.SVNr==0:
   self.ret = "error : 请选择一种权限类型"
  elif IP == '':
   self.ret = "error : 请输入服务器IP"
  elif self.rname == '':
   self.ret = "error : 请输入项目名"
  elif self.username == '':
   self.ret = "error : 请输入用户名"
  else:
   self.ret = Sadd.linkA(IP, project=self.rname, username=self.username, svnrw=self.SVNrw, svnr=self.SVNr, clientip=who)     #传值到服务端
   
  self.retAll=self.retAll+self.ret+'\n'
  self.OK.plainTextEdit.setPlainText(self.retAll)  
  
 def linkA(IP,**other):          
  print (str(other))  
  target_host = IP
  target_port = 9999
  client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  try:
   client.connect((target_host,target_port))
   client.send(str(other).encode())      
   response = client.recv(4096)
   return response.decode('gb2312')        
   
  except TimeoutError:
   return "error:connect %s timeout" %IP
  except ConnectionRefusedError:
   return "error:%s reject" %IP
  
class explain(QDialog):
 def __init__(self):               
  super(explain,self).__init__()
  self.OK=Ui_explain()
  self.OK.setupUi(self)


class Smain(QtWidgets.QWidget):         
 def __init__(self):       
  super(Smain,self).__init__()
  self.OK=Ui_Smain()
  self.OK.setupUi(self)
 
 def deploy(self):           
  svnin=Sdeploy()
  svnin.show()
  svnin.exec()
  
 def adduser(self):       
  svnin=Sadd()
  svnin.show()
  svnin.exec()
  
 def help(self):        
  svnin=explain()
  svnin.show()
  svnin.exec()
  
def mainwindows():
 app = QtWidgets.QApplication(sys.argv) 
 windows = Smain()
 windows.show()
 sys.exit(app.exec())
  
if __name__ == "__main__":
 mainwindows() 