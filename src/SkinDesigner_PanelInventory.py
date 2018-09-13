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
Use this component to display all panel types generated to develop the skin solution with a count of haw many panels are panel
On bold are displayed the panels types that have standard dimensiosn (not custom sized).

    Args:
        _skinPanelData:  A list with information on panel types generated by the SkinGenerator component.  
        showCustom: A boolean that specifies if includes or excludes the custom sized panels.
        drawGeometry: A boolean that turns on/off drawing of panel types in the scene.
        drawBreps: A boolean that turns on/off outputing grasshopper geometry versions of the panel types.
        panelIndex: An integer that specifies which panel index in the list of panels generated to display. By default it shows all the panels in the list.
        locPoint A grasshoper Point object to indicate the start point location in the scene to draw  the panel types.
        
    Returns:
        Breps: A list of Breps of the panels created when drawBreps is turned on.
"""

ghenv.Component.Name = "SkinDesigner_PanelInventory"
ghenv.Component.NickName = 'PanelInventory'
ghenv.Component.Message = 'VER 0.5.00\nAug_24_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "04 | Display"



import Grasshopper.Kernel as gh
import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc
from types import *
SGLibPanel = sc.sticky["SGLib_Panel"]
SGLibDisplayUtilities = sc.sticky["SGLib_DisplayUtilities"]

PANEL_TYPES_ID=str(ghenv.Component.InstanceGuid)
warningData = []

def DeleteMockup():
    
    if not sc.sticky["PanelTypes_Data"+ PANEL_TYPES_ID] : return
        
    for data in sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] :
        if isinstance(data, SGLibPanel): data.HideAll() #same as deleting all panel objects
        elif rs.IsText(data) : rs.DeleteObject(data)
    

#initialize
sc.doc = rc.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

#init set up global variables
unitSystem = sc.doc.ModelUnitSystem
_UNIT_COEF = 1
if unitSystem == rc.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == rc.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
if unitSystem == rc.UnitSystem.Millimeters: _UNIT_COEF = 1000

if _skinPanelData == []: warningData.append( "'_skinPanelData' input data missing")

locP = None
if  type(_locPoint) == rc.Geometry.ArcCurve: 
    success, circle = _locPoint.TryGetCircle()
    locP = circle.Center
elif type(_locPoint) == rc.Geometry.Point3d : locP = _locPoint
else: warningData.append( "I need a circle or point for location")

if locP: offsetX, offsetY, offsetZ = locP

if showCustom == None: showCustom = True
Mockup_Bay = [] ; textTypes = []; frameCanvasCrvs = []
Breps = []
layoutRows = 15; rowCounter = 0
layoutColumns = 8; colCounter = 0
maxRowHeight = 0; firstRowHeight = 0; maxRowLength = 0
rowSeparation = 10; colSeparation= 10
margin = 20*_UNIT_COEF

if "PanelTypes_Data"+PANEL_TYPES_ID not in sc.sticky : sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] = []

DeleteMockup()
SGLibDisplayUtilities.BakeGeo([], "PanelTypes_Frame"+PANEL_TYPES_ID) #sticky field name to store baked objects based on panel name    
            
panelTypeCounter = 0
panelCounter = 0

if _skinPanelData <> [] and locP:
    try:

        for panelData in _skinPanelData :
            for i in range(len(panelData)):
                colCounter +=1
                panelTypeCounter +=1
                if panelIndex <> None and panelTypeCounter <> panelIndex: continue
                panelName = panelData[i][0].GetName()
                #print panelName
                isSurfacePanelMode = panelData[i][0].GetPanelProperty("SurfacePanelMode")
                if isSurfacePanelMode or panelName.find("-Width")>0 or panelName.find("-Height")>0 or panelName.find(" Left")>0 or panelName.find(" Right")>0: 
                    if showCustom or isSurfacePanelMode :fontHeight = rowSeparation/5 ; fontStyle=0 
                    else: continue #skip custom panel if showCustom off 
                else: fontHeight= rowSeparation/5*1.2 ; fontStyle = 1
                
                arrBoxPoints = [[offsetX, offsetY, offsetZ],[offsetX + panelData[i][0].GetPanelProperty("PanelWidth"), offsetY, offsetZ],\
                    [offsetX, offsetY, offsetZ+panelData[i][0].GetPanelProperty("PanelHeight")],\
                    [offsetX + panelData[i][0].GetPanelProperty("PanelWidth"), offsetY, offsetZ+panelData[i][0].GetPanelProperty("PanelHeight")]]
                    
                blockCount = len(panelData[i][0].GetPanelProperty("BlockInstances"))
                panelCounter += blockCount
                #create text info
                if drawGeometry:
                    
                    panelName = panelName.replace(" ", "\n\r", 1)
                    prevLayer = rs.CurrentLayer()
                    rs.CurrentLayer("GEO::_Canvas")
                    txtPlane = rs.PlaneFromFrame(rs.PointSubtract(arrBoxPoints[0],[0,0,rowSeparation/2]), (1,0,0), (0,0,1))
                    textTypes.append(rs.AddText(panelName + "\n\rCount: " + str(blockCount), txtPlane, fontHeight, font_style=fontStyle))
                    rs.CurrentLayer(prevLayer)
                #create panel copy
                Mockup_Bay.append(SGLibPanel())
                Mockup_Bay[len(Mockup_Bay)-1].Copy(panelData[i][0])
                panelPoints = Mockup_Bay[len(Mockup_Bay)-1].GetPanelProperty("PanelCornerPoints")
                alignXform = rc.Geometry.Transform.Translation(-min(panelPoints[0].X, panelPoints[2].X), 0, 0)
                tmpBoxPts = rs.PointArrayTransform(arrBoxPoints, alignXform)
                Mockup_Bay[len(Mockup_Bay)-1].MorphPanel(tmpBoxPts)
                #print i; print panelData
                Mockup_Bay[len(Mockup_Bay)-1].Draw(drawGeometry)
                panelBreps = Mockup_Bay[len(Mockup_Bay)-1].GetBreps()
                p1, p2 ,p4, p3 = arrBoxPoints

                xForm = rc.Geometry.Transform.Translation(offsetX, offsetY, offsetZ)
                xForm = alignXform*xForm
                panelPoints = list(xForm.TransformList(panelPoints))
                panelPoints.append(panelPoints[0])
                frameCanvasCrvs += SGLibDisplayUtilities.DrawCanvasGeo(panelPoints, panelBreps, None)
                
                if  drawBreps : Breps += panelBreps
                
                panelBbox = rc.Geometry.BoundingBox(panelPoints)
                maxRowHeight = panelBbox.Diagonal.Z if panelBbox.Diagonal.Z > maxRowHeight else maxRowHeight
                
                if colCounter < layoutColumns:
                    offsetX += panelBbox.Diagonal.X + colSeparation*_UNIT_COEF
                    
                else:
                    if panelTypeCounter == colCounter :
                        firstRowHeight = maxRowHeight
                    maxRowLength = offsetX+panelBbox.Diagonal.X-locP.X if offsetX+panelBbox.Diagonal.X-locP.X > maxRowLength else maxRowLength
                    offsetX = locP[0]
                    offsetZ -= maxRowHeight+rowSeparation*_UNIT_COEF
                    maxRowHeight = 0
                    colCounter = 0
        
        
        if drawGeometry: 
            if maxRowLength == 0:
                    maxRowLength = offsetX+panelBbox.Diagonal.X-locP.X if offsetX+panelBbox.Diagonal.X-locP.X > maxRowLength else maxRowLength
            sheetPts = [locP+rc.Geometry.Point3d(0,0, firstRowHeight), locP+rc.Geometry.Point3d(maxRowLength,0,firstRowHeight),\
                locP+rc.Geometry.Point3d(maxRowLength,0,offsetZ-locP.Z), locP+rc.Geometry.Point3d(0,0,offsetZ-locP.Z)]
            sheetPts = [pt+rc.Geometry.Vector3d(margins[0], 0, margins[1]) for pt, margins in zip(sheetPts,[[-margin,margin],[margin,margin],[margin,-margin],[-margin, -margin]])]
            sheetPts.append(sheetPts[0])
            sheetCrv = rc.Geometry.PolylineCurve(sheetPts)
            SGLibDisplayUtilities.BakeGeo(frameCanvasCrvs + [sheetCrv], "PanelTypes_Frame"+PANEL_TYPES_ID) #sticky field name to store baked objects based on panel name
    except:
        warningData.append( "Can not generate panel, check inputs")
        DeleteMockup()
        SGLibDisplayUtilities.BakeGeo([], "PanelTypes_Frame"+PANEL_TYPES_ID) #sticky field name to store baked objects based on panel name                
        raise

    sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] = Mockup_Bay + textTypes
else:
    DeleteMockup()
    SGLibDisplayUtilities.BakeGeo([], "PanelTypes_Frame"+PANEL_TYPES_ID) #sticky field name to store baked objects based on panel name                
     
#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc

if warningData <> []: 
    for warning in warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str(warning))
print str(panelTypeCounter) + " Panel Types Created"
print str(panelCounter) + " Total Panels"
print "Done"