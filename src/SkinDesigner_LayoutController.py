# SkinDesigner: A Plugin for Building Skin Design (GPL) started by Santiago Garay

# This file is part of SkinDesigner.
# 
# Copyright (c) 2017, Santiago Garay <sgaray1970@gmail.com> 
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
Use this component to specify a layout pattern to a skin solution.

    Args:
        _layoutType: A layoutType component providing a layout algorithm such as DataPattern or DataRandom components.
        filter: A list of integers representing the panel bay ID numbers (based on their input number in SkinGenerator) that will be affected by the Layout Controller. By default, all panel bays will be affected.
        layoutRegions : A list of geometry objects that limit the area of application of the Layout Controller on the SkinGenerator surfaces. Grasshopper Surface, polysurface and curve types are accepted as well as Rhino scene ID versions of these geometry types. If no modifier geometry is specified, the algorithm is aplied on all SkinGenerator surfaces.
        regionsDistanceTH : A floating point number that specifies the distance between the panel center point and the closest point to the region geometry. Larger numbers will detect regions that don't tightly follow the facade surfaces. Defalt value is 0.1 meters.
        regionsEdgeDithering: A floating point number that specifies the blending between the modified and unmodified areas created by the region objecs. The default value is 0.0
    Returns:
        layoutController: A layoutController object to be connected to the SkinGenerator component.

