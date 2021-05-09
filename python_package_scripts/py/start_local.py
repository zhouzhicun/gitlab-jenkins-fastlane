
# -*- coding: utf-8 -*-

import os
import sys
import types
import datetime

import PackageConfig
import FileManager
import Package


cur_date = datetime.datetime.now().strftime("%Y_%m%d")
cur_time = datetime.datetime.now().strftime("%H%M")


def main():

    # 第一步: 配置相关路径， # 解析打包配置文件，  # 创建根目录
    localRootPath = os.environ['HOME'] + "/Desktop/package"

    # 解析打包配置文件
    configFilePath = os.path.dirname(sys.argv[0]) + "/PackageConfig.plist"
    PackageConfig.parse(configFilePath)

    FileManager.createRootPath(localRootPath)


    src_from = raw_input("请输入本地工程的根目录, 提示:将本地工程的根目录直接拖入控制台即可\n")
    src_from = src_from.strip()

    packages = raw_input("请输入包类型,例如10 11 20等，用空格隔开\n")
    packageTypeArr = packages.strip().split(" ")


    # 复制工程到根目录
    rootPath = FileManager.srcPath
    FileManager.copySrc(src_from, rootPath)

    # clean工程
    repositoryName = PackageConfig.configDic[PackageConfig.ConfigItem_RepositoryName]
    cur_srcPath = FileManager.srcPath + "/" + repositoryName
    Package.cleanProject(cur_srcPath)

    packageInfoArr = []
    for packageType in packageTypeArr:

        environment_type = int(packageType) / 10
        encrypt_type = int(packageType) % 10

        packageInfo = Package.PackageInfo(None, None, environment_type, encrypt_type)
        packageInfoArr.append(packageInfo)


    print("开始打包")
    for tempPackageInfo in packageInfoArr:
        tempPackageInfo.package(cur_date, cur_time)

    print("打包结束")
    print("当前时间为: " + datetime.datetime.now().strftime("%Y_%m%d_%H%M"))

    # # 上次到SVN
    # svn_root_path = PackageConfig.configDic[PackageConfig.ConfigItem_Package_SVN_Remote_Path]
    # FileManager.svn_commit(cur_date, cur_time, svn_root_path)


main()
