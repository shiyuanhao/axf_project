
## 一、git操作
git push -u origin master

## 二、链接远程服务器
ssh root@112.74.55.3

## 三、基本步骤
```
- 安装基本环境
    虚拟环境、mysql

- 上传项目
    保证项目能正常运行(相关依赖)

- Nginx
    静态文件、代理

- uWsgi
    启动Django项目

- Nginx 与 uwsgi对接
```

## 四、虚拟环境安装
一定要测试是否安装成功！！

## 五、数据库
一定要测试是否安装成功！！

## 六、安装Nginx
一定要测试是否安装成功！！
浏览器中输入 IP，能看到 `Welcome to nginx!` 说明Nginx安装成功!!!


## 七、Nginx基本配置 [以2048为实例]
```
# mynginx.config
http {
   server {

	location /2048 {
	   alias /var/www/2048html/;
	}	
   }
}
```

## 八、Django项目

## 九、uwsgi安装

## 十、uwsgi启动Django项目

## 十一、nginx + uwsgi Django项目


## 十二、其他
- Nginx
```
# 安装
## key验证
$ wget http://nginx.org/keys/nginx_signing.key
$ sudo apt-key add nginx_signing.key

## 添加到 /etc/apt/sources.list 文件中
deb http://nginx.org/packages/ubuntu/ xenial nginx
deb-src http://nginx.org/packages/ubuntu/ xenial nginx

## 更新源
$ apt update

## 安装
$ apt install nginx




## 相关命令
# 设置关闭开机自启动
$ systemctl disable nginx.service

# 设置开机自启动 (并没有开启Nginx)
$ systemctl enable nginx.service

# 重启nginx
$ systemctl restart nginx.service

# 查看状态
$ systemctl status nginx.service

# 启动
$ systemctl start nginx.service

# 关闭
$ systemctl stop nginx.service


##
# 查看进行
ps -ef | grep nginx

# 杀死进程
pkill -9 nginx

# 指定配置文件启动
$ nginx -c path/filename


##
# 检查是否安装成功 浏览器中输入服务器IP地址，可以看到`Welcome to nginx!`说明安装成功!
```

- Nginx配置
```
# 服务器文件路径
# /var/www/2048html/2048.html

server {
    # /game/2048.html
    location /game {
        # /var/www/2048html/2048.html
        alias /var/www/2048html/;
    }
}
```
> 注意: 配置文件修改后，需要重新启动!!!!



- Django
```
# 上传项目

# 数据库(表单、数据)    [客户端做数据备份 >>>> 服务器数据恢复]
$ apt install mysql-server

# 运行环境 [虚拟环境]
# 第一步: 安装
$ pip install virtualenv
$ pip install virtualenvwrapper
# 第二步: 查看安装目录
$ type virtualenvwrapper.sh
# 第三步: 配置
$ vi ~/.bashrc
    export WORKON_HOME=~/.virtualenvs
    source    /usr/local/bin/virtualenvwrapper.sh
# 第四步: 创建目录
$ mkdir ~/.virtualenvs
# 第五步: 刷新环境
$ source ~/.bashrc
# 第六步: 创建虚拟环境
$ mkvirtualenv python3 -p /usr/bin/python3.5
# 第七步: 检查是否成功(是否python3.5版本)
$ python # 备注: ubuntu中Python2的环境默认都是全的，但是Python3的集成不够完整，有部分包是欠缺的
$ apt update
$ apt install python3-dev
# 第八步: 安装依赖
$ pip install -r requirements.txt

# 启动项目
$ python manage.py runserver 0.0.0.0:8000
```

- uwsgi
```
# 安装    [虚拟环境]
pip install uwsgi

## 配置
http=0.0.0.0:9000
# 配置工程目录(项目目录-服务器所在位置) /var/www/Python1809AXF/    Python1809AXF/wsgi.py
chdir=/var/www/Python1809AXF/
# 配置项目的wsgi目录
wsgi-file=Python1809AXF/wsgi.py

# 启动
uwsg --ini uwsgi.ini


##
# 查看进行
ps -ef | grep uwsgi

# 杀死进程
pkill -9 uwsgi
```




