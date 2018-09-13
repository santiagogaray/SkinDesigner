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
# SkinDesigner_System-CurtainWall
"""
Use this component to generate a curtain-wall system to be added to a Panel component.
Note mullion thickness inputs accept floating point values or lists of three values to specify each mullion segment independently(left or below window, at window, above or right of window).

    Args:
        width: A floating point value that indicates in scene units the width of all panel and window mullions. Default value is 0.05m (2 inches)
        thickness: A floating point value that indicates in scene units the thickness of all panel and window mullions. Default value is 0.1m (4 inches)
        Alternatively a list of three floating point values can be indicated to specify mullion properties at each of the three mullion pieces(below/left of window, at window, above/right of window)
        capThickness: A floating point value that indicates in scene units the cap thickness of all panel and window mullions. Default value is 0.25m (1 inch).
        Alternatively a list of three floating point values can be indicated to specify mullion properties at each of the three mullion pieces(below/left of window, at window, above/right of window)
        windowThickness: A floating point value that indicates in scene units the thickness of window mullions. Overrides overal 'thickness' parameter Default value uses 'thickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        windowCapThickness: A floating point value that indicates in scene units the cap thickness of all window mullions. Overrides overal 'capThickness' parameter. Default value uses 'capThickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        panelThickness_H: A floating point value that indicates in scene units the thickness of horizontal panel mullions only. Overrides overal 'thickness' parameter. Default value uses 'thickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        panelCapThickness_H: A floating point value that indicates in scene units the cap thickness of horizontal panel mullion caps only. Overrides overal 'capThickness' parameter. Default value uses 'capThickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        panelThickness_V: A floating point value that indicates in scene units the thickness of vertical panel mullions only. Overrides overal 'thickness' parameter. Default value uses 'thickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        panelCapThickness_V: A floating point value that indicates in scene units the cap thickness of vertical panel mullion caps only. Overrides overal 'capThickness' parameter. Default value uses 'capThickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        windowThickness_H: A floating point value that indicates in scene units the thickness of horizontal window mullions only. Overrides overal 'thickness' and 'windowThickness' parameters. Default value uses 'thickness' or 'windowThickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        windowCapThickness_H: A floating point value that indicates in scene units the cap thickness of horizontal window mullion caps only. Overrides overal 'capThickness' and 'windowCapThickness' parameters. Default value uses 'capThickness' or 'windowCapThickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        windowThickness_V: A floating point value that indicates in scene units the thickness of vertical window mullions only. Overrides overal 'thickness' and 'windowThickness' parameters. Default value uses 'thickness' or 'windowThickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)
        windowCapThickness_V: A floating point value that indicates in scene units the cap thickness of vertical window mullion caps only. Overrides overal 'capThickness' and 'windowCapThickness' parameters. Default value uses 'capThickness' or 'windowCapThickness' value specified.
        Alternatively a list of three floating point values can be indicated to specify mullion propertys at each of the three mullion pieces(below/left of window, at window, above/right of window)


    Returns:
        panelSystem: A list with curtain-wall data packed to be connected to a Panel component panelSystem input

"""

ghenv.Component.Name = "SkinDesigner_System-CurtainWall"
ghenv.Component.NickName = 'System-CurtainWall'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

import Grasshopper.Kernel as gh
import GhPython
# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
accessItem = ghenv.Component.Params.Input[0].Access.item
typeFloat = GhPython.Component.NewFloatHint()

inputNames = ['-----global mullion data---','width','thickness','capThickness','windowThickness','windowCapThickness', '-----panel mllion data-----', 'panelThickness_H','panelCapThickness_H',\
    'panelThickness_V', 'panelCapThickness_V', '-----window mullion data---', 'windowThickness_H', 'windowCapThickness_H','windowThickness_V','windowCapThickness_V']
    
for input in range(numInputs):
    if input >= len(inputNames): continue
    ghenv.Component.Params.Input[input].NickName = inputNames[input]
    ghenv.Component.Params.Input[input].Name = inputNames[input]
    ghenv.Component.Params.Input[input].Access = accessList
    ghenv.Component.Params.Input[input].TypeHint = typeFloat

