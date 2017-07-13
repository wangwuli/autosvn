# autosvn 说明
===
基于Subversion/apache/mysql的svn自动部署工具,<br>
使用前提是，apache的svn服务已经部署好，<br>
samba服务使用的是IP控制访问权限。
开发环境为centos7.3。


这是工具是去年制作的，<br>
制作初衷是为去除重复建立项目的工作，将工具直接给开发人员，让他们自己玩去，<br>
这个工具我也许会继续维护、优化、还请大家能给予意见。<br>

![](https://raw.githubusercontent.com/wangwuli/autosvn/master/gihub/main.png)  <br>
![](https://raw.githubusercontent.com/wangwuli/autosvn/master/gihub/add.png)    <br>
![](https://raw.githubusercontent.com/wangwuli/autosvn/master/gihub/adduser.png) <br>
+++++++
v0.2 loding..

server，增加配置文件，使得修改配置文件，直接start使用，<br>
解决因Subversion/apache/mysql程序安装方式/安装路径不同导致的环境兼容性问题。<br><br>
今天跑了一下，应该差不多了。<br>

### 《NEW》
下一步有时间的话，可能会找或者写一些API去shell化，以及增加前提环境make文件。

+++++++

end，ths

