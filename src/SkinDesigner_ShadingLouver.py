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
# Louver Shading
"""
Use this component to generate a shade louver to be added to a panel

    Args:
        layerName: A string indicating the layer the louver shade geometry will use when drawn in the scene. Default is _P_Shading
        width: A floating point value that represents the louvers' horizontal dimension in scene units. Default is 0.25m (10 inches aprox.)
        thickness: A floating point value that represents the louvers'  vertical dimension in scene units. Default value is 0.025m (1 inch)
        spacing: A floating point value that represents the spacing between louvers in scene units. Default value is 0.15m (6 inches aprox.)
        rotation: A floating point value indicating the rotation applied to the louvers length axis, with origon at the mid point of the louvers width. Default is 0.0
        offsetFromWallFromWall: A floating point value that represenets a separation distance from panel wall's exterior surface  (not including panel systems applied).Default value is 0.025 m (1 inch)
        verticalOrientation: A boolean to turn on/off vertical orientation of the shade. Default is False (horizontal).
        windowLouvers: A boolean to turn on off considering fromLeftEdge, fromBottomEdge and fromEdgeEnd values relative to the window instead of realtive to the panel. Deafult is False (dimensions are considered relative to the panel)
        fromLeftEdge: A floating point value indicating the separation of the louvers from the left edge of the panel or the window if it is a window louver. Default value is 0.0.
        fromRightEdge: A floating point value indicating the separation of the louvers from the right edge of the panel or the window if it is a window louver. Default value is 0.0.
        fromBottomEdge:  A floating point value indicating the separation of the louvers from the bottom edge of the panel or the window if it is a window louver. Default value is 0.0.
        fromTopEdge:  A floating point value indicating the separation of the louvers from the top edge of the panel or the window if it is a window louver. Default value is 0.0.
    Returns:
        shadingSystem: A list with shading data packed to be connected to a Panel component shadingSystem input


    Returns:


"""
# WindowData(wd) = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess 

ghenv.Component.Name = "SkinDesigner_ShadingLouver"
ghenv.Component.NickName = 'ShadingLouver'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "3"
except: pass

import Grasshopper.Kernel as gh
import GhPython
# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item
typeFloat = GhPython.Component.NewFloatHint()
typeString = GhPython.Component.NewStrHint()
typeBool = gh.Parameters.Hints.GH_BooleanHint_CS()
typeVector = gh.Parameters.Hints.GH_Vector3dHint()

for input in range(numInputs):
    access = accessList
    typeHint = typeString   
    if input == 0: inputName = 'width'; access = accessItem; typeHint = typeFloat
    elif input == 1: inputName = 'thickness'; access = accessItem; typeHint = typeFloat
    elif input == 2: inputName = 'spacing'; access = accessItem; typeHint = typeFloat
    elif input == 3: inputName = 'rotation'; access = accessItem; typeHint = typeFloat
    elif input == 4: inputName = 'offsetFromWall'; access = accessItem; typeHint = typeFloat
    elif input == 5: inputName = 'verticalOrientation' ; access = accessItem; typeHint = typeBool   
    elif input == 6: inputName = 'windowLouver'; access = accessItem; typeHint = typeBool   
    elif input == 7: inputName = 'layerName'; access = accessItem
    elif input == 8: inputName = '------------------------'
    elif input == 9: inputName = 'fromLeftEdge' ; access = accessItem
    elif input == 10: inputName = 'fromRightEdge'; access = accessItem
    elif input == 11: inputName = 'fromBottomEdge' ; access = accessItem
    elif input == 12: inputName = 'fromTopEdge'; access = accessItem
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    ghenv.Component.Params.Input[input].TypeHint = typeHint
ghenv.Component.Attributes.Owner.OnPingDocument()



import scriptcontext as sc
import Rhino


#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == Rhino.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
if unitSystem == Rhino.UnitSystem.Millimeters: _UNIT_COEF = 1000
sc.doc = ghdoc



if numInputs == 0 or width == None : width = .1*_UNIT_COEF
if numInputs < 2 or thickness== None : thickness = .01*_UNIT_COEF
if numInputs < 3 or spacing == None : spacing = .15*_UNIT_COEF
if numInputs < 4 or rotation == None : rotation = 0.0
if numInputs < 5 or offsetFromWall == None : offsetFromWall = .02*_UNIT_COEF
if numInputs < 8 or layerName == None : layerName = "_P_Shading"

if numInputs < 10 or fromLeftEdge == None : fromLeftEdge = 0.0
if numInputs < 11 or fromRightEdge == None : fromRightEdge = 0.0
if numInputs < 12 or fromBottomEdge == None : fromBottomEdge = 0.0
if numInputs < 13 or fromTopEdge == None : fromTopEdge = 0.0


if numInputs >= 5 and verticalOrientation == True : shadingType = 'VerticalLouver'; hOffset = str(spacing)+"/2"; vOffset="0"
else: shadingType = 'HorizontalLouver'; hOffset = "0"; vOffset=str(spacing)+"/2"

if numInputs >= 6 and windowLouver == True:
    if shadingType == 'HorizontalLouver': shadingType = 'HorizontalWindowLouver'
    else: shadingType = 'VerticalWindowLouver'


shiftEndVectors = [None, None]
if numInputs > 14 and shiftEnd1 : shiftEndVectors[0] = [shiftEnd1.X, shiftEnd1.Y, shiftEnd1.Z]
if numInputs > 15 and shiftEnd2 : shiftEndVectors[1] = [shiftEnd2.X, shiftEnd2.Y, shiftEnd2.Z]


shadingSystem = "AddShadingType('" + shadingType +"', layerName='"+ layerName +"', fromLeftBottom = ["+str(fromLeftEdge)+", "+str(fromBottomEdge)+\
    "], fromRightTop=["+str(fromRightEdge)+", "+str(fromTopEdge)+"],width="+str(thickness)+", thickness="+str(width)+\
    ", spacing="+str(spacing)+", offset="+str(offsetFromWall)+", rotation="+str(rotation)+", shiftEnds="+str(shiftEndVectors)+")\r\n"

#print shadingSystem
print "Done"