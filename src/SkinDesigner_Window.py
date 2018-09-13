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
# Window
"""
Use this component to generate a window to be input to a Panel component.
-
Refer to PanelLib API for Definition input functions
    Args:
        width: A floating point number representing the window opening width in scene units. Panel properties 'PanelWidth' and 'PanelHeights' are valid. Default value is 'PanelWidth/2'.
        height: A floating point number representing the window opening height in scene units. Panel properties 'PanelWidth' and 'PanelThickness' are valid. Default value is 'PanelHeight/2'.
        fromLeft: A floating point value indicating in scene units the horizontal placement of the window from the left edge of the panel. Panel properties 'PanelWidth',  'PanelHeight' and 'C'(centered on panel) are valid. Default value is 'C'.
        fromBottom: A floating point value indicating in scene units the vertical placement of the window from the bottom edge of the panel. Panel properties 'PanelWidth', 'PanelHeight' and 'C'(centered on panel) are valid. Default value is 'C'.
        recess : A floating point value indicating in scene units the location of the glass pane relative to the front face of the wall element. Positive values place the glass pane inbound from the wall surface, negative values project the glass pane outbound. Default value is 0.0.
        conformSurfPanel : A boolean indicating if window conforms to the shape of a surface (for Surface Panel Mode' only). default is False.
    Returns:
        windowSystem: A list with window data formatted to be connected to a Panel component windowSystem input

"""


ghenv.Component.Name = "SkinDesigner_Window"
ghenv.Component.NickName = 'Window'
ghenv.Component.Message = 'VER 0.5.00\nJul_18_2018'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "02 | Parameters"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass



#import rhinoscriptsyntax as rs
#import Rhino
#import Panel14 as PanelLib
#import scriptcontext as sc

wWidth = "PanelWidth/2"
wHeight = "PanelHeight/2"
wFromLeft = "C"
wFromBottom = "C"
wRecess = 0.0
wConformSurface = False

if width<>None : wWidth = width
if height <> None : wHeight = height
if fromLeft <> None : wFromLeft = fromLeft
if fromBottom <> None : wFromBottom = fromBottom
if recess <> None : wRecess = -recess
if conformSurfPanel <> None : wConformSurface = conformSurfPanel

windowSystem = [wWidth,wHeight, wFromLeft, wFromBottom, wRecess, wConformSurface]
