#!/usr/bin/python
# coding:utf-8
#211
#svn 目录为/var/svn 模式http:// 钩子网站目录为/var/usr/local/apache2/htdocs/
import socket, threading, os, re, MySQLdb, random
import sys, os, time, atexit, string  
from signal import SIGTERM 
import ConfigParser
  
class Daemon:  
  def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/tmp/error.log'):  
      #需要获取调试信息，改为stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr'，以root身份运行。  
    self.stdin = stdin  
    self.stdout = stdout  
    self.stderr = stderr  
    self.pidfile = pidfile  
    
  def _daemonize(self):  
    try:  
      pid = os.fork()    #第一次fork，生成子进程，脱离父进程  
      if pid > 0:  
        sys.exit(0)      #退出主进程  
    except OSError, e:  
      sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))  
      sys.exit(1)  
    
    os.chdir("/")      #修改工作目录  
    os.setsid()        #设置新的会话连接  
    os.umask(0)        #重新设置文件创建权限  
    
    try:  
      pid = os.fork() #第二次fork，禁止进程打开终端  
      if pid > 0:  
        sys.exit(0)  
    except OSError, e:  
      sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))  
      sys.exit(1)  
    
     #重定向文件描述符  
    sys.stdout.flush()  
    sys.stderr.flush()  
    si = file(self.stdin, 'r')  
    so = file(self.stdout, 'a+')  
    se = file(self.stderr, 'a+', 0)  
    os.dup2(si.fileno(), sys.stdin.fileno())  
    os.dup2(so.fileno(), sys.stdout.fileno())  
    os.dup2(se.fileno(), sys.stderr.fileno())  
    
     #注册退出函数，根据文件pid判断是否存在进程  
    atexit.register(self.delpid)  
    pid = str(os.getpid())  
    file(self.pidfile,'w+').write('%s\n' % pid)  
    
  def delpid(self):  
    os.remove(self.pidfile)  
  
  def start(self):  
     #检查pid文件是否存在以探测是否存在进程  
    try:  
      pf = file(self.pidfile,'r')  
      pid = int(pf.read().strip())  
      pf.close()  
    except IOError:  
      pid = None  
    
    if pid:  
      message = 'pidfile %s already exist. Daemon already running!\n'  
      sys.stderr.write(message % self.pidfile)  
      sys.exit(1)  
      
    #启动监控  
    self._daemonize()  
    self._run()  
  
  def stop(self):  
    #从pid文件中获取pid  
    try:  
      pf = file(self.pidfile,'r')  
      pid = int(pf.read().strip())  
      pf.close()  
    except IOError:  
      pid = None  
    
    if not pid:   #重启不报错  
      message = 'pidfile %s does not exist. Daemon not running!\n'  
      sys.stderr.write(message % self.pidfile)  
      return  
  
     #杀进程  
    try:  
      while 1:  
        os.kill(pid, SIGTERM)  
        time.sleep(0.1)  
        #os.system('hadoop-daemon.sh stop datanode')  
        #os.system('hadoop-daemon.sh stop tasktracker')  
        #os.remove(self.pidfile)  
    except OSError, err:  
      err = str(err)  
      if err.find('No such process') > 0:  
        if os.path.exists(self.pidfile):  
          os.remove(self.pidfile)  
      else:  
        print str(err)  
        sys.exit(1)  
  
  def restart(self):  
    self.stop()  
    self.start()  
  
  def _run(self):  
    """ run your fun"""  
    while True:  
      #fp=open('/tmp/result','a+')  
      #fp.write('Hello World\n')  
      sys.stdout.write('%s:hello world\n' % (time.ctime(),))  
      sys.stdout.flush()   
      time.sleep(2)  
  
