# -*- coding: utf-8 -*-

import os
import sys
import types
import datetime

import biplist



##################### 常量定义 ##########################

#包类型
PackageType_AppStore = 1
PackageType_jailbreak = 2

#环境类型
EnvironmentType_Product = 0
EnvironmentType_TestIn = 1
EnvironmentType_TestOut = 2
EnvironmentType_PreProduct = 3
EnvironmentType_Custom = 4


#加密类型
EncryptType_NoEncrypt = 0
EncryptType_Encrypt = 1



##################### 打包配置文件的配置项 ########################


#SVN地址
ConfigItem_Package_SVN_Remote_Path = "Package_SVN_Remote_Path"

#git配置
ConfigItem_GitPath = "GitPath"
ConfigItem_Branch = "Branch"
ConfigItem_RepositoryName = "RepositoryName"

#App配置
ConfigItem_BundleId = "BundleId"
ConfigItem_DefaultAppName = "DefaultAppName"
ConfigItem_ProjectName = "ProjectName"

#环境配置匹配项
ConfigItem_Environment_API_Path = "Environment_API_Path"
ConfigItem_Environment_Pattern = "Environment_Pattern"
ConfigItem_Open_Encrypt_pattern = "Open_Encrypt_pattern"
ConfigItem_Environment_Address_pattern = "Environment_Address_pattern"


#证书配置
ConfigItem_CodeSignIdentity = "CodeSignIdentity"



#配置文件路径
ConfigItem_XcodeProj_Path = "XcodeProj_Path"
ConfigItem_Environment_File_Path = "Environment_File_Path"
ConfigItem_Info_Plist_Path = "Info_Plist_Path"





##################### 解析配置文件 ##########################

configDic = {}

def parse(configFilePath):


    global configDic

    #读取配置文件
    configDic = biplist.readPlist(configFilePath)

    #去前后空格
    for key in configDic:
        configDic[key] = configDic[key].strip()













