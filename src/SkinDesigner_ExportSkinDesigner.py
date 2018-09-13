# SkinDesigner: A Plugin for Building Skin Design (GPL) started by Santiago Garay
# This component was written thanks to Giulio Piacentino a really helpful example.
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
Developers of skin generator can use this to export new userobjects to the master folder.
This component was written thanks to Giulio Piacentino a really helpful example.
-
    Args:
        components: Any output from a new  component that you wish to export. Right now, only one component can be connected at a time but you can input a "*" (without quotation marsk) to search all changed Ladybug components on a grasshopper canvas.
        export: Set to "True" to export components.
    Returns:
        readMe!: ...
"""

ghenv.Component.Name = "SkinDesigner_ExportSkinDesigner"
ghenv.Component.NickName = 'ExportSkinDesigner'
ghenv.Component.Message = 'VER 0.5.00\nSep_13_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "05 | Update"


try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import Grasshopper.Kernel as gh
import scriptcontext as sc
import shutil
import os
import uuid

UOFolder = "C:\\Users\\" + os.getenv("USERNAME") + "\\AppData\\Roaming\\Grasshopper\\UserObjects\\"
cs = gh.GH_ComponentServer()

#gh.GH_ComponentServer

exposureDict = {0 : ghenv.Component.Exposure.dropdown,
                1 : ghenv.Component.Exposure.primary,
                2 : ghenv.Component.Exposure.secondary,
                3 : ghenv.Component.Exposure.tertiary,
                4 : ghenv.Component.Exposure.quarternary,
                5 : ghenv.Component.Exposure.quinary,
                6 : ghenv.Component.Exposure.senary,
                7 : ghenv.Component.Exposure.septenary
                }




class Preparation(object):
    """ Set of functions to prepare the environment for running the studies"""
    def __init__(self):
        self.monthList = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        self.numOfDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
        self.numOfDaysEachMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.numOfHours = [24 * numOfDay for numOfDay in self.numOfDays]
    
    def giveWarning(self, warningMsg, GHComponent):
        w = gh.GH_RuntimeMessageLevel.Warning
        GHComponent.AddRuntimeMessage(w, warningMsg)
        
    def checkUnits(self):
        units = sc.doc.ModelUnitSystem
        if `units` == 'Rhino.UnitSystem.Meters': conversionFactor = 1.00
        elif `units` == 'Rhino.UnitSystem.Centimeters': conversionFactor = 0.01
        elif `units` == 'Rhino.UnitSystem.Millimeters': conversionFactor = 0.001
        elif `units` == 'Rhino.UnitSystem.Feet': conversionFactor = 0.305
        elif `units` == 'Rhino.UnitSystem.Inches': conversionFactor = 0.0254
        else:
            print 'Kidding me! Which units are you using?'+ `units`+'?'
            print 'Please use Meters, Centimeters, Millimeters, Inches or Feet'
            return
        print 'Current document units is in', sc.doc.ModelUnitSystem
        print 'Conversion to Meters will be applied = ' + "%.3f"%conversionFactor
        return conversionFactor
    
    def angle2north(self, north):
        try:
            # print north
            northVector = rc.Geometry.Vector3d.YAxis
            northVector.Rotate(math.radians(float(north)), rc.Geometry.Vector3d.ZAxis)
            northVector.Unitize()
            return math.radians(float(north)), northVector
        except Exception, e:
            # print `e`
            try:
                northVector = rc.Geometry.Vector3d(north)
                northVector.Unitize()
                return rc.Geometry.Vector3d.VectorAngle(rc.Geometry.Vector3d.YAxis, northVector, rc.Geometry.Plane.WorldXY), northVector
            except:
                    #w = gh.GH_RuntimeMessageLevel.Warning
                    #ghenv.Component.AddRuntimeMessage(w, "North should be a number or a vector!")
                    return 0, rc.Geometry.Vector3d.YAxis
    
    def setScale(self, scale, conversionFac = 1):
        try:
            if float(scale)!=0:
                try:scale = float(scale)/conversionFac
                except: scale = 1/conversionFac
            else: scale = 1/conversionFac
        except: scale = 1/conversionFac
        return scale
    
    def nukedir(self, dir, rmdir = True):
        # copied from 
        if dir[-1] == os.sep: dir = dir[:-1]
        files = os.listdir(dir)
        for file in files:
            if file == '.' or file == '..': continue
            path = dir + os.sep + file
            if os.path.isdir(path):
                self.nukedir(path)
            else:
                os.unlink(path)
        if rmdir: os.rmdir(dir)
    
    def readRunPeriod(self, runningPeriod, p = True, full = True):
        if not runningPeriod or runningPeriod[0]==None:
            runningPeriod = ((1, 1, 1),(12, 31, 24))
            
        stMonth = runningPeriod [0][0]; stDay = runningPeriod [0][1]; stHour = runningPeriod [0][2];
        endMonth = runningPeriod [1][0]; endDay = runningPeriod [1][1]; endHour = runningPeriod [1][2];
        
        if p:
            startDay = self.hour2Date(self.date2Hour(stMonth, stDay, stHour))
            startHour = startDay.split(' ')[-1]
            startDate = startDay.Replace(startHour, "")[:-1]
            
            endingDay = self.hour2Date(self.date2Hour(endMonth, endDay, endHour))
            endingHour = endingDay.split(' ')[-1]
            endingDate = endingDay.Replace(endingHour, "")[:-1]
            
            #if full:
            #    print 'Analysis period is from', startDate, 'to', endingDate
            #    print 'Between hours ' + startHour + ' to ' + endingHour
            #
            #else: print startDay, ' - ', endingDay
             
        return stMonth, stDay, stHour, endMonth, endDay, endHour
    
    def checkPlanarity(self, brep, tol = 1e-3):
        # planarity tolerance should change for different 
        return brep.Faces[0].IsPlanar(tol)
    
    def findDiscontinuity(self, curve, style, includeEndPts = True):
        # copied and modified from rhinoScript (@Steve Baer @GitHub)
        """Search for a derivatitive, tangent, or curvature discontinuity in
        a curve object.
        Parameters:
          curve_id = identifier of curve object
          style = The type of continuity to test for. The types of
              continuity are as follows:
              Value    Description
              1        C0 - Continuous function
              2        C1 - Continuous first derivative
              3        C2 - Continuous first and second derivative
              4        G1 - Continuous unit tangent
              5        G2 - Continuous unit tangent and curvature
        Returns:
          List 3D points where the curve is discontinuous
        """
        dom = curve.Domain
        t0 = dom.Min
        t1 = dom.Max
        points = []
        #if includeEndPts: points.append(curve.PointAtStart)
        get_next = True
        while get_next:
            get_next, t = curve.GetNextDiscontinuity(System.Enum.ToObject(rc.Geometry.Continuity, style), t0, t1)
            if get_next:
                points.append(curve.PointAt(t))
                t0 = t # Advance to the next parameter
        if includeEndPts: points.append(curve.PointAtEnd)
        return points
    
    def checkHour(self, hour):
        if hour<1: hour = 1
        elif hour%24==0: hour = 24
        else: hour = hour%24
        return hour

    def checkMonth(self, month):
        if month<1: month = 1
        elif month%12==0: month = 12
        else: month = month%12
        return month

    def checkDay(self, day, month, component = None):
        w = gh.GH_RuntimeMessageLevel.Warning
        if day<1:
            if component!=None:
                component.AddRuntimeMessage(w, "Day " + `day` + " is changed to 1.")
            day = 1
        if month == 2 and day > 28:
            if component!=None:
                msg = "Feb. has 28 days. The date is corrected by Ladybug."
                component.AddRuntimeMessage(w, msg)
            day = 28
            
        elif (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
            if component!=None:
                msg = self.monthList[month-1] + " has 30 days. The date is corrected by Ladybug."
                component.AddRuntimeMessage(w, msg)
            day = 30
            
        elif day > 31:
            if component!=None:
                msg = self.monthList[month-1] + " has 31 days. The date is corrected by Ladybug."
                component.AddRuntimeMessage(w, msg)
            day = 31
        
        return day
    
    def hour2Date(self, hour, alternate = False):
        numOfDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
        numOfHours = [24 * numOfDay for numOfDay in numOfDays]
        #print hour/24
        if hour%8760==0 and not alternate: return `31`+ ' ' + 'DEC' + ' 24:00'
        elif hour%8760==0: return 31, 11, 24
    
        for h in range(len(numOfHours)-1):
            if hour <= numOfHours[h+1]: month = self.monthList[h]; break
        try: month
        except: month = self.monthList[h] # for the last hour of the year
    
        if (hour)%24 == 0:
            day = int((hour - numOfHours[h]) / 24)
            time = `24` + ':00'
            hour = 24
        else:
            day = int((hour - numOfHours[h]) / 24) + 1
            minutes = `int(round((hour - math.floor(hour)) * 60))`
            if len(minutes) == 1: minutes = '0' + minutes
            time = `int(hour%24)` + ':' + minutes
        if alternate:
            time = hour%24
            if time == 0: time = 24
            month = self.monthList.index(month)
            return day, month, time
            
        return (`day` + ' ' + month + ' ' + time)
    
    def tupleStr2Tuple(self, str):
        strSplit = str[1:-1].split(',')
        return (int(strSplit[0]), int(strSplit[1]), int(strSplit[2]))
    
    def date2Hour(self, month, day, hour):
        # fix the end day
        numOfDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        # dd = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        JD = numOfDays[int(month)-1] + int(day)
        return (JD - 1) * 24 + hour
    
    def getHour(self, JD, hour):
        return (JD - 1) * 24 + hour
    
    def getJD(self, month, day):
        numOfDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        return numOfDays[int(month)-1] + int(day)


def exportToUserObject(component, targetFolder, lb_preparation):
    targetFolder = os.path.join(targetFolder, "userObjects")
    if not os.path.isdir(targetFolder): os.mkdir(targetFolder)
    
    def isNewerVersion(currentUO, component):
        # check if the component has a newer version than the current userObjects
        # version of the connected component
        if component.Message == None: return True
        if len(component.Message.split("\n"))<2: return True
        
        ghVersion, ghDate = component.Message.split("\n")
        ghCompVersion = map(int, ghVersion.split("VER ")[1].split("."))
        month, day, ghYear  = ghDate.split("_")
        # print version, date
        month = lb_preparation.monthList.index(month.upper()) + 1
        ghCompDate = int(lb_preparation.getJD(month, day))
        
        # in case there was no date for the userobject
        # the file will be considered older and will be overwrittern
        ghComponent = currentUO.InstantiateObject()
        # this is not the best way but works for now!
        # should be a better way to compute the component and get the message
        componentCode = ghComponent.Code.split("\n")
        
        UODate = ghCompDate - 1
        # version of the file
        for lineCount, line in enumerate(componentCode):
            if lineCount > 200: break
            if line.strip().startswith("ghenv.Component.Message"):
                #print line
                # print line.split("=")[1].strip().split("\n")
                version, date = line.split("=")[1].strip().split("\\n")
                
                # in case the file doesn't have an standard Ladybug message let it be updated
                try: UOVersion = map(int, version.split("VER ")[1].split("."))
                except: return True
                month, day, UOYear  = date.split("_")
                
                # should find the reason and fix it later
                if month == "SEPT": month = "SEP"
                
                month = lb_preparation.monthList.index(month.upper()) + 1
                UODate = int(lb_preparation.getJD(month, day))
                break
        
        # check if the version of the code is newer
        try:
            if int(ghYear.strip()) > int(UOYear[:-1].strip()):
                    return True
            elif ghCompDate > UODate:
                return True
            elif ghCompDate == UODate:
                for ghVer, UOVer in zip(UOVersion, UOVersion):
                    if ghVer < UOVer: return False
                return True
            else:
                print "\nThere is a newer userObject in Grasshopper folder that will be copied: " + currentUO.Path + "." + \
                      "\nUserObject version is: " +  version + " " + date + \
                      "\nThe component version is: "  +  ghVersion + " " + ghDate + ".\n"
                
                return False
        except:
            return True
            
    # check if the userObject is already existed in the folder
    try:
        filePath = os.path.join(UOFolder, component.Name + ".ghuser")
        currentUO = gh.GH_UserObject(filePath)
    except:
        # the userobject is not there so just create it
        currentUO = None
 
    if currentUO!=None:
        # if is newer remove
        if isNewerVersion(currentUO, component):
            # it has a newer version so let's remove the old one and creat a new userobject
            pass
            if not component.Category == "Maths":
                removeNicely = cs.RemoveCachedObject(filePath)
                if not removeNicely: os.remove(filePath)
        else:
            # there is already a newer version so just copy that to the folder instead
            # and return
            dstFullPath = os.path.join(targetFolder, component.Name + ".ghuser")
            shutil.copy2(filePath, dstFullPath)
            return
    
    # create the new userObject in Grasshopper folder
    uo = gh.GH_UserObject()
    uo.Icon = component.Icon_24x24
    
    try: uo.Exposure = exposureDict[int(component.AdditionalHelpFromDocStrings)]
    except:
        try:
            compCode = component.Code
            # this is so dirty
            exposureNumber = compCode.split("ghenv.Component.AdditionalHelpFromDocStrings")[1].split("\n")[0].replace("=", "").replace('"', "").strip()
            uo.Exposure = exposureDict[int(exposureNumber)]
            
        except:
            uo.Exposure = exposureDict[int(1)]
    
    uo.BaseGuid = component.ComponentGuid
    uo.Description.Name = component.Name
    uo.Description.Description = component.Description
    
    # if user hasn't identified the category then put it into honeybee as an unknown!
    if component.Category == "Maths":
        uo.Description.Category = "Honeybee"
    else:
        uo.Description.Category = component.Category
        
    if component.SubCategory == "Script":
        uo.Description.SubCategory = "UnknownBees"
    else:
        uo.Description.SubCategory = component.SubCategory
    
    uo.CreateDefaultPath(True)
    uo.SetDataFromObject(component)
    uo.SaveToFile()
    
    # copy the component over
    dstFullPath = os.path.join(targetFolder, component.Name + ".ghuser")
    shutil.copy2(filePath, dstFullPath)
    
    gh.GH_ComponentServer.UpdateRibbonUI()
    
    print "UserObject successfully added to: "


def exportToFile(component, targetFolder, lb_preparation):
    
    targetFolder = os.path.join(targetFolder, "src")
    if not os.path.isdir(targetFolder): os.mkdir(targetFolder)
    
    def isNewerVersion(componentCode, fileName):
        # check if the component has a newer version of source code
        # version of the connected component
        if component.Message == None: return True
        if len(component.Message.split("\n"))<2: return True
        
        ghVersion, ghDate = component.Message.split("\n")
        ghCompVersion = map(int, ghVersion.split("VER ")[1].split("."))
        month, day, ghYear  = ghDate.split("_")
        # print version, date
        month = lb_preparation.monthList.index(month.upper()) + 1
        ghCompDate = int(lb_preparation.getJD(month, day))
        
        # in case there was no date in the file
        # the file will be considered older and will be overwrittern
        # 
        pyFileDate = ghCompDate - 1
        
        # version of the file
        with open(os.path.join(targetFolder,fileName), "r") as pyFile:
            for lineCount, line in enumerate(pyFile):
                if lineCount > 200: break
                if line.strip().startswith("ghenv.Component.Message"):
                    # print line
                    # print line.split("=")[1].strip().split("\n")
                    version, date = line.split("=")[1].strip().split("\\n")
                    try:
                        pyFileVersion = map(int, version.split("VER ")[1].split("."))
                    except:
                        # in case the file doesn't have an standard Ladybug message
                        return True
                    month, day, pyYear  = date.split("_")
                    month = lb_preparation.monthList.index(month.upper()) + 1
                    pyFileDate = int(lb_preparation.getJD(month, day))
                    break
        
        # check if the version of the code is newer
        if int(ghYear.strip()) > int(pyYear[:-1].strip()):
                return True
        elif ghCompDate > pyFileDate:
            return True
        elif ghCompDate == pyFileDate:
            for ghVer, pyVer in zip(ghVersion, pyFileVersion):
                if ghVer < pyVer: return False
            return True
        else:
            print "\nThere is already a newer version in the folder for: " + fileName + "." + \
                  "\nCurrent file version is: " +  version + " " + date + \
                  "\nThe component version is: "  +  ghVersion + " " + ghDate + ".\n"
            
            return False
    
    
    fileName = component.Name + ".py"
    
    # code inside the component
    code = component.Code
    
    # check if the file already exist
    if os.path.isfile(os.path.join(targetFolder, fileName)):
        if not isNewerVersion(code, fileName):
            return False
            
    with open(os.path.join(targetFolder, fileName), "w") as pyoutf:
        if isinstance(code, unicode):
            code = code.encode('ascii','ignore').replace("\r", "")
        pyoutf.write(code)
    
    print "Exported " + fileName + " to: " + os.path.join(targetFolder, fileName)
    return True

def getAllTheComponents(onlyGHPython = True):
    components = []
    
    document = ghenv.Component.OnPingDocument()
    
    for component in document.Objects:
        if onlyGHPython and type(component)!= type(ghenv.Component):
            pass
        else:
            components.append(component)
    
    return components

def getListOfConnectedComponents(componentInputParamIndex = 0, onlyGHPython = True):
    # this function is edited version of Guilio's code from here:
    # [github link]
    components = []
    
    param = ghenv.Component.Params.Input[componentInputParamIndex]
    sources = param.Sources
    if sources.Count == 0: return components
    
    for source in sources:
        attr = source.Attributes
        if (attr is None) or (attr.GetTopLevel is None):
            pass
        else:
            component = attr.GetTopLevel.DocObject
    
    if component == None or (onlyGHPython and type(component) != type(ghenv.Component)):
            #collect only python components
            pass
    else:
        components.append(component)
    
    return components

def main(components):
    lb_preparation = Preparation()
    
    #targetFolder = 'F:\Research+Innovation\1_Skin_Generator\'
    
    if not os.path.isdir(targetFolder): os.mkdir(targetFolder)
        
    if components[0] == "*":
        ghComps = getAllTheComponents()
    else:
        ghComps = getListOfConnectedComponents()
    
    if len(ghComps)== 0: return "Found 0 components!"
    
    for ghComp in ghComps:
        fileExported = exportToFile(ghComp, targetFolder, lb_preparation)
        if fileExported:
            exportToUserObject(ghComp, targetFolder, lb_preparation)


if export and len(components)!=0:
    msg = main(components)
    ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, msg)
else:
    print "At the minimum one of the components are missing!"



