warningData=[]
#tranform inputs with one element lists to a single floating point value.
for num in range(numInputs) :
    inputData = ghenv.Component.Params.Input[num]
    if inputData.VolatileData.DataCount == 0: continue
    if inputData.VolatileData.DataCount == 1:
        value = inputData.VolatileData[0][0]
        inputString = inputData.Name + "=" + str(value)
        try:
            codeObj= compile(inputString,'<string>','single')
            eval(codeObj)
        except: warningData.append("Invalid input "+ inputString)

# reset deleted inputs. They keep last data otherwise.
for num in range(16-numInputs) :
    inputString = inputNames[15-num]
    if '-----' in inputString: continue
    inputString += '=[]'
    codeObj= compile(inputString,'<string>','single')
    eval(codeObj)
    
    
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


# WindowData(wd) = 0=width,1=height,2=fromLeft,3=fromBottom,4=recess

if width == [] : width = .05*_UNIT_COEF
if thickness == [] : thickness = 0.1* _UNIT_COEF
if windowThickness == [] : windowThickness = thickness
if capThickness == [] : capThickness = 0.025*_UNIT_COEF
if windowCapThickness == [] : windowCapThickness = capThickness

if panelThickness_H == [] : panelThickness_H = thickness
if panelThickness_V == [] : panelThickness_V = thickness
if panelCapThickness_H == [] : panelCapThickness_H = capThickness
if panelCapThickness_V == [] : panelCapThickness_V = capThickness
    

if windowThickness_H == [] : windowThickness_H = windowThickness
if windowThickness_V == [] : windowThickness_V = windowThickness
if windowCapThickness_H == [] : windowCapThickness_H = windowCapThickness
if windowCapThickness_V == [] : windowCapThickness_V = windowCapThickness

panelSystem = [0,0,0,0]

PanelActions = "AddPane('_P_Glass_SP',thickness="+str(0.02*_UNIT_COEF)+", offset="+str(0.02*_UNIT_COEF)+", offsetEdge="+str(0.02*_UNIT_COEF)+")\r\n"
MullionActions = ""
WindowMullionActions = "" #WindowMullionActions = "ShowWall()\r\n"

for mullionType in ['PanelLeft', 'PanelRight','PanelTop','PanelBottom','WindowBottom','WindowTop','WindowLeft', 'WindowRight'] :
    
    if mullionType in ['PanelBottom', 'PanelTop'] :
        if panelThickness_H: thickness  = panelThickness_H
        else :continue
        capThickness = panelCapThickness_H
    if mullionType in ['PanelLeft', 'PanelRight'] :
        if panelThickness_V: thickness = panelThickness_V
        else :continue
        capThickness = panelCapThickness_V
    if mullionType in ['PanelLeft', 'PanelRight','PanelTop','PanelBottom'] :
        MullionActions += "AddMullionType('"+ mullionType+"', width="+ str(width)+", thickness=" + str(thickness)+", capThickness=" + str(capThickness)+")\r\n"

    if mullionType in ['WindowBottom','WindowTop'] :
        if windowThickness_H : windowThickness = windowThickness_H
        else : continue
        windowCapThickness = windowCapThickness_H
    if mullionType in ['WindowLeft', 'WindowRight'] :
        if windowThickness_V : windowThickness = windowThickness_V
        else : continue
        windowCapThickness = windowCapThickness_V
        
    if mullionType in ['WindowLeft', 'WindowRight','WindowBottom','WindowTop'] :
        WindowMullionActions += "AddMullionType('"+ mullionType+"', width="+ str(width)+", thickness=" + str(windowThickness)+", capThickness=" + str(windowCapThickness)+")\r\n"




if warningData <> []: 
    for warning in warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str(warning))
else:
    panelSystem = ["CurtainWall" , PanelActions , MullionActions, WindowMullionActions]

#print panelSystem
 
#thickness= thicknessA = thicknessC="max(thickness, wd[4]*-1)" # use wall thickness or glass recess on punched window
#MullionData = "AddWindowMullions(width="+ str(width)+", thickness=[" + str(thicknessA)+","+ str(thickness)+","+ str(thicknessC)+\
#    "], capThickness=[0,0.05,0])\r\n"


print "Done"