class MyDaemon(Daemon):  
	def _run(self):  

		self.master = {}
		self.masterpasswd = {}

		conn = MySQLdb.connect(host = configure['mysql']['host'], user = configure['mysql']['user'], passwd = configure['mysql']['passwd'], db = configure['mysql']['db'])
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM `%s`.`%s`;" %(configure['mysql']['db'],configure['mysql']['table']))
		alluser = cursor.fetchall()
		conn.commit()
		cursor.close ()
		conn.close ()

		for oneuser in alluser:
			if oneuser[4] == '1':        #如果权限为1 允许创建项目
				self.master[oneuser[0]] = oneuser[2]        
			
			if oneuser[3] or oneuser[3] != None:       #如果没有设置密码 默认为51job
				self.masterpasswd[oneuser[2]] = oneuser[3]
			else:
				self.masterpasswd[oneuser[2]] = configure['server']['default_passwd']

		
		host = configure['server']['host_listen']
		port = int(configure['server']['server_port'])
		print type(port)
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((host,port))
		server.listen(5)
		print host,port
		
		while 1:
			client,addr = server.accept()
			print ('Connected by:',addr)
			client_handler = threading.Thread(target=self.handle_client,args=(client,))
			client_handler.start()
	
	def swappass(self):        #生成密码
		num = 12
		Pass = ''
		while num>0:
		  
			PaW=chr(random.randint(48,126))
			if PaW != '\\':             #出现过，Mysql密码中的单个'\'设置密码时,'\'会消失
				Pass = Pass + "".join(PaW)
				num-=1
		return Pass
		
	def handle_client(self,client_socket):
		while 1:
			succeed = ''
			getmessage = client_socket.recv(4096)
			if getmessage != b"":
				getmessage=eval(getmessage)       #将收到的字符串，转回为字典
				print (getmessage)
				try:
					getmessage.get(self.master[getmessage['clientip']])               #判断是否有权限
				except KeyError:
					client_socket.send("you 'meiyou' permission !".encode())
					break
					
				svn_project_path = configure['path']['subversion_path'] + getmessage['project']
				
				apache_project = configure['path']['apache_project_path'] + getmessage['project']
				if getmessage.get('svn'):          #######使用svn部署项目#####
					
					
					if os.path.exists(svn_project_path):      #判断项目是否已经存在
						client_socket.send("project is exist !".encode())
						break
	 
					#创建项目
					os.system('%ssvnadmin create %s' % (configure['path']['subversion_bin'],svn_project_path))
	
					#权限配置
					try:
						authz=open('%s/conf/authz' % svn_project_path,'a')
						authz.write('[%s:/]\n%s=rw\nsvn=rw\n' % (getmessage['project'],self.master[getmessage['clientip']]))
						authz.close()
					except IOError:
						client_socket.send("error : project name NONONO...".encode())
						client_socket.close()
	
					#密码配置
					os.system('%shtpasswd -cb %s/conf/passwd %s %s' %(configure['path']['apache_bin'],svn_project_path,self.master[getmessage['clientip']],self.masterpasswd[self.master[getmessage['clientip']]]))
					os.system('%shtpasswd -b %s/conf/passwd %s %s' %(configure['path']['apache_bin'],svn_project_path,configure['subversion']['postcommit_name'],configure['subversion']['postcommit_pass']))
	
					#配置文件配置
					svnserve_conf = svn_project_path + '/conf/svnserve.conf'
					print svn_project_path
					
					os.system("sed -i 's/# anon-access = read/anon-access = none/g' %s" %svnserve_conf)
					os.system("sed -i 's/# auth-access = write/auth-access = write/g' %s" %svnserve_conf)
					os.system("sed -i 's/# password-db = passwd/password-db = passwd/g' %s" %svnserve_conf)
					os.system("sed -i 's/# authz-db = authz/authz-db = authz/g' %s" %svnserve_conf)
					# os.system("sed -i 's/# realm = My First Repository/realm = %s/g' %s" % (svn_project_path,svnserve_conf))
					os.system("sed -i 's/# realm = My First Repository/realm = %s/g' %s" % (svn_project_path.replace('/','\/'),svnserve_conf))
	
					#配置钩子
					hooks=open('%s/hooks/post-commit' %svn_project_path,'a')
					hooks.write('#!/bin/sh\nexport LANG=zh_CN.UTF-8\n%ssvn update %s --username %s --password %s >> %s/hooks/codedeploy.log\n' % (configure['path']['subversion_bin'],apache_project,configure['subversion']['postcommit_name'],configure['subversion']['postcommit_pass'],svn_project_path))
					hooks.close()
					os.system('chmod u+x %s/hooks/post-commit' %svn_project_path)
	
					#apache配置
					os.system('mkdir %s' %apache_project)
					apachesvn=open(configure['path']['apache_svnconf_path'],'a')
					apachesvn.write('<Location /%ssvn>\nDAV svn\nSVNPath %s\nAuthType Basic\nAuthName "Subversion repos"\nAuthUserFile %s/conf/passwd\nRequire valid-user\n</Location>\n\n\n' %(getmessage['project'],svn_project_path,svn_project_path))
					apachesvn.close()
					
					os.system('service httpd reload')
					#configure['path']['subversion_path']/httpd -k graceful
					
					#钩子启动
					os.system('%ssvn co http://%s/%ssvn  %s  --username=%s --password=%s' %(configure['path']['subversion_bin'],configure['server']['apache_listen_ip'],getmessage['project'],apache_project,configure['subversion']['postcommit_name'],configure['subversion']['postcommit_pass']))
	
					#权限配置
					apache_user = configure['path']['apache_user']
					os.system('chown -R  %s.%s %s' %(apache_user,apache_user,svn_project_path))
					os.system('chown -R  %s.%s %s/.svn' %(apache_user,apache_user,apache_project))
					os.system('chown -R  %s.%s %s' %(apache_user,apache_user,apache_project))
					
					succeed='succeed\nsvn addr:http://%s/%ssvn\nsvn user:%s\nproject look addr:http://%s/%s' % (configure['server']['apache_listen_ip'],getmessage['project'],self.master[getmessage['clientip']],configure['server']['apache_listen_ip'],getmessage['project'])
	
				if getmessage.get('mysql'):             ##是否需求mysql##
					mysqlpass=self.swappass()
					conn = MySQLdb.connect(host = configure['mysql']['host'], user = configure['mysql']['user'], passwd = configure['mysql']['passwd'], db = configure['mysql']['db'])
					cursor = conn.cursor()
					try:
						cursor.execute("create database %s" % getmessage['project'])
						cursor.execute("grant all privileges on %s.* to '%s'@'%%' identified by '%s';" %(getmessage['project'],getmessage['project'],mysqlpass))
					except:
						client_socket.send("mysql: database is exist !".encode())
						break	 
					conn.commit()
					cursor.close ()
					conn.close ()
					succeed = succeed + '\n\nmysqlname:%s\nmysqlpass:%s\n' % (getmessage['project'],mysqlpass)
	 
   
				if getmessage.get('samba'):                   ##是否需求samba##
   
					if os.path.exists(apache_project):         #判断项目是否已经存在	 
						sambaN=open('%ssmb.conf' %configure['path']['samba_path'],'r')
						if re.search('\[%s\]' %getmessage['project'] ,sambaN.read(20480)):
							sambaN.close()
							client_socket.send("samba: project is exist !".encode())
							break      
						else:
							sambaN.close()
							sambaC=open('%ssmb.conf' %configure['path']['samba_path'],'a')
							sambaC.write('\n[%s]\npath = %s\nbrowseable = yes\npublic = yes\nwritable = yes\nguest ok = yes\nhosts allow =%s\n' % (getmessage['project'], gapache_project, getmessage['clientip']))
							sambaC.close()
							succeed=succeed + "samba: \\\\%s\\%s\\\n" % (configure['server']['apache_listen_ip'],getmessage['project'])
					else:
						client_socket.send("project not exist !".encode())
						break
     
	
				if getmessage.get('svnrw') or getmessage.get('svnr'):    ######使用svnrw与svnr为添加用户功能判断######
					try:
						getmessage.get(self.master[getmessage['clientip']])               #判断是否有权限
					except KeyError:
						client_socket.send("you 'meiyou' permission !".encode())
						break
	
					try:
						userswap=open('%s/conf/authz' % svn_project_path,'r') #判断用户是否存在
					except IOError:
						client_socket.send("project no exist !".encode())
						break
					if re.search(getmessage['username'],userswap.read(4096)):
						client_socket.send("user 'yijing' exist !".encode())
						break
					userswap.close()
	
					#密码配置
					try:
						os.system('%shtpasswd -b %s/conf/passwd %s %s' %(configure['path']['apache_bin'],svn_project_path,getmessage['username'],self.masterpasswd[getmessage['username']]))
					except KeyError:
						client_socket.send("user not self.master !".encode())
						break
	 
					#添加用户
					addauthz=open('%s/conf/authz' % svn_project_path,'a')
					if getmessage.get('svnrw'):
						addauthz.write('%s=rw\n' % getmessage['username'])
					else:
						addauthz.write('%s=r' % getmessage['username'])
					addauthz.close()
	
					succeed="OK"
	
			if not getmessage:
				break
			if getmessage == "exit":
				break
			client_socket.send(succeed.encode())
	
		client_socket.close()
		

class configuration():		   #读取配置文件
	def get_dict(self,head):
		dictA = {}
		for servername in head:
			dictA[servername[0]] = servername[1]
		return dictA

			
	def readconffile(self):
		conff = ConfigParser.ConfigParser() 

		conff.read("./is.conf") 

		secs = conff.sections() 
		
		server_all = {}
		for head in secs:
			server = conff.items(head) 
			
			server_all[head] = self.get_dict(server)
		return  server_all
	
  
if __name__ == '__main__':    #启动
	global configure
	configure = configuration().readconffile()
	daemon = MyDaemon(configure['server']['pidfile'], stdout = configure['server']['log'])
	
	if len(sys.argv) == 2:  
		if 'start' == sys.argv[1]:  
			daemon.start()  
		elif 'stop' == sys.argv[1]:  
			daemon.stop()  
		elif 'restart' == sys.argv[1]:  
			daemon.restart()  
		else:  
			print 'unknown command'  
			sys.exit(2)  
		sys.exit(0)  
	else:  
		print 'usage: %s start|stop|restart' % sys.argv[0]  
		sys.exit(2)  

