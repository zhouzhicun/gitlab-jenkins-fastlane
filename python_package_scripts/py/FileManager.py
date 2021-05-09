
# -*- coding: utf-8 -*-

import os
import sys
import types
import datetime
import time

import PackageConfig

rootPath = ""       #根目录
srcPath = ""        #src目录
ipaPath = ""        #ipa输出目录
buildPath = ""      #build目录
localSVNPath = ""   #svn上传目录


######################### 创建或者删除目录 ##########################

def createPath(filePath):

    #如果目录已存在，则先删除， 然后在创建
    if os.path.exists(filePath):
        os.system("rm -rf %s" % filePath)
    os.makedirs(filePath)


def removePath(filePath):

    #如果本地根代码目录已存在，则删除
    if os.path.exists(filePath):
        os.system("rm -rf %s" % filePath)




######################### 创建根目录 #############################

def createRootPath(localRootPath):

    global rootPath
    global srcPath
    global ipaPath
    global buildPath
    global localSVNPath

    # 根目录
    tempRootPath = os.path.dirname(os.environ["WORKSPACE"]) + "/temp_" + os.environ["JOB_NAME"]
    rootPath = localRootPath or tempRootPath

    ipaPath = rootPath + "/ipa"
    srcPath = rootPath + "/mysrc"
    buildPath = rootPath + "/build"
    localSVNPath = rootPath + "/svn"

    createPath(rootPath)
    createPath(ipaPath)
    createPath(srcPath)
    createPath(buildPath)
    createPath(localSVNPath)



####################### 下载代码 ################################


#从git上下载源码到本地
def git_clone(gitPath, branch, rootPath):

    print("开始Git下载...")
    print gitPath
    print branch
    print rootPath
    os.system("git clone -b %s %s %s" % (branch, gitPath, rootPath))



#从本地复制源码到本地
def copySrc(projectPath, rootPath):

    print ("开始复制本地工程...")
    os.system("cp -rf %s %s" % (projectPath, rootPath))




##################### 上传至svn服务器  ###########################

def svn_commit(curDate, curTime, remote_svn_root_path):

    #1 创建本次ipa的远端svn目录

    curSVNPath = remote_svn_root_path + "/" + curDate + "/" + curTime
    os.system("svn mkdir --parents %s -m \"创建ipa包目录\"" % curSVNPath)

    #2 checkout刚刚创建的svn目录到本地
    os.system("svn checkout %s %s" % (curSVNPath, localSVNPath))


    #3 复制ipa包目录到本地svn目录
    os.system('cp -rf %s %s' % (ipaPath, localSVNPath))

    #4 svn提交
    os.chdir(localSVNPath)
    os.system('svn add *')
    os.system('svn commit -m \"提交测试包\"')


    return curSVNPath
