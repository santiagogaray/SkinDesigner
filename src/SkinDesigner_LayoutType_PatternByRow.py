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
# LayoutType_PatternByRow
"""
Use this component to apply a specific pattern layout algorithm to a Layout Controller. 
DattaPattern2 places each pattern on different rows: patternRow_1 will be used on the 1st row of the facade, patternRow_2 on the second, etc., repeating the sequence of patterns to complete all the rows if neccesary.

    Args:
        patternRow_1: (patternRow_2, etc.) A list of integers represetning the the sequence of panel bay IDs to be used in the pattern algorithm.
                    Addtitional patterns can be aded with the '+' sign to be used on the subsequent levels.
   Returns:
        layoutType: A layout algorithm that inputs into a Layout Controller component.

"""

ghenv.Component.Name = "SkinDesigner_LayoutType_PatternByRow"
ghenv.Component.NickName = 'LayoutType_PatternByRow'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Design Controllers"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

# automnatically set the right input names and types (when using + icon) 
import Grasshopper.Kernel as gh
import GhPython
import scriptcontext as sc

numInputs = ghenv.Component.Params.Input.Count
accessList = ghenv.Component.Params.Input[0].Access.list
typeInt = gh.Parameters.Hints.GH_IntegerHint_CS()


for input in range(numInputs):
    access = accessList
    inputName = 'patternRow_' + str(input+1)

    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = accessList
    ghenv.Component.Params.Input[input].TypeHint = typeInt
    
ghenv.Component.Attributes.Owner.OnPingDocument()

import Grasshopper.Kernel as gh
#import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
from types import *
import random
import copy
import math



class LayoutDataFunction:
    
    __m_patterns = []
    warningData = []
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    
    def __init__(self):
        

        for input in range(numInputs):
            list = eval('patternRow_'+str(input+1))
            if list and list <> []: self.__m_patterns.append(list)
        if self.__m_patterns == []:
            self.warningData.append("Provide at least one pattern") 

            
    def GetParameter(self, strParam):
        
        return None   
        
    #Selection of panel bay based on pattern/panel location
    def Run(self, PanelBay_List, bayList, level, inLevelIndex, defaultBayList, randomObj, bayIndex, panelPlane) :
        
        
        rowPatternIndex = level - (int(level/len(self.__m_patterns)) * len(self.__m_patterns)) # relationship between floor number and bay number
        rowPattern = self.__m_patterns[rowPatternIndex]
        entryIndex = inLevelIndex - (int(inLevelIndex/len(rowPattern))* len(rowPattern) ) # curent index in list based on bay location
        bayIndex  = rowPattern[entryIndex]
        return bayIndex-1
        
        

            
        



layoutType = LayoutDataFunction()
if layoutType.warningData <> []: 
    for warning in layoutType.warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str(warning))

print "Done"
