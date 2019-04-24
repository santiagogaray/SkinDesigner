#
# SkinDesigner: A Plugin for Building Skin Design (GPL) started by Santiago Garay
# This component was written thanks to Mostapha Sadeghipour Roudsari creator of the Ladybug component.
# This file is part of SkinDesigner.
# 
# Copyright (c) 2017, Santiago Garay <sgaray1970@gmail.com> and Chris Mackey <Chris@MackeyArchitecture.com>
# SkinDesigner is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# SkinDesigner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with SkinDesigner; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
Code Developers and Beta Testers of new SkinDesigner components can use this component to remove old SkinDesigner components, add new SkinDesigner components, and update existing SkinDesigner components from a synced Github folder on their computer.
This component can also update outdated SkinDesigner components in an old Grasshopper file so long as the updates to the components do not involve new inputs or outputs.
-
Provided by SkinDesigner 0.0.65
    
    Args:
        sourceDirectory_: An optional address to a folder on your computer that contains the updated SkinDesigner userObjects. If no input is provided here, the component will download the latest version from GitHUB.
        _updateAllUObjects: Set to "True" to sync all the SkinDesigner userObjects in your Grasshopper folder with the GitHUB.
    Returns:
        readMe!: ...
"""

ghenv.Component.Name = "SkinDesigner_Update SkinDesigner"
ghenv.Component.NickName = 'updateSkinDesigner'
ghenv.Component.Message = 'VER 0.5.01\nApr_24_2019'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "05 | Update"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import scriptcontext as sc
import Grasshopper.Kernel as gh
import os
import shutil
import zipfile
import time
import urllib
import Grasshopper.Folders as folders
import System


monthList = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

def nukedir(dir, rmdir = True):
    # copied from 
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if file == '.' or file == '..': continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            nukedir(path)
        else:
            try:
                os.remove(path)
            except:
                pass
                #print 'Failed to remove ' + path
    if rmdir:
        try:
            os.rmdir(dir)
        except:
            pass

def getJD(month, day):
    numOfDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    return numOfDays[int(month)-1] + int(day)

def downloadSourceAndUnzip():
    """
    Download the source code from github and unzip it in temp folder
    """
    url = "https://github.com/santiagogaray/SkinDesigner/archive/master.zip"
    targetDirectory = os.path.join(folders.ClusterFolders[0] + 'SDgithub')
    
    # download the zip file
    print "Downloading the source code..."
    zipFile = os.path.join(targetDirectory, os.path.basename(url))
    
    # if the source file is just downloded then just use the available file
    download = True
    try:
        nukedir(targetDirectory, True)
    except:
        pass
    
    # create the target directory
    if not os.path.isdir(targetDirectory):
        os.mkdir(targetDirectory)
    
    if download:
        try:
            client = System.Net.WebClient()
            client.DownloadFile(url, zipFile)
            client.Dispose()
            if not os.path.isfile(zipFile):
                print "Download failed! Try to download and unzip the file manually form:\n" + url
                return
        except Exception, e:
            print `e` + "\nDownload failed! Try to download and unzip the file manually form:\n" + url
            return None, None
    
    #unzip the file
    with zipfile.ZipFile(zipFile) as zf:
        for f in zf.namelist():
            if f.endswith('/'):
                try: os.makedirs(f)
                except: pass
            else:
                zf.extract(f, targetDirectory)
    zf.close()
    
    userObjectsFolder = os.path.join(targetDirectory, r"SkinDesigner-master\userObjects")
    
    return userObjectsFolder, targetDirectory


def main(sourceDirectory, updateAllUObjects):
    targetDirectory = None
    if sourceDirectory == None:
        userObjectsFolder, targetDirectory = downloadSourceAndUnzip()
        if userObjectsFolder==None:
            return "Download failed! Read component output for more information!", False
    else:
        userObjectsFolder = sourceDirectory
    
    destinationDirectory = folders.ClusterFolders[0]
    
    # copy files from source to destination
    if not userObjectsFolder  or not os.path.exists(userObjectsFolder):
        return 'source directory address is not a valid address!', False
    
    srcFiles = os.listdir(userObjectsFolder)
    print 'Removing Old Version...'
    # remove userobjects that are currently removed
    fileNames = os.listdir(destinationDirectory)
    for fileName in fileNames:
        # check for skinDesigner userObjects and delete the files if they are not
        # in source anymore
        if fileName.StartsWith('SkinDesigner') and fileName not in srcFiles:
            fullPath = os.path.join(destinationDirectory, fileName)
            os.remove(fullPath)                
    
    print 'Updating your userObjects...'
    for srcFileName in srcFiles:
        # check for skinDesigner userObjects
        if srcFileName.StartsWith('SkinDesigner'):
            srcFullPath = os.path.join(userObjectsFolder, srcFileName)
            dstFullPath = os.path.join(destinationDirectory, srcFileName) 
            
            # check if a newer version is not aleady exist
            if not os.path.isfile(dstFullPath):
                shutil.copy2(srcFullPath, dstFullPath)
            # or is older than the new file
            elif os.stat(srcFullPath).st_mtime - os.stat(dstFullPath).st_mtime > 1:
                shutil.copy2(srcFullPath, dstFullPath)
    
    # Delete the old downloaded directory out of the userObjects folder.
    if targetDirectory != None:
        nukedir(targetDirectory)
    
    return "Done!" , True


if _updateAllUObjects == True:
    msg, success = main(sourceDirectory_, _updateAllUObjects)
    if not success:
        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, msg)
        print msg
    else:
        print msg
else:
    print " "
