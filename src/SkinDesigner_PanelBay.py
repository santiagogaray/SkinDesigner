# By Santiago Garay
# Panel Bay

"""
Use this component to create a panel bay (group of panels)

To add more panels in the construction, simply zoom into the component and hit the lowest "+" sign that shows up on the input side.  
To remove panels from the construction, zoom into the component and hit the lowest "-" sign that shows up on the input side.

    Args:
        pattern: A list of strings with panel names that indicate the order of the panels in the panel bay. 
        If no pattern is provided the list will follow the panel input order
        _panel_1: (panel_2, panel_3,...) Any Panel object generated by a Panel component to be included in the panel bay list.

    Returns:
        panel_Bay: A Panel list containing all the Panel objects in the order indicated  in the pattern. 
        Panel bays are used as inputs in SkinGenerator or PanelViewer components

"""

ghenv.Component.Name = "SkinDesigner_PanelBay"
ghenv.Component.NickName = 'PanelBay'
ghenv.Component.Message = 'VER 0.0.48\nJul_13_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "01 | Construction"

# automnatically set the right input names and types (when using + icon) 
numInputs = ghenv.Component.Params.Input.Count
 
for input in range(numInputs):
    
    if input == 0: 
        inputName = 'pattern'
        access = ghenv.Component.Params.Input[0].Access.list
    else: 
        inputName = '_panel_' + str(input)
        access = ghenv.Component.Params.Input[0].Access.item
    ghenv.Component.Params.Input[input].NickName = inputName
    ghenv.Component.Params.Input[input].Name = inputName
    ghenv.Component.Params.Input[input].Access = access
    
ghenv.Component.Attributes.Owner.OnPingDocument()


import Grasshopper.Kernel as gh
import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
SGLibPanel = sc.sticky["SGLib_Panel"]

panel_Bay = []
panel_List ={}
warningData = []

numInputs = ghenv.Component.Params.Input.Count
for input in range(numInputs):
    item = ghenv.Component.Params.Input[input]
    if "_panel" in item.Name and item.VolatileDataCount > 0:
        pList = []
        if item.VolatileData.get_DataItem(0):
            panel = item.VolatileData.get_DataItem(0).Value
            if isinstance(panel, SGLibPanel):panel_List[panel.GetName()] = panel
            else: warningData.append("Invalid data found at "+item.Name +" - data ignored"); continue

if panel_List:

    if pattern:
        Letters_List = pattern
        for i in range(len(Letters_List)):
            if Letters_List[i] in panel_List :
                panel_Bay.append(panel_List[Letters_List[i]])
    if pattern == None or pattern == [] :
        panel_Bay = panel_List.values()
        panel_Bay.reverse()

if warningData <> []: 
    for warning in warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str(warning))
print panel_List