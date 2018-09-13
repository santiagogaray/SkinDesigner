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
Use this component to display all panel types used to generate the skin. Also a count of each panelis provided
On bold are dicplayed the panels defined as Panel objects. The additional panels created by Skin_Automata

-

    Args:
        SkinPanel_List: List  
        Loc: ID of point object that defines mock up location

    Returns:
        Nothing
"""

ghenv.Component.Name = "SkinDesigner_SkinPanelIndexViewer"
ghenv.Component.NickName = 'SkinPanelIndexBrepViewer'
ghenv.Component.Message = 'VER 0.5.00\nSep_13_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "04 | Display"



import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
from types import *
SGLibPanel = sc.sticky["SGLib_Panel"]
import copy
import math

PANEL_TYPES_ID=str(ghenv.Component.InstanceGuid)

        
 
    

#initialize
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

if  LocCircle: 
    Loc = LocCircle.Center
    offsetX = Loc.X ; offsetY = Loc.Y ; offsetZ = Loc.Z
else: print "I need a circle for location"
if _panelIndex <> None : pIndex = _panelIndex
else : pIndex = 1 

Mockup_Bay = [] ; textTypes = [] 


WallGeo =  []
WindowGeo = []
ShadingGeo = []
ShadingGeo = []
PanelGeo = []

for PPData in PostProcData:
    
    if isinstance(PPData, list) and len(PostProcData) and "LBHB_PanelsOutput" in PPData[0]:
        
        SkinPanel_List = PPData[1]
        panel = None ; pCounter = 0
        for panelData in SkinPanel_List :
            for i in range(len(panelData)):
                
                
                panelName = panelData[i][0].GetName()
                if (panelName.find("-Width")>0 or panelName.find("-Height")>0): 
                    if ShowCustom :fontHeight = 0.5 ; fontStyle=0 ; pCounter +=1
                    else: continue #skip custom panel if ShowCustom off 
                else: fontHeight= .6 ; fontStyle = 1; pCounter +=1
                
                if pCounter == _panelIndex :
                    
                    panel = panelData[i][0]; break
                    
        if panel:
            
            for ang in angle:
                widthOffset = panel.GetPanelProperty("PanelWidth")/2
                if ang == None : ang = 0
                arrBoxPoints = [[offsetX-widthOffset, offsetY, offsetZ],[offsetX + widthOffset, offsetY, offsetZ],\
                    [offsetX-widthOffset, offsetY, offsetZ+panel.GetPanelProperty("PanelHeight")],\
                    [offsetX + widthOffset, offsetY, offsetZ+panel.GetPanelProperty("PanelHeight")]]
                    
                xform = rs.XformTranslation((0,-LocCircle.Radius, 0))
                arrBoxPoints = rs.PointArrayTransform(arrBoxPoints, xform)
                xform = Rhino.Geometry.Transform.Rotation(math.radians(ang), Rhino.Geometry.Vector3d.ZAxis, Loc)
                for point in arrBoxPoints:
                    point.Transform(xform)
                
                #create text info
                #rs.CurrentLayer("_P_0")
                #panelName = panel.GetName()
                #textTypes.append(rs.AddText(panelName, rs.PointSubtract(arrBoxPoints[0], [0,1,0]), fontHeight, font_style=fontStyle))
                #rs.RotateObject(textTypes[len(textTypes)-1], rs.TextObjectPoint(textTypes[len(textTypes)-1]), 270)
                
                #create and draw panel selected
                newPanel = SGLibPanel()
                newPanel.Copy(panel)
                newPanel.MorphPanel(arrBoxPoints)
                newPanel.Draw()

                #collect relevant objects 
                WallGeo.extend(newPanel.GetBreps("Wall"))
                WindowGeo.extend(newPanel.GetBreps("Window"))
                ShadingGeo.extend(newPanel.GetBreps("Shading"))
                ShadingGeo.extend(newPanel.GetBreps("Mullions"))
                rg = Rhino.Geometry
                pt1, pt2, pt3, pt4= arrBoxPoints  
                PanelGeo.append(rg.Brep.CreateFromCornerPoints(rg.Point3d(pt1[0],pt1[1],pt1[2]), rg.Point3d(pt2[0],pt2[1],pt2[2]),\
                    rg.Point3d(pt4[0],pt4[1],pt4[2]), rg.Point3d(pt3[0],pt3[1],pt3[2]), sc.doc.ModelAbsoluteTolerance))



#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc


print "Done"