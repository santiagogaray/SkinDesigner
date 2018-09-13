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
# Custom Geometry 
"""
Use this component to generate a custom geometry system to plug in Panel component.
-
    Args:
        _geometry: A list of Breps or a dynamicGeometry object output from a DynamicGeometry component used as the base geometry to be placed on the panel.
        upAxisVector: A unitized vector with a 1 value on the (X, Y or Z)component indicating the Z axis(up) for the geometry placement. Default is Z (0,0,1) 
        placementVector: A vector that specifies the placement (X, Y, Z) of the geometry in the panel. Origin is at lower left corner.
        scaleVector: A vector that specifies the scale factors (X, Y, Z) of the geomtry in the panel. Scale origin is at lower left corner of the panel.
        rotation: A floating point number that specifies the rotation of the geometry. Rotation origin is at lower left corner of the panel.
        tilable: A boolean turning on/off tiling of the geometry until it covers entire panel.
        trimToPanelSize: A boolean that turns on/off trimminig of the geomtry outsuide the panel extension.
        windowVoidDepth: A floating point number that reperesetns the depth of the subsdtracting volume in front of the window area.
        
    Returns:
        customSystem: A list with data custom geometry packed to be connected to a Panel component customSystem input

"""

ghenv.Component.Name = "SkinDesigner_CustomGeometry"
ghenv.Component.NickName = 'CustomGeometry'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "4"
except: pass

import Grasshopper.Kernel as gh
import GhPython

# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item
typeFloat = GhPython.Component.NewFloatHint()
typeVector3d = gh.Parameters.Hints.GH_Vector3dHint()
typeGHDoc = GhPython.Component.GhDocGuidHint()
typeBool = gh.Parameters.Hints.GH_BooleanHint_CS()
typeNull = gh.Parameters.Hints.GH_NullHint()

for input in range(numInputs):
    access = accessList
    typeHint = None
    if input == 0: inputName = '_geometry' ; access = accessList; typeHint = typeNull
    elif input == 1: inputName = 'upAxisVector' ; access = accessItem; typeHint = typeVector3d
    elif input == 2: inputName = 'placementVector' ; access = accessItem; typeHint = typeVector3d
    elif input == 3: inputName = 'scaleVector' ; access = accessItem; typeHint = typeVector3d
    elif input == 4: inputName = 'rotation' ; access = accessItem; typeHint = typeFloat
    elif input == 5: inputName = 'tilable'; access = accessItem; typeHint = typeBool 
    elif input == 6: inputName = 'trimToPanelSize'; access = accessItem; typeHint = typeBool 
    elif input == 7: inputName = 'windowVoidDepth'; access = accessItem; typeHint = typeFloat
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    if typeHint: ghenv.Component.Params.Input[input].TypeHint = typeHint
    
ghenv.Component.Attributes.Owner.OnPingDocument()

import scriptcontext as sc
import Rhino as rc
import rhinoscriptsyntax as rs
from types import *

#init set up global variables
_UNIT_COEF = 1
sc.doc = rc.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == rc.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == rc.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
if unitSystem == rc.UnitSystem.Millimeters: _UNIT_COEF = 1000
sc.doc = ghdoc

newCustomGeometry = None
vecUpAxis = rc.Geometry.Vector3d(0,0,1)
vecPlacement = rc.Geometry.Vector3d(0,0,0)
vecScaleFactor = rc.Geometry.Vector3d(1,1,1) #(non uniform scale can throw error someimtes(ex.cirles))
rotationZ = 0
isTilable = False
isTrimmed = False
dblWindowVoidDepth = 0
customSystem = None

#check for object type : Brep or dynamicGeometry instance
if _geometry and _geometry[0]:
    if type(_geometry[0]) == rc.Geometry.Brep :
        newCustomGeometry = _geometry
    elif str(type(_geometry[0])) == "<type 'instance'>" : 
        newCustomGeometry = _geometry[0]
    
    if numInputs > 1 and upAxisVector <> None: vecUpAxis = rs.coerce3dvector(upAxisVector)
    if numInputs > 2 and placementVector <> None: vecPlacement = rs.coerce3dvector(placementVector)
    if numInputs > 3 and scaleVector <> None: vecScaleFactor = rs.coerce3dvector(scaleVector)
    if numInputs > 4 and rotation <> None : rotationZ = eval(str(rotation))
    if numInputs > 5 and tilable <> None : isTilable = tilable
    if numInputs > 6 and trimToPanelSize <> None : isTrimmed = trimToPanelSize
    if numInputs > 7 and windowVoidDepth <> None: dblWindowVoidDepth = windowVoidDepth
        
    customSystem = [newCustomGeometry, vecPlacement, vecScaleFactor, vecUpAxis, isTilable, rotationZ, dblWindowVoidDepth, isTrimmed]
else:
    ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, "Missing '_geoemtry' input")
print "Done"
