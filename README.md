# autosvn 说明
===
基于Subversion/apache/mysql的svn自动部署工具


这是工具是去年制作的，现在也在一直在使用，<br>
制作初衷是为去除重复建立项目的工作，将工具直接给开发人员，让他们自己玩去，<br>
要知道，你将要对接40、50位开发人员，这就不是懒的事情了<br>
先上client端，<br>
server端还在清理，后续放上来，因为之前是自己使用，几天捏出来的玩意，东西有点乱，<br>
这个工具我也许会继续维护、优化、还请大家能给予意见。<br>

![](https://raw.githubusercontent.com/wangwuli/autosvn/master/gihub/main.png)  <br>
![](https://raw.githubusercontent.com/wangwuli/autosvn/master/gihub/add.png)    <br>
![](https://raw.githubusercontent.com/wangwuli/autosvn/master/gihub/adduser.png) <br>
+++++++
v0.2 loding..

server，增加配置文件，使得修改配置文件，直接start使用，<br>
解决因Subversion/apache/mysql程序安装方式/安装路径不同导致的环境兼容性问题。<br><br>
server文件已经差不多改造完毕，可以守护进程读取conf文件运行，不过今天忙晕了，忘记把对应的conf文件放哪里了，明天看有没有时间再找找。

+++++++

end，ths

