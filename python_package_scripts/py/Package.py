# -*- coding: utf-8 -*-


import os
import sys
import types
import datetime

import thread
import threading

import FileManager
import PackageConfig
import AppProjectConfig




def cleanProject(project_root_path):

    print("clean...")
    os.chdir (project_root_path)
    os.system ("xcodebuild clean -project Pods/Pods.xcodeproj -sdk iphoneos")
    os.system ("xcodebuild clean -sdk iphoneos")


class PackageInfo:

    def __init__(self, environmentName, environmentAddr, environmentType, encryptType):
        self.environmentName = environmentName
        self.environmentAddr = environmentAddr
        self.environmentType = environmentType
        self.encryptType = encryptType


    def package(self, curDate, curTime):

        folder = ''
        if self.environmentName and self.environmentAddr:
            #自定义环境
            folder = self.environmentName + "_" + str(self.encryptType)
        else:
            #固定环境
            folder = str(self.environmentType) + str(self.encryptType)

        # 创建本次打包的工作目录
        curWorkspacePath = FileManager.buildPath + "/" + folder
        FileManager.createPath(curWorkspacePath)

        #复制代码到当前工作目录下
        repositoryName = PackageConfig.configDic[PackageConfig.ConfigItem_RepositoryName]
        cur_srcPath = FileManager.srcPath + "/" + repositoryName
        FileManager.copySrc(cur_srcPath, curWorkspacePath)

        #获得当前工程目录
        curProjectPath = curWorkspacePath + "/" + repositoryName
        curBuildPath = curWorkspacePath + "/build"

        # 第一步: 获取appName, ipa包名
        defaultAppName = PackageConfig.configDic[PackageConfig.ConfigItem_DefaultAppName]
        projectName = PackageConfig.configDic[PackageConfig.ConfigItem_ProjectName]
        (curAppName, curIpaPackageName) = \
            AppProjectConfig.buildAppName(curDate,
                                        curTime,
                                        defaultAppName,
                                        projectName,
                                        self.environmentName,
                                        self.environmentType,
                                        self.encryptType)

        # 第二步: 修改App配置文件
        environmentAddrPattern = PackageConfig.configDic[PackageConfig.ConfigItem_Environment_Address_pattern]
        environmentPattern = PackageConfig.configDic[PackageConfig.ConfigItem_Environment_Pattern]
        encryptPattern = PackageConfig.configDic[PackageConfig.ConfigItem_Open_Encrypt_pattern]
        AppProjectConfig.modifyAppConfigFile(curProjectPath,
                                             self.environmentAddr,
                                             self.environmentType,
                                             self.encryptType,
                                             curAppName)

        # 第三步: 打包
        self.buildPackage(curProjectPath, curBuildPath, curIpaPackageName)




    def buildPackage(self, project_root_path, build_path, ipa_package_name):


        FileManager.createPath(build_path)

        print("编译...")
        os.chdir (project_root_path)
        os.system ("xcodebuild -project Pods/Pods.xcodeproj build")

        #证书签名
        codeSignIdentity = PackageConfig.configDic[PackageConfig.ConfigItem_CodeSignIdentity]
        os.system ("xcodebuild -sdk iphoneos -configuration Release CODE_SIGN_IDENTITY=\"%s\"" % codeSignIdentity)
        os.system ("cp -rf build/Release-iphoneos/*.app %s" % build_path)
        os.system ("cp -rf build/Release-iphoneos/*.app.dSYM %s" % build_path)


        print("打包...")
        os.chdir (build_path)

        ipaPath = FileManager.ipaPath
        os.system ("mkdir Payload")
        os.system ("cp -rf *.app Payload")
        os.system ("zip -r %s.ipa Payload" % ipa_package_name)
        os.system ("cp -rf %s.ipa %s" % (ipa_package_name, ipaPath))
        os.system ("rm -rf Payload")
        os.system ("rm -rf %s.ipa" % ipa_package_name)

        #删除build目录
        #PackageConfig.removePath(build_path)








