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
# Shading
"""
Use this component to generate a shade object to be added to a panel

    Args:
        layerName: A string indicating the layer the shade geometry will use when drawn in the scene. Default is _P_Shading
        width: A floating point value that represents a shade object's horizontal dimension in scene units. Default is 0.25m (10 inches aprox.)
        thickness: A floating point value that represents a shade object's  vertical dimension in scene units. Default value is 0.025m (1 inch)
        offsetFromWall: A floating point value that represenets a separation distance from panel wall's exterior surface  (not including panel systems applied).Default value is 0.025 m (1 inch)
        verticalOrientation: A boolean to turn on/off vertical orientation of the shade. Default is False (horizontal).
        windowShade: A boolean to turn on/off fromLeftEdge, fromBottomEdge and fromEdgreEnd values to be measured relative to the window bottom/left corner instead of realtive to the panel bottom/left corne. Deafult is False (dimensions are considered relative to the panel)
        fromLeftEdge: A floating point value indicating the separation of the shade from the left edge of the panel or the window if it is a window shade. Default value is 0.0. Also negative values are used to set dimensions from the panel or window right edge. 
        fromBottomEdge:  A floating point value indicating the separation of the shade from the bottom edge of the panel or the window if it is a window shade. Default value depends on shade orientation: In horizotnal shades it is the panel height (top of panel) or window height (top of window) if it is a window shade. In vertical shades default value is is 0.0. Also negative values are used to set dimensions from the top of panel or window.
        fromOppositeEdge:  A floating point value indicating the separation of the shade from the opposite edge of the panel or the window if it is a window shade. Default value is 0.0 (no separation ).
        rotation: A floating point value indicating the rotation around the shade's long axis, with center at the mid point of the shade's width. Default is 0.0
    Returns:
        shadingSystem: A list with shading data packed to be connected to a Panel component shadingSystem input

"""


ghenv.Component.Name = "SkinDesigner_Shading"
ghenv.Component.NickName = 'Shading'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "3"
except: pass

import Grasshopper.Kernel as gh
import GhPython
import scriptcontext as sc
import Rhino

# automnatically set the right input names and types (when using + icon) 

numInputs = ghenv.Component.Params.Input.Count
if numInputs: 
    accessList = ghenv.Component.Params.Input[0].Access.list
    accessItem = ghenv.Component.Params.Input[0].Access.item
    typeFloat = GhPython.Component.NewFloatHint()
    typeVector3d = gh.Parameters.Hints.GH_Vector3dHint()
    typeString = GhPython.Component.NewStrHint()
    typeBool = gh.Parameters.Hints.GH_BooleanHint_CS()
    typeVector = gh.Parameters.Hints.GH_Vector3dHint()

for input in range(numInputs):
    access = accessList
    typeHint = typeString 
    if input == 0: inputName = 'width'; access = accessItem; typeHint = typeFloat
    elif input == 1: inputName = 'thickness'; access = accessItem; typeHint = typeFloat
    elif input == 2: inputName = 'rotation'; access = accessItem; typeHint = typeFloat
    elif input == 3: inputName = 'offsetFromWall'; access = accessItem; typeHint = typeFloat
    elif input == 4: inputName = 'verticalOrientation'; access = accessItem; typeHint = typeBool  
    elif input == 5: inputName = 'windowShade'; access = accessItem; typeHint = typeBool  
    elif input == 6: inputName = 'layerName'; access = accessItem
    elif input == 7: inputName = '------------------------'
    elif input == 8: inputName = 'fromLeftEdge' ; access = accessItem
    elif input == 9: inputName = 'fromBottomEdge' ; access = accessItem
    elif input == 10: inputName = 'fromOppositeEdge'; access = accessItem
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    ghenv.Component.Params.Input[input].TypeHint = typeHint
        
ghenv.Component.Attributes.Owner.OnPingDocument()


#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == Rhino.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
if unitSystem == Rhino.UnitSystem.Millimeters: _UNIT_COEF = 1000
sc.doc = ghdoc

try:
    if layerName == None: layerName = "_P_Shading" 
except: layerName = "_P_Shading"
try:
    if width == None : width = 3/12*_UNIT_COEF
except: width = 3/12*_UNIT_COEF
try:
    if thickness == None : thickness = .025*_UNIT_COEF
except: thickness = .025*_UNIT_COEF
try:
    if offsetFromWall == None : offsetFromWall = .025*_UNIT_COEF
except: offsetFromWall = .025*_UNIT_COEF

try: 
    if verticalOrientation == True : shadingType = "VerticalShade"
    else : shadingType = 'HorizontalShade'    
except : verticalOrientation = False; shadingType = 'HorizontalShade'
try:
    if windowShade == None: windowShade = False
except: windowShade = False
try: 
    if fromLeftEdge == None : fromLeftEdge = 0.0
except: fromLeftEdge = 0.0
try: 
    fromBottomEdge
except: fromBottomEdge = None

if fromBottomEdge == None : 
    if windowShade==False : 
        if verticalOrientation : fromBottomEdge = 0.0
        else : fromBottomEdge = 'PanelHeight'
    else : 
        if  verticalOrientation : fromBottomEdge = 0.0
        else : fromBottomEdge = -0.01
try:
    if fromOppositeEdge == None : fromOppositeEdge = 0.0
except: fromOppositeEdge = 0.0

#window shade?

if windowShade == True:
    if shadingType == 'HorizontalShade' : shadingType = 'HorizontalWindowShade'
    elif shadingType == 'VerticalShade' : shadingType = 'VerticalWindowShade'

fromEdge = fromOppositeEdge
fromLeft = fromLeftEdge
fromBottom = fromBottomEdge
fromBottomEdge = None
angleRot = 0
#rotation data
try:
    if rotation <> None:  angleRot = rotation
except: pass

#shade ends shifting data
shiftEndVectors = [None, None]
try:
    if shiftEnd1 == None :shiftEndVectors[0] = [0,0,0]
    else: shiftEndVectors[0] = [shiftEnd1[0], shiftEnd1[1], shiftEnd1[2]]
except: shiftEndVectors[0] = [0,0,0]
try:
    if shiftEnd2 == None : shiftEndVectors[1] = [0,0,0]
    else: shiftEndVectors[1] = [shiftEnd2[0], shiftEnd2[1], shiftEnd2[2]]
except: shiftEndVectors[1] = [0,0,0]



# WindowData(wd) = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess 

shadingSystem = "AddShadingType('" + shadingType +"', layerName='"+ layerName +"', fromLeftBottom = ["+str(fromLeft)+", "+str(fromBottom)+"], fromEdge="+str(fromEdge)+\
    ",width="+str(thickness)+", thickness="+str(width)+", offset="+str(offsetFromWall)+", rotation="+str(angleRot)+", shiftEnds="+str(shiftEndVectors)+")\r\n"


#print shadingSystem
print "Done"