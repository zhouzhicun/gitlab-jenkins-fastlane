##Fastlane教程
参考文档:      
[fastlane源码](https://github.com/fastlane/fastlane)    
[fastlane各个插件的教程](https://docs.fastlane.tools/actions/#building)     
[fastlane插件开发](http://www.infoq.com/cn/articles/actual-combat-of-fastlane-part02)       
[使用 fastlane 实现 iOS 持续集成](http://www.cocoachina.com/ios/20150916/13433.html)           
[深入浅出 Fastlane 一看你就懂](https://icyleaf.com/2016/07/fastlane-in-action/)


Action是Fastlane自动化流程中的最小执行单元，直观上来讲就是Fastfile脚本中的一个个命令，比如：git\_pull，deliver，pod\_install等等，而这些命令背后都对应一个用Ruby编写的脚本。

到目前为止Fastlane包含大约170多个Action，大约分为如下几类：

- 和移动端持续交付相关的15个核心的工具链：如：deliver（上传ipa，截屏和meta信息到ITC），supply（上传apk，截屏和meta信息到Google Play），sigh（iOS Provisioning文件管理）等等，详情如下：https://github.com/fastlane/fastlane#fastlane-toolchain
- 和iOS相关的，如：ipa，xcode\_install等等
- 和Android相关的，如：gradle，adb等等
- 和版本控制相关的，如git\_pull，hg\_push等等
- 和iOS依赖库管理相关的，如：cocoapods，carthage等等
- 第三方平台对接相关的，如：hipchat，jira，twitter，slack等等

这些Action的详情和使用方法可以查看这个链接：
[fastlane actions](https://docs.fastlane.tools/actions/Actions/)


Plugin就是在Action的基础上做了一层包装，这个包装巧妙的利用了RubyGems这个相当成熟的Ruby库管理系统，所以其可以独立于Fastlane主仓库进行查找，安装，发布和删除。
我们甚至可以简单的认为：Plugin就是RubyGem封装的Action，我们可以像管理RubyGems一样来管理Fastlane的Plugin。

- fastlane actions: List all available fastlane actions
- fastlane action [action_name]: Shows a more detailed description of an action
- fastlane lanes: Lists all available lanes with description
- fastlane list: Lists all available lanes without description
- fastlane new_action: Create a new action (integration) for fastlane
- fastlane env: Print out the fastlane ruby environment when submitting an issue


##Fastlane基本操作

####1 安装fastlane

	sudo gem install fastlane

####2 创建fastlane工程
首先进入到ios项目工程的根目录(即xcodeproj文件所在目录)，然后执行以下命令:

	fastlane init

运行该命令时，会提示回答如下几个问题:
	
	1. 
	Your Apple ID (e.g. fastlane@krausefx.com): 315701008@qq.com
	App Identifier (com.krausefx.app): com.xiaoniu88.Loan
	
	2. 
	Would you like to create your app on iTunes Connect and the Developer
	Portal? (y/n)
	n
	
	3. 
	Optional: The scheme name of your app (If you don't need one, just hit Enter):
	
	XNLoan


命令执行完成后，会在项目根目录下创建一个fastlane目录




####3 fastlane 常用命令(以下操作都是在项目根目录下执行)

1. 查看任务列表
	
		fastlane list
		
		或
		fastlane lanes

2. 运行某个任务，例如运行test任务

	  	fastlane ios test

3. 查看fastlane提供的所有actions列表

		fastlane actions

4. 查看指定action(例如adb)的使用帮助

		fastlane action adb
	
5. 创建自定义action(执行如下命令，并输入action名即可)

		fastlane new_action
		
		例如:
		opsdeMacBook-Pro:XNLoanApp xiaoniu$ fastlane new_action
		Must be lower case, and use a '_' between words. Do not use '.'
		examples: 'testflight', 'upload_to_s3'
		Name of your action: send_notify_mail
		[18:02:16]: Created new action file './fastlane/actions/send_notify_mail.rb'. Edit it to implement your custom action.


	命令执行完成后，将会在fastlane目录下创建一个actions目录，以及以action名作为文件名的rb文件。




###fastlane开发注意:

1. 安装exchange邮件发送组件viewpoint
		
		sudo gem install viewpoint

		******************如果安装没有报错，请忽略下面*********************
		
		sudo xcode-select -switch /Applications/Xcode.app/Contents/Developer
		
		brew install pkg-config libxml2 libxslt
		brew unlink xz
		gem install viewpoint
		brew link xz
	
	
	​	
		#nokogiri官网: https://github.com/sparklemotion/nokogiri
		#安装nokogiri报错，请参考 http://www.nokogiri.org/tutorials/installing_nokogiri.html
		#gem install nokogiri
	
2. 定义task, 例如:

		desc "Runs testTask"
		  lane :testTask do
		
		   # 使用ruby代码
		    hsh = { "red" => 0xf00, "green" => 0x0f0, "blue" => 0x00f }
		    hsh.each do |key, value|
		        print key, " is ", value, "\n"
		    end
		
		    puts "Hello, Ruby!";
		
		    #访问 Appfile文件中的变量
		    puts CredentialsManager::AppfileConfig.try_fetch_value(:app_identifier)
		
		    # 调用自定义的Action
		    send_notify_mail
		
		  end




###svn操作以及邮件发送功能代码:



	#!/usr/bin/ruby


​	
	########################### SVN 操作  ##################################
	
	def svn_commit(local_ipa_Path, remote_ipa_root_path, local_temp_svn_path)

		time = Time.new
		curDate = time.strftime("%Y%m%d")
		curTime = time.strftime("%H%M%S")
	
		#1 创建本次ipa的远端svn目录
		curSVNPath = remote_ipa_root_path + "/" + curDate + "/" + curTime
		system "svn mkdir --parents #{curSVNPath} -m \"创建ipa包目录\""
	
		#2 checkout刚刚创建的svn目录到本地
		system "svn checkout #{curSVNPath} #{local_temp_svn_path}"
	
		#3 复制ipa包目录到本地svn目录
		system "cp -rf #{local_ipa_Path} #{local_temp_svn_path}"
	
		#4 svn提交
		system "cd #{local_temp_svn_path} && svn add *  && svn commit -m \"提交测试包\""
	
	end
	
	ipa_path = '/Users/xiaoniu/Desktop/hehe'
	ipa_svn_path = 'http://tech.xiaoniu88.net/svn/documents/AppDocuments/XNOnline/开发/IOS/niudai_test'
	temp_svn_path = '/Users/xiaoniu/Desktop/svntest'
	svn_commit(ipa_path, ipa_svn_path, temp_svn_path)


​	
​	
​	
	############################ 使用ruby ViewPoint发送邮件 ####################################
	
	# 第一步： 打开 https://mail.xiaoniu66.com/ews/Exchange.asmx, 输入账号和密码,
	# 登陆成功会提示:
	# 已创建服务。
	# 若要测试此服务，需要创建一个客户端，并将其用于调用该服务。可以使用下列语法，从命令行中使用 svcutil.exe 工具来进行此操作:


​	
	# 参考文档:https://github.com/WinRb/Viewpoint
	require 'viewpoint'
	include Viewpoint::EWS
	
	endpoint = 'https://mail.xiaoniu66.com/ews/Exchange.asmx'
	user = 'xiaoniu\\xn047862'
	pass = 'Zhou'
	
	cli = Viewpoint::EWSClient.new endpoint, user, pass
	cli.send_message subject: "hello", body: "你是谁啊", to_recipients: ['zhouzhicun@xiaoniu66.com']





​		