
# -*- coding: utf-8 -*-

import os
import sys
import types
import datetime

import biplist

import PackageConfig






######################### App名字+包名 #############################

# # 中文后缀
# def appNameSuffix_CN(environment_type, encrypt_type)
#
#     environment_suffix = ""
#     if environment_type == 1:
#         # 内网测试环境
#         environment_suffix = "测试内网"
#
#     elif environment_type == 2:
#         # 外网测试环境
#         environment_suffix = "测试外网"
#
#     elif environment_type == 3:
#         # 准生产环境
#         environment_suffix = "准生产"
#
#     encrypt_suffix = ""
#     if encrypt_type == 0:
#         # 不加密
#         encrypt_suffix = "不加密"
#
#     elif encrypt_type == 1:
#         # 加密
#         encrypt_suffix = "加密"
#
#     return environment_suffix + "_" + encrypt_suffix


# 英文后缀
def appNameSuffix_EN(environment_type, encrypt_type):

    environment_suffix = ""
    if environment_type == PackageConfig.EnvironmentType_TestIn:
        # 内网测试环境
        environment_suffix = "TestIn"

    elif environment_type == PackageConfig.EnvironmentType_TestOut:
        # 外网测试环境
        environment_suffix = "TestOut"

    elif environment_type == PackageConfig.EnvironmentType_PreProduct:
        # 准生产环境
        environment_suffix = "preProduct"

    encrypt_suffix = ""
    if encrypt_type == PackageConfig.EncryptType_NoEncrypt:
        # 不加密
        encrypt_suffix = "noEncrypt"

    elif encrypt_type == PackageConfig.EncryptType_Encrypt:
        # 加密
        encrypt_suffix = "Encrypt"

    return environment_suffix + "_" + encrypt_suffix


def appNameSuffix_Custom(environment_name, encrypt_type):

    encrypt_suffix = ""
    if encrypt_type == PackageConfig.EncryptType_NoEncrypt:
        # 不加密
        encrypt_suffix = "noEncrypt"

    elif encrypt_type == PackageConfig.EncryptType_Encrypt:
        # 加密
        encrypt_suffix = "Encrypt"

    return environment_name + "_" + encrypt_suffix


def buildAppName(curDate, curTime, defaultAppName, projectName, environment_name, environment_type, encrypt_type):

    # App后缀名(例如:测试内网_加密)
    suffix = appNameSuffix_EN(environment_type, encrypt_type)
    if environment_name :
        suffix = appNameSuffix_Custom(environment_name, encrypt_type)


    # App名(例如:牛贷_测试内网_加密)
    curAppName = defaultAppName + "_" + suffix

    # ipa包名(例如:XNLoan_2016_1120_1200_测试内网_加密)
    curIpaPackageName = projectName + "_" + curDate + "_" + curTime + "_" + suffix

    return (curAppName, curIpaPackageName)



def modifyAppConfigFile(project_path, environment_addr, environment_type, encrypt_type, appName):

    print("修改App配置文件...")
    cur_environment_File_Path = project_path + "/" + PackageConfig.configDic[PackageConfig.ConfigItem_Environment_File_Path]
    cur_Info_Plist_Path = project_path + "/" + PackageConfig.configDic[PackageConfig.ConfigItem_Info_Plist_Path]


    # 修改App配置
    modifyEnvironmentConfigFile(cur_environment_File_Path,
                                environment_type,
                                environment_addr,
                                encrypt_type)
    modifyAppInfoPlistFile(cur_Info_Plist_Path, appName)





######################### 修改App环境配置文件 #############################

def modifyEnvironmentConfigFile(environment_Path, enviroment_Type, enviroment_Addr, encrypt_Type):


    print ("修改url_macro文件...")

    environment_pattern = PackageConfig.configDic[PackageConfig.ConfigItem_Environment_Pattern]
    environment_addr_pattern = PackageConfig.configDic[PackageConfig.ConfigItem_Environment_Address_pattern]
    encrypt_pattern = PackageConfig.configDic[PackageConfig.ConfigItem_Open_Encrypt_pattern]



    # 读取环境配置文件(url_macro文件)
    fileRead = open(environment_Path, 'r')
    lines = fileRead.readlines()
    fileRead.close()

    # 修改url_macro文件
    fileWrite = open(environment_Path, 'w')
    for line in lines:

        if environment_pattern in line:

            # 环境配置
            fileWrite.write(line.replace(line, "%s %d\n" % (environment_pattern, enviroment_Type)))

        elif enviroment_Addr and (environment_addr_pattern in line):

            # 如果环境地址不为空, 则替换
            tempAddr = enviroment_Addr + PackageConfig.configDic[PackageConfig.ConfigItem_Environment_API_Path]
            fileWrite.write(line.replace(line, "%s @\"%s\"\n" % (environment_addr_pattern, tempAddr)))

        elif encrypt_pattern in line:

            # 加密配置
            fileWrite.write(line.replace(line, "%s %d\n" % (encrypt_pattern, encrypt_Type)))
        else:

            fileWrite.write(line)

    fileWrite.close()



######################### 修改App info.plist文件 #############################

def modifyAppInfoPlistFile(info_plist_path, appName):

    # 读取info.plist文件,并修改appName
    infoPlistDic = biplist.readPlist(info_plist_path)
    infoPlistDic["CFBundleDisplayName"] = appName

    # 写info.plist文件
    biplist.writePlist(infoPlistDic, info_plist_path)



######################### 修改渠道文件 #############################

def modifyAppChannelPlistFile(channel_plist_path, channel):


    # 读取渠道配置文件,channel
    infoPlistDic = biplist.readPlist(info_plist_path)
    infoPlistDic["channel"] = channel

    # 写渠道配置文件
    biplist.writePlist(infoPlistDic, info_plist_path)



