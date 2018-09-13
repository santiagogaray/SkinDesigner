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
Use this component to apply a post-processing function(representation properties of the skin) to a SkinGenerator component. This component optimizes the display of the panel geometry for better facade analysis with Ladybug Tools. 

    Args:
        ShadeWidthThreshold: A floating point value indicating the minimum shading and mullion caps projections to be included in the final geometry of the panels. Default value is 0.1m
    Returns:
        PostProcFunction:  A PPFunction object to be connected to the SkinGenerator postProcFunctions input.
"""

ghenv.Component.Name = "SkinDesigner_PP-LBHB_Output"
ghenv.Component.NickName = 'PP-LBHB_Output'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Design Controllers"
try: ghenv.Component.AdditionalHelpFromDocStrings = "3"
except: pass

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
#from types import *
#import random
#import copy
#import math

SGLibPanel = sc.sticky["SGLib_Panel"]

#GLOBAL PARAMETERS-------------------------------------------------------
#init set up global variables
_UNIT_COEF = 1
sc.doc = Rhino.RhinoDoc.ActiveDoc
unitSystem = sc.doc.ModelUnitSystem
if unitSystem == Rhino.UnitSystem.Feet: _UNIT_COEF = 3.28084
if unitSystem == Rhino.UnitSystem.Inches: _UNIT_COEF = 3.28084*12
if unitSystem == Rhino.UnitSystem.Millimeters: _UNIT_COEF = 1000

sc.doc = ghdoc


#paramters
#init 
sc.doc = Rhino.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

class PP_LadybugFunction:
    
    __m_functionCall = ''
    __m_PPDrawMode = None
    __m_ShadeWidthThresh = 0.1*_UNIT_COEF
    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        self.__m_functionCall = "LBHB_PanelsOutput(skinPanelData)"
        self.__m_PPDrawMode = "LADYBUG"
        
        if  ShadeWidthThreshold <> None : self.__m_ShadeWidthThresh = ShadeWidthThreshold
        
    def PP_SetPanelsProperties(self, PanelBay_List):
        
        for panelBay in PanelBay_List:
            for panel  in panelBay :
                panel.SetDrawMode(self.__m_PPDrawMode)
                if self.__m_ShadeWidthThresh <> None :
                    panel.SetPanelProperty("LB_ShadeThreshold", self.__m_ShadeWidthThresh)
    
    
    def RunString(self):
        return self.__m_functionCall
        
        
    #----------------------------------------------------------------------------------------
    # Prepares Ladybug data (extracts optimized glass and shading geoemetry for analysis)
    #-----------------------------------------------------------------------------------------
    
    def LBHB_PanelsOutput(self, skinPanelData):
        
   
        
        #--Prep work:Convert to Brep versions from GUI objects and pack in a 2D list and move to LB layers 
        return [self.RunString(), skinPanelData.values()]


PostProcFunction = PP_LadybugFunction()
print "Done"
