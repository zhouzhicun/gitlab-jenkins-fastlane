
# -*- coding: utf-8 -*-

import os
import sys
import types
import datetime
import time



import AccountConfig
import PackageConfig
import Package
import FileManager


import ExchangeMail


reload(sys)
sys.setdefaultencoding('utf8')


cur_date = datetime.datetime.now().strftime("%Y_%m%d")
cur_time = datetime.datetime.now().strftime("%H%M")



######################  解析jenkins 配置信息  ###################################
def parsePackageInfo():

    Git_Branch = os.environ["Git_Branch"]
    TestIn_Encrypt = os.environ["TestIn_Encrypt"]
    TestIn_NoEncrypt = os.environ["TestIn_NoEncrypt"]
    TestOut_Encrypt = os.environ["TestOut_Encrypt"]
    TestOut_NoEncrypt = os.environ["TestOut_NoEncrypt"]
    PreProduct_Encrypt = os.environ["PreProduct_Encrypt"]
    PreProduct_NoEncrypt = os.environ["PreProduct_NoEncrypt"]
    Custom_Environment_List = os.environ.get("Custom_Environment_List")


    packageInfoArr = []
    packageInfo = None
    if TestIn_Encrypt == "true":
        packageInfo = Package.PackageInfo(None, None, 1, 1)
        packageInfoArr.append(packageInfo)

    if TestIn_NoEncrypt == "true":
        packageInfo = Package.PackageInfo(None, None, 1, 0)
        packageInfoArr.append(packageInfo)

    if TestOut_Encrypt == "true":
        packageInfo = Package.PackageInfo(None, None, 2, 1)
        packageInfoArr.append(packageInfo)

    if TestOut_NoEncrypt == "true":
        packageInfo = Package.PackageInfo(None, None, 2, 0)
        packageInfoArr.append(packageInfo)

    if PreProduct_Encrypt == "true":
        packageInfo = Package.PackageInfo(None, None, 3, 1)
        packageInfoArr.append(packageInfo)

    if PreProduct_NoEncrypt == "true":
        packageInfo = Package.PackageInfo(None, None, 3, 0)
        packageInfoArr.append(packageInfo)


    if Custom_Environment_List:
        environmentStringArr = Custom_Environment_List.split("\n")
        for temp in environmentStringArr:
            environment = temp.split("|")
            if len(environment) == 3:

                name = environment[0].strip()
                addr = environment[1].strip()
                encryptType = int(environment[2].strip())

                if encryptType == 0:
                    packageInfo = Package.PackageInfo(name, addr, 4, 0)
                    packageInfoArr.append(packageInfo)
                elif encryptType == 1:
                    packageInfo = Package.PackageInfo(name, addr, 4, 1)
                    packageInfoArr.append(packageInfo)
                elif encryptType == 2:
                    packageInfo = Package.PackageInfo(name, addr, 4, 0)
                    packageInfoArr.append(packageInfo)
                    packageInfo = Package.PackageInfo(name, addr, 4, 1)
                    packageInfoArr.append(packageInfo)


    return (Git_Branch, packageInfoArr)


def main():

    #第1步: 解析打包配置文件
    configFilePath = os.path.dirname(sys.argv[0]) + "/PackageConfig.plist"
    PackageConfig.parse(configFilePath)

    #第2步: 创建根目录
    FileManager.createRootPath(None)

    #第3步: 解析环境变量
    (tempBranch, packageInfoArr) = parsePackageInfo()
    if (not packageInfoArr) or (len(packageInfoArr) == 0):
        print("请选择打包类型！！！！！")
        return


    #第4步: git下载代码到本地root目录
    gitPath = PackageConfig.configDic[PackageConfig.ConfigItem_GitPath]
    branch = tempBranch or PackageConfig.configDic[PackageConfig.ConfigItem_Branch]
    rootPath = FileManager.srcPath

    # print("src = %s" % rootPath)
    # FileManager.git_clone(gitPath, branch, rootPath)
    git_clone_cmd = "git clone -b %s %s %s" % (branch, gitPath, rootPath)
    print git_clone_cmd
    os.system(git_clone_cmd)


    #第5步: clean工程
    repositoryName = PackageConfig.configDic[PackageConfig.ConfigItem_RepositoryName]
    cur_srcPath = FileManager.srcPath + "/" + repositoryName
    Package.cleanProject(cur_srcPath)

    # 第6步: 开始打包
    print("开始打包")
    for tempPackageInfo in packageInfoArr:
        tempPackageInfo.package(cur_date, cur_time)

    print("打包结束，开始上传")


    # 第7步: 上传到SVN
    svn_root_path = PackageConfig.configDic[PackageConfig.ConfigItem_Package_SVN_Remote_Path]
    commitPath = FileManager.svn_commit(cur_date, cur_time, svn_root_path)

    print("上传结束，开始发邮件")

    # 第8步: 发送邮件
    mailInfo = ExchangeMail.MailInfo()
    recipientList = os.environ.get("Recipients_List") or AccountConfig.EMAIL_DEFAULT_RecipientList
    mailInfo.sendMessage(subject="test",
                         body="本次打包上传路径:%s" % commitPath,
                         recipients=recipientList)

    print("邮件发送成功")
    print("当前时间为: " + datetime.datetime.now().strftime("%Y_%m%d_%H%M"))

main()




