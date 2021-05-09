# jenkins环境搭建

### 1.安装JDK 

#### 第一步:下载JDK

首先我们需要下载java开发工具包JDK，选择下载mac osx版本就行。下载地址：

	http://www.oracle.com/technetwork/java/javase/downloads/index.html

#### 第二步:安装JDK

安装完成后，测试一下JDK是否安装成功。输入以下命令: 

	java -version 

如果出现以下信息，说明JDK已安装配置成功.

	java version "1.8.0_101"
	Java(TM) SE Runtime Environment (build 1.8.0_101-b13)
	Java HotSpot(TM) 64-Bit Server VM (build 25.101-b13, mixed mode)

### 2.安装homebrew

首先键入如下命令查看是否已安装homebrew:

	brew -v

如果出现以下信息，则说明已安装homebrew:
	Homebrew 1.1.5
	Homebrew/homebrew-core (git revision 718b; last commit 2016-12-21)

否则键入一下命令安装homebrew:

	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"



### 3. 通过brew安装jenkins	

#### 3.1 brew安装jenkins

	brew install jenkins

#### 3.2 卸载jenkins	

	//第一步:卸载jenkins
	brew uninstall jenkins
	
	//第二步:删除jenkins文件夹
	rm -rf ~/.jenkins


#### 3.3 启动&重启jenkins


	//方式1, 直接启动jenkins, 按control+c 关闭jenkins
	jenkins 
	
	//方式2:作为服务启动
	brew services start jenkins
	
	//重启jenkins服务
	brew services restart jenkins
	
	//停止jenkins服务
	brew services stop jenkins

#### 注意:

第一次启动jenkins时(使用方式1)，jenkins会自动创建一个管理员账号。其中密码信息显示如下:


	*************************************************************
	*************************************************************
	*************************************************************
	
	Jenkins initial setup is required. An admin user has been created and a password generated.
	Please use the following password to proceed to installation:
	
	a2796f4d676c485ab545be3d1766105e
	
	This may also be found at: /Users/xiaoniu/.jenkins/secrets/initialAdminPassword
	
	*************************************************************
	*************************************************************
	*************************************************************


如上所示，其中初始化密码为:"a2796f4d676c485ab545be3d1766105e", 并把初始密码保存在如下目录文件中:

	/Users/xiaoniu/.jenkins/secrets/initialAdminPassword


#### 3.4 使用jenkins

打开浏览器，输入以下地址即可。 

	http://localhost:8080/

如果我们是第一次打开jenkins，会提示我们 Unlock Jenkins， 这时候我们直接输入上面的初始化密码即可， 然后会提示我们安装插件，我们直接选择安装建议的插件就好了。然后就是创建第一个管理员账号。

	用户名: xif
	密码: zhouzhicun
	邮箱: 315701008@qq.com

####3.5 所有的jenkins的job构建的工作目录位于

	/Users/xiaoniu/.jenkins/workspace





# Jenkins配置

参考文档:     
[Jenkins学习二：Jenkins安装与配置](http://www.cnblogs.com/yangxia-test/p/4354328.html)

### 1.用户管理

* 第一步:点击 左侧菜单栏的"系统管理"
* ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/用户管理-第一步.png)
* 第二步:点击 系统管理列表中的"管理用户"
  ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/用户管理-第二步.png)
* 第三步:新建or编辑or删除用户
  ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/用户管理-第三步.png)



### 2 邮件配置

1. 点击系统管理-->系统设置:
   ![11](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/jenkins邮件配置-第1步.png)

2. 下拉到中间位置的"Jenkins Location", 配置如下:
   ![22](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/jenkins邮件配置-第2步.png)

3. 下拉到最底部的"邮件通知", 配置如下:
   ![33](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/jenkins邮件配置-第3步.png)

##### 注意: 

第2步中的“系统管理员邮件地址”设置必须和第3步中的“使用SMTP认证”的用户名一致。



### 3 权限管理

参考文档:    
[Jenkins学习七：Jenkins的授权和访问控制](http://www.cnblogs.com/yangxia-test/p/4368778.html)


1. 安装权限管理插件: Role-based Authorization Strategy。     
   然后打开: 系统管理--> Configure Global Security, 并按照下图勾选授权策略
   ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/权限设置-第0步.png)

2. 打开 "系统管理" --> Manage and Assign Roles 菜单
   权限管理主要分为三大块: 
   * Manage Roles: 角色权限设置
   * Assign Roles:	用户权限设置
   * Role Strategy Macros				

如图所示:
![33](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/权限设置-第1步.png)


3. Manage Roles: 角色权限设置
   ![33](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/权限设置-第2步.png)

4. Assign Roles:	用户权限设置
   ![33](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/权限设置-第3步.png)


简单角色权限设置:
admin: 勾选所有权限
dev: 略
test: Overall(Read, RunScripts),Job(Build,Read)


###4 创建job

* 第1步:点击 左侧菜单栏的"新建"
  ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/创建job-第1步.png)

* 第2步:输入job名，并选择job构建类型     
  Enter an item name(输入job名) --> 点击选中"构建一个自由风格的软件项目"--> 点击"OK"。
  ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/创建job-第2步.png)



* 第3步:点击 配置job "General"块, 其中General块配置项主要包括如下:
  * 项目名称
  * 描述
  * 参数化构建过程 --> 添加构建参数

![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/创建job-第3步.png)


* 第4步:配置job "构建"块, 操作如下:		
  点击"增加构建步骤" --> 选择 Execute shell, 通过python脚本进行构建打包。如图:
  ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/创建job-第4步.png)
  ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/创建job-第5步.png)

* 第5步:配置job "构建后操作"块, 操作如下:	
  点击"增加构建后操作步骤" --> 选择 Email Notification, 配置收件人的邮箱地址即可。
  ![](/Users/zzc/Desktop/gitlab-jenkins-fastlane/jenkins/image/创建job-第6步.png)

  













