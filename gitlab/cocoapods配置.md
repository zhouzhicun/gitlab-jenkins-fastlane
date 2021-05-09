##cocoapods配置问题

参考文档:    
[CocoaPods: pod search 搜索类库失败的解决办法](http://blog.cocoachina.com/article/29127)	

#####ios环境配置：
下载安装Xcode, 安装cocoaPods。

CocoaPods: pod search 搜索类库失败的解决办法:

1. 重装cocoapods
	
		//第一步: 删除旧的pod
		rm -rf ~/.cocoapods/repos/master 
		
		//替换gems源
		gem sources --remove https://rubygems.org/
		gem sources -a https://ruby.taobao.org/
		
		//安装新版 cocoapods
		sudo gem install -n /usr/local/bin cocoapods
		
		sudo xcode-select -switch /Applications/Xcode.app/Contents/Developer


2. pod setup
如果pod setup很久时间都未成功，甚至报如下错误的话:

		bogon:repos xiaoniu$ pod setup
		Setting up CocoaPods master repo
		[!] /usr/bin/git clone https://github.com/CocoaPods/Specs.git master
		
		Cloning into 'master'...
		error: RPC failed; curl 56 SSLRead() return error -36
		fatal: The remote end hung up unexpectedly
		fatal: early EOF
		fatal: index-pack failed


	解决方法是:    
	
		//第一步: cd repos目录下
		cd ~/.cocoapods/repos/
		
		//第二步: git clone Specs.git到该目录下
		git clone https://github.com/CocoaPods/Specs.git master
		
		//第三步: pod setup
		pod setup




​	
3. 如果此时还pod search不到的话，cd到master目录下，调用find命令看看是否存在search的pod库是否存在，例如:

		find . -name "Weex*" -print 

	如果能find到的话，说明Specs.git已存在，但是search不到，说明search_index.json缓存文件是旧的，没有包含新的pod库，我们需要删除它。
		
		//终端输入
		rm ~/Library/Caches/CocoaPods/search_index.json
	
	删除成功后，再执行search命令:
	
		终端输入：
		pod search afnetworking(不区分大小写)
		
		输出：Creating search index for spec repo 'master'.. Done!，
		稍等片刻, 就会出现所有带有afnetworking字段的类库。


