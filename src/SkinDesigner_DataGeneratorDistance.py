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
Use this component to generate data through a distance-based algorithm to be used in the Panel Controller Legacy version

    Args:
        _geometry: A list of grasshopper geometry or scene geometry that is used to find the closest distance to the current panel bay center point.
        minDist: A floating point value that defines the minimum possible distance allowed. Lower values will be clipped to this value. Default is 0.0
        maxDist: A floating point value that defines the maximum valid distance. Higher values will be ignored and will not affect that panel data. Default is 10 in scene units.
        multipliers: A list of floating point coeficients that modulate the distance value before applying it to the input data comming from the Panel DesignFunction component. The list of multipliers is applied sequentially to the panels.
        constrainToAxis: A unit vector specifying one or more axis to calculate the distance from.
    Returns:
        dataGenerator: A data generator algorithm that inputs into a Panel Controller Legacy component.

"""

ghenv.Component.Name = "SkinDesigner_DataGeneratorDistance"
ghenv.Component.NickName = 'DataGeneratorDistance'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Design Controllers"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

import Grasshopper.Kernel as gh
import rhinoscriptsyntax as rs
import System
import Rhino as rc
#import scriptcontext as sc
from types import *
import random
import copy
#import math
#import imp



class PanelDataFunction:
    
    __m_geometry = []
    __m_maxDist = 10
    __m_minDist = 0
    __m_globalMultiplier = 0
    __m_instanceMultiplierCounter = 0
    __m_constrainToAxis = None
    warningData = []
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        
        if constrainToAxis <> None : self.__m_constrainToAxis = constrainToAxis
        
        if _geometry <> []:
            for index, obj in enumerate(_geometry) :
                try:
                    if type(obj) == System.Guid:
                        if  not rs.IsObject(obj) : self.warningData.append("Invalid geometry at #"+ str(index)) ; continue
                        objData = rs.ObjectName(obj) #extract data if any
                        geo = rc.DocObjects.ObjRef(obj).Brep()
                        if geo == None : geo = rc.DocObjects.ObjRef(obj).Curve()
                        geo.SetUserString('Data', objData)
                        self.__m_geometry.append(geo)
                    else: 
                        obj.SetUserString('Data', " ")
                        self.__m_geometry.append(obj)
                except:
                    self.warningData.append("Invalid geometry object item #"+ str(index+1)) ; continue
        if self.__m_geometry == []: self.warningData.append("Missing '_geometry' input"); return

        if minDist <> None: self.__m_minDist = minDist
        if maxDist <> None: self.__m_maxDist = maxDist
        if multipliers <> []: self.__m_globalMultiplier = multipliers
        else: self.__m_globalMultiplier = [1]
        self.__m_instanceMultiplierCounter = 0

    def Reset(self):
        self.__m_instanceMultiplierCounter = 0

    #parameter value change based on proximity to modifier objects
    def Run(self, dataInstance=None, valueMin=None, valueMax=None, numSamples=None, skinInstance=None, panelFlags=None):
        
        #return if no proximity objects
        #if len(self.__m_geometry) == 0: return dataInstance
        
        currCellRow = skinInstance.GetProperty("SKIN_CURRENT_CELL_ROW")
        currCellColumn = skinInstance.GetProperty("SKIN_CURRENT_CELL_COLUMN")
        bayCornerPoints = skinInstance.GetCellProperty( currCellRow, currCellColumn, "CELL_CORNER_POINTS",)
        
        #return if one sample only (no variation)
        if numSamples == 1: return dataInstance      
        
        # Get mulitplier for this run instance (useful if muliplier list is provided)
        if self.__m_instanceMultiplierCounter >= len(self.__m_globalMultiplier) : self.__m_instanceMultiplierCounter = 0

        globalMultiplier = self.__m_globalMultiplier[self.__m_instanceMultiplierCounter]
        self.__m_instanceMultiplierCounter +=1
        
        
        #obtain panel center point to evaluate
        midDist = rs.VectorScale(rs.VectorCreate(bayCornerPoints[3],bayCornerPoints[0]),.5)
        centerPoint = rs.PointAdd(bayCornerPoints[0], midDist)
        
        
        #evaluate distance of panel to proximity objects, find closest object.
        dataMult = 1
        dataShift = 0
        finalCoef = None
        finalIsPositive = True #store positive/negative sign on distance data 
        for obj in self.__m_geometry:
            
            MIN_DIST = self.__m_minDist
            MAX_DIST = self.__m_maxDist
            DATA_MULT = dataMult
            
            #look for data stored on curves name (with format: MIN_DIST=float / MAX_DIST=float / DATA_MULT = float)
            datalist =[]
            objData = obj.GetUserString('Data')
            dataList = list(objData.rsplit("/"))
            for data in dataList : 
                if 'MIN_DIST' in data or 'MAX_DIST' in data or 'DATA_MULT' in data : 
                    codeObj= compile(data,'<string>','single') ; eval(codeObj)
            
            #is a curve?
            if obj.ObjectType == rc.DocObjects.ObjectType.Curve: 
                #paramCurve = 0.0
                success, paramCurve  = obj.ClosestPoint(centerPoint)
                closePoint = obj.PointAt(paramCurve)
                
            #is a surface/polysurface?
            elif obj.ObjectType == rc.DocObjects.ObjectType.Brep: 
                closePoint = obj.ClosestPoint(centerPoint)
                
            #get distance of current modifier object to current panel
            #if rs.IsBrep(obj): #is a surface/polysurface?
                #closePoint = rs.BrepClosestPoint(obj, centerPoint)[0]
                #dist = rs.Distance(closePoint, centerPoint)
            #elif rs.IsCurve(obj): #is a curve?
                #dist = rs.Distance(rs.EvaluateCurve(obj, rs.CurveClosestPoint(obj, centerPoint)), centerPoint)
            #else: continue # Invalid object, skip
            
            #register distance relative to one or more axis
            isPositive = True 
            if self.__m_constrainToAxis : 
                dist = (closePoint - centerPoint)*self.__m_constrainToAxis
                if type(dist) == rc.Geometry.Vector3d: dist = dist.Length
                isPositive = (True if dist > 0 else False) #store sign data separtately.
            else : dist = (closePoint - centerPoint).Length
            
            dist = abs(dist)
            
            if dist < MIN_DIST : dist = 0 #affect up to minuimum distance as if distance = 0
            if dist > MAX_DIST : continue #ignore if dist out of range
            
            # modulate data instance to 0-100% range times global and local multipliers
            coef = globalMultiplier*DATA_MULT*(1-dist/MAX_DIST)
            # if multiple objects affect same panel, keep the larger modifying value
            if finalCoef <> None :
                finalCoef = (max(finalCoef,coef) if DATA_MULT*globalMultiplier > 0 else min(finalCoef,coef))
            else: finalCoef = coef
            #update sign data if coef data updated
            if finalCoef == coef: finalIsPositive = isPositive
            
        if finalCoef == None : 
            if len(self.__m_geometry) == 0 : finalCoef  = 1-globalMultiplier #if no objects affect entire skin w/multiplier
            else: return dataInstance  #keep unchanged if geomtry objects don't affect panel
            
        newDataInstance = dataInstance + (valueMax-valueMin)*(finalCoef+dataShift)  # ecuation to create new data value
        
        #clamp values outside of range
        if  newDataInstance > max(valueMax, valueMin) : newDataInstance = max(valueMax, valueMin)
        if  newDataInstance < min(valueMax, valueMin) : newDataInstance = min(valueMax, valueMin)
        
        #snap new values back to sample steps.
        tmpList =[]
        dataStep = (valueMax-valueMin)/(numSamples-1)
        for i in range(numSamples):tmpList.append(i*dataStep+valueMin)
        
        mappedList = map(lambda x: abs(x-newDataInstance),tmpList)
        index = mappedList.index(min(mappedList))
        newDataInstance = tmpList[index]
        
        
        return (newDataInstance if finalIsPositive else -newDataInstance) 
        
        
dataGenerator = PanelDataFunction()

if dataGenerator.warningData <> []: 
    for warning in dataGenerator.warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)

if "Missing '_geometry' input" in dataGenerator.warningData: dataGenerator = None
print "Done"