"""

ghenv.Component.Name = "SkinDesigner_LayoutController"
ghenv.Component.NickName = 'LayoutController'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Design Controllers"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import Grasshopper.Kernel as gh
import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc
from types import *
import random
import copy
import math
import System

#init set up global variables
sc.doc = rc.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
_UNIT_COEF = 1
if unitSystem == rc.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == rc.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
if unitSystem == rc.UnitSystem.Millimeters: _UNIT_COEF = 1000
sc.doc = ghdoc


try:
    SGLibDesignFunction = sc.sticky["SGLib_DesignFunction"]
except:
    ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,"I need SkinDesigner_SkinDesigner component")
else: 

    class LayoutDesignFunction(SGLibDesignFunction):
        global _UNIT_COEF
        __m_modifierObjects = []
        __m_functionCall = ''
        __m_functionType = ''
        __m_falloffRadius = 0
        __m_filterBayID_List = []
        __m_randomObject = None
        __m_randomSeed = 1
        __m_DataFunction = None
        __m_modifierDistThreshold = 0.1 * _UNIT_COEF
        warningData = []
        
        #CONSTRUCTOR -------------------------------------------------------------------------------------------
        def __init__(self):
            
            sc.doc = rc.RhinoDoc.ActiveDoc
    
            self.__m_functionType = 'Layout'
            if layoutRegions : self.__m_modifierObjects = layoutRegions
                
            if regionsDistanceTH : self.__m_modifierDistThreshold = regionsDistanceTH
            
            for index, obj in enumerate(self.__m_modifierObjects) :
                try:
                    if type(obj) == System.Guid:
                        if  not rs.IsObject(obj) : 
                            self.warningData.append("Invalid 'layoutRegions' value at #"+ str(index+1))
                            self.__m_modifierObjects[index] = None
                            continue
                        objData = rs.ObjectName(obj) #extract data if any
                        geo = rc.DocObjects.ObjRef(obj).Brep()
                        if geo == None : geo = rc.DocObjects.ObjRef(obj).Curve()
                        geo.SetUserString('Data', objData)
                        self.__m_modifierObjects[index] = geo
                    else: obj.SetUserString('Data', " ")
                except:
                    self.warningData.append("Invalid 'layoutRegions' value at #"+ str(index+1))
                    self.__m_modifierObjects[index] = None
                    continue
            try: 
                while True: self.__m_modifierObjects.remove(None)
            except: pass
            
            if regionsEdgeDithering <> None : self.__m_falloffRadius = regionsEdgeDithering 
            if filter : self.__m_filterBayID_List = filter
            self.__m_randomObject = random.Random()    #Global Random generator object
            self.__m_randomObject.seed(self.__m_randomSeed)
    
            if _layoutType:
                if _layoutType.__class__.__name__ <> "LayoutDataFunction":
                    self.warningData.append("Invalid 'layoutType' input")
                    self.__m_DataFunction = None
                else : self.__m_DataFunction = _layoutType
            else: self.warningData.append("Missing 'layoutType' input")
            sc.doc = ghdoc
            
            
        def IsLayoutType(self):
            if self.__m_functionType == 'Layout': return True
            return False
            
            
        def IsPanelType(self):
            if self.__m_functionType == 'Panel': return True
            return False        
    
        def Reset(self):
            if self.__m_DataFunction: 
                param = self.__m_DataFunction.GetParameter('RandomSeed')
                if param : self.__m_randomObject.seed(param)
            
            
        #Selection of panel bay base on proximity to modifier curves
        #Refer to Skin API for skinInstance properties available (GetProperty and GetCellProperty)     
        def Run(self, PanelBay_List, currentBay, skinInstance):
            
            modDistTolerance = self.__m_modifierDistThreshold
            level = skinInstance.GetProperty("SKIN_CURRENT_CELL_ROW")  
            inLevelIndex = skinInstance.GetProperty("SKIN_CURRENT_CELL_COLUMN") 
            bayIndex = skinInstance.GetProperty("SKIN_CURRENT_BAY_INDEX")
            ptPanel = skinInstance.GetCellProperty(level, inLevelIndex, "CELL_CORNER_POINTS")
            defaultBayList = skinInstance.GetProperty("BAY_LIST")
            
            # new bay index passed in to this function via currentBay, currentBay is modified by design functions when a panel bay has to be changed.
            # (bayIndex is the original bay index at this cell location before design functions potentialty changed it).
            newBayIndex = PanelBay_List.index(currentBay)  
            if self.__m_DataFunction == None : return [PanelBay_List[bayIndex], bayIndex]          
            
            #check if bayindex should not be changed (bayStayList)
            if self.__m_filterBayID_List <> []:
                filterBayList = copy.deepcopy(self.__m_filterBayID_List)
                for i in range(len(filterBayList)) : filterBayList[i] -= 1 #convert to cero based list
                if newBayIndex not in filterBayList : return [PanelBay_List[newBayIndex], bayIndex]
            
            
            rndVal = self.__m_randomObject.random()# 0-1 random base value for algorithm
            
            #obtain panel center point to evaluate
            midDist = rs.VectorScale(rs.VectorCreate(ptPanel[3],ptPanel[0]),.5)
            centerPoint = rs.PointAdd(ptPanel[0], midDist)  
          
            #multiple curves can be tested simultaneosly with algorithm
            dist = 0 ; flagPanel = False  
            panelWidth = abs(rs.Distance(ptPanel[0],ptPanel[1]))
            panelHeight = abs(rs.Distance(ptPanel[1],ptPanel[3]))
            panelPlane=rs.PlaneFromPoints(ptPanel[0], ptPanel[1], ptPanel[2]) #panel bay plane
            
            if self.__m_modifierObjects == [] :
                newBayIndex = self.__m_DataFunction.Run(PanelBay_List, [] , level, inLevelIndex,  defaultBayList, self.__m_randomObject, bayIndex, panelPlane) 
                if newBayIndex >= len(PanelBay_List) :
                    self.warningData.append("Invalid panel bay id value: newBayIndex - default panel id used")
                    return [PanelBay_List[bayIndex], bayIndex]  
                return [PanelBay_List[newBayIndex], bayIndex]  
            
            for obj in self.__m_modifierObjects :
                
                #if not rs.IsObject(obj) : print "Invalid modifier object"; continue
                #look for falloff and bay data stored on curves name (with format: FALLOFF=float, BAY_LIST=integer)
                datalist =[]
                objData = obj.GetUserString('Data')
                dataList = list(objData.rsplit("/"))
                FALLOFF = self.__m_falloffRadius
                for data in dataList : 
                    if 'FALLOFF' in data: codeObj= compile(data,'<string>','single') ; eval(codeObj)
                    
                if FALLOFF > -1 : # a 0 value will skip the gradient check on current curve
                
                    #is a curve?
                    if obj.ObjectType == rc.DocObjects.ObjectType.Curve: 
                        #if  a flat closed curve in same plane as panel catch all points inside
                        if obj.IsClosed and obj.IsPlanar(sc.doc.ModelAbsoluteTolerance) and obj.IsInPlane(panelPlane, sc.doc.ModelAbsoluteTolerance):
                            result =  obj.Contains(centerPoint, panelPlane)
                            if result == rc.Geometry.PointContainment.Inside or result == rc.Geometry.PointContainment.Coincident : flagPanel = True
                        if flagPanel == False:
                            paramCurve = 0.0
                            success, paramCurve  = obj.ClosestPoint(centerPoint)
                            closePoint = obj.PointAt(paramCurve)
                            dist = abs((closePoint - centerPoint).Length)
                            if not obj.IsClosed: 
                                #open curves flag panels with distance to panel center point <1/2 panel size
                                heightDist = abs(closePoint.Z - centerPoint.Z)+ sc.doc.ModelAbsoluteTolerance 
                                widthDist = abs((closePoint - rc.Geometry.Point3d(centerPoint.X, centerPoint.Y, closePoint.Z)).Length) + sc.doc.ModelAbsoluteTolerance 
                                if heightDist < panelHeight/2 and widthDist < panelWidth/2: flagPanel = True
                        
                    #is a surface/polysurface?
                    elif obj.ObjectType == rc.DocObjects.ObjectType.Brep: 
                        #get distance of current modifier object to current panel center point
                        closePoint = obj.ClosestPoint(centerPoint)
                        dist = abs((closePoint - centerPoint).Length)
                        if dist < sc.doc.ModelAbsoluteTolerance + modDistTolerance  : flagPanel = True
                        
                    # Invalid object, skip
                    else: continue 
                    
                
                    #RANDOMLY SELECT THE BLOCKS BASED ON THEIR PROXIMITY TO THE GRADIENT CENTERPOINT. 
                    #dblDist = rs.Distance(rs.EvaluateCurve(obj, rs.CurveClosestPoint(obj, centerPoint)), centerPoint)
                    if flagPanel == False and FALLOFF>0:
                        if rndVal > dist/FALLOFF : flagPanel = True
                        elif rndVal > dist-FALLOFF/rndVal/15 : flagPanel = True
                
                #replace bayindex data for this panel depending on data specified (generic or specifc index)
                if flagPanel :
                    flagPanel = False
                    PATTERN = []
                    for data in dataList : 
                        if 'PATTERN' in data: 
                            codeObj= compile(data,'<string>','single') ; eval(codeObj) 
                    newBayIndex = self.__m_DataFunction.Run(PanelBay_List, PATTERN, level, inLevelIndex, defaultBayList, self.__m_randomObject, bayIndex, panelPlane)        
            
            
            #check for invalid id values         
            if newBayIndex >= len(PanelBay_List) :
                self.warningData.append("Invalid panel bay id value: newBayIndex - default panel id used")
                return [PanelBay_List[bayIndex], bayIndex]  

            #return the new panel bay and keep bay index unchanged  
            return [PanelBay_List[newBayIndex], bayIndex]   
    
            
    
    layoutController = LayoutDesignFunction()
    if layoutController.warningData <> []: 
        for warning in layoutController.warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        
    if "Invalid 'layoutType' input" in layoutController.warningData or "Missing 'layoutType' input" in layoutController.warningData : layoutController = None

print "Done"
