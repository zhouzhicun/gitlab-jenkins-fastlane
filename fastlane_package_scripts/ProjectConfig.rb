#!/usr/bin/ruby


module Config

############################ Modify_environment ##################################
#环境配置
Env_file         = "/XNLoan/Macro/URLMacro.h"
Env_type_pattern = "#define Configure_Environment "
Env_addr_pattern = "#define XNL_URL_BASE "



############################ send_notify_mail ######################################
#邮箱配置
Email_endpoint 		= "https://mail.xiaoniu66.com/ews/Exchange.asmx"

#发件人账号信息
Email_user 	 		= "xiaoniu\\zx.CI_Admin.sys"
Email_password 		= "111111"

#邮件人默认列表
Email_Recipients 	= 
"11@xiaoniu66.com
22@xiaoniu66.com
33@xiaoniu66.com\n"


############################ upload_to_svn ######################################
#ipa包上传的svn根目录
Svn_package_path 	 = "http://tech.xiaoniu88.net/svn/documents/AppDocuments/XNOnline/开发/IOS/niudai_test"



############################ 工程基本配置 ######################################
Package_scheme 							= "XNLoan"
Package_Develop_codesigning_identity 	= "iPhone Developer: Yu Liu (LWCUPRHZZN)"


end

