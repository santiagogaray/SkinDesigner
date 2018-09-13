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
# System_Wall
"""
Use this component to generate a Wall system to be added to a Panel component.

    Args:
        windowFrameWidth: A floating point value that indicates in scene units the width of the window frame. Default value is 0.025m (1 inch)
        windowFrameThickness: A floating point value that indicates in scene units the thickness of the window frame. Panel property 'PanelThickness' is valid. Default value depends on the glass pane placement.
        windowFrameLoc: A floating point value that indicates in scene units the location of the window frame. Positive values shift the frame inbound to the panel while negative values shift the frame outboud. Note the shifting is constrained to keep attachment to both the wall and the glass pane. Panel property 'PanelThickness' is valid. Default value is 0.0.
        tileWidth: A floating point value that indicates in scene units the horizontal dimension of the tile. Panel properties 'PanelWidth' and 'PanelHeight' are also valid. Default value is 0.0.
        tileHeight: A floating point value that indicates in scene units the vertical dimension of the tile. Panel properties 'PanelWidth' and 'PanelHeight' are also valid. Default value is 0.0.
        tileThickness: A floating point value that indicates in scene units the thickness of the tile. Panel properties 'PanelWidth' and 'PanelHeight' are valid. Default value is 0.025m (1 inch) if tileWidth and tileThickness are specified, otherwise is 0.00.
        tileJoint: A floating point value that indicates in scene units the joint dimension between tiles.  Default value is 0.025m (1 inch) if tileWidth and tileThickness are specified, otherwise is 0.00.
        tileEdgeOffset: A floating point value that indicates in scene units the dimentsion of  the joint around the panel edges.  Default value is tileJoint/2 if tileJoint is greater than 0.0, otherwise is 0.0.
    Returns:
        panelSystem: A list with the wall system data packed to be connected to a Panel component panelSystem input


"""


ghenv.Component.Name = "SkinDesigner_System-Wall"
ghenv.Component.NickName = 'System-Wall'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass


import GhPython
# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item
typeFloat = GhPython.Component.NewFloatHint()

for input in range(numInputs):
    access = accessList
    typeHint = None
    if input == 0: inputName = 'windowFrameWidth' ; access = accessItem; typeHint = typeFloat
    elif input == 1: inputName = 'windowFrameThickness' ; access = accessItem; typeHint = typeFloat
    elif input == 2: inputName = 'windowFrameLoc' ; access = accessItem; typeHint = typeFloat
    elif input == 3: inputName = 'tileWidth' ; access = accessItem
    elif input == 4: inputName = 'tileHeight'; access = accessItem
    elif input == 5: inputName = 'tileThickness' ; access = accessItem; typeHint = typeFloat
    elif input == 6: inputName = 'tileJoint'; access = accessItem; typeHint = typeFloat
    elif input == 7: inputName = 'tileEdgeOffset'; access = accessItem; typeHint = typeFloat
    else: continue
    
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    if typeHint: ghenv.Component.Params.Input[input].TypeHint = typeHint
    
ghenv.Component.Attributes.Owner.OnPingDocument()

import scriptcontext as sc
import Rhino
from types import *

#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == Rhino.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
if unitSystem == Rhino.UnitSystem.Millimeters: _UNIT_COEF = 1000
sc.doc = ghdoc


# WindowData(wd) = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess
if  numInputs > 3:
    if tileWidth == None or tileHeight == None: tileWidth = tileHeight = 0
else: tileWidth = tileHeight = 0
    
if  numInputs > 4:
    if type(tileThickness) == StringType : tileThickness = eval(tileThickness)
    elif tileThickness == None: tileThickness = .025*_UNIT_COEF if tileWidth > 0 else  0
else: tileThickness = .025*_UNIT_COEF if tileWidth > 0 else  0

if  numInputs > 5:
    if type(tileJoint) == StringType : tileJoint = eval(tileJoint)
    elif tileJoint == None : tileJoint = .025*_UNIT_COEF if tileWidth > 0 else  0
else: tileJoint = .025*_UNIT_COEF if tileWidth > 0 else  0

if  numInputs > 6:
    if type(tileEdgeOffset) == StringType : tileEdgeOffset = eval(tileEdgeOffset)
    if tileEdgeOffset == None : tileEdgeOffset = tileJoint/2
else: tileEdgeOffset = tileJoint/2


panelSystem= [0,0,0,0]
paneName="_P_Clad"
paneThickness = .01*_UNIT_COEF #standard pane thickness (not relevant)
PanelActions = "AddPane('"+ paneName + "', thickness="+str(paneThickness)+", offset="+str(paneThickness)+", offsetEdge="+str(tileEdgeOffset)+\
    ", tileWidth="+str(tileWidth)+", tileHeight="+str(tileHeight)+", tileThickness="+str(tileThickness)+", tileGap="+str(tileJoint)+")\r\n"


if windowFrameThickness == None: windowFrameThickness = "max(PanelThickness+0.02*_UNIT_COEF+"+str(paneThickness+tileThickness)+", abs(eval(str(Window['recess']))) + 0.05*_UNIT_COEF + "+str(paneThickness+tileThickness)+")"
if windowFrameWidth == None: windowFrameWidth = .025*_UNIT_COEF
if windowFrameLoc == None: windowFrameLoc = "0"

MullionActions = ""
WindowMullionActions = ""

windowFrameInThickness = "min(max(0.02*_UNIT_COEF,"+"eval(str(Window['recess']))+PanelThickness-0.01*_UNIT_COEF)+"+str(windowFrameLoc)+","+str(windowFrameThickness)+"+0.02*_UNIT_COEF)"
windowFrameOutThickness = "min(max("+str(windowFrameThickness) + "-(" + windowFrameInThickness + "),.02*_UNIT_COEF),"+str(windowFrameThickness)+")"

for mullionType in ['WindowBottom','WindowTop','WindowLeft', 'WindowRight'] :
    WindowMullionActions += "AddMullionType('"+ mullionType+"', width="+ str(windowFrameWidth)+", thickness=[" + \
    str(windowFrameInThickness)+"], capThickness=[" + str(windowFrameOutThickness)+"])\r\n"


panelSystem = ["WallSystem" , PanelActions , MullionActions, WindowMullionActions]



