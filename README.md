# SkinDesigner
SkinDesigner is a facade panelization tool for Grasshopper

SkinDesigner enables the rapid generation of facade geometries from building massing surfaces and repeating, user-defined panels.

To install:

1-Make sure you have Rhino 5 and Grasshopper installed, or Rhino 6.
2-Install GHPython from www.food4Rhino.com website(Rhino 5 only).
3-Select and drag all the userObjects (downloaded here) onto your Grasshopper canvas.
4-Restart Rhino Grasshopper.

SkinDesigner has the geometric freedom to create virtually any facade geometry that is composed of similar repeating elements. However, unlike traditional Grasshopper workflows for generating such facades, SkinDesigner makes use of the following:

BLOCKS – Full façade systems are built with blocks for each repeating panel type. The use of blocks keeps the file size down and enables the “scaling up” of local façade concepts to large buildings.

DETAIL CONTROL – Flexibility to generate either fully-detailed facades (with solid geometric elements, mullions, etc.) or to generate simplified surface geometry (more appropriate for environmental studies, calculating metrics like glazing ratio, etc.)

CUSTOMIZATION CONTROL – The ability to specify the number of unique panel types that are generated from a continuous numerical data set. This enables the creation of data-driven facades that maintain control over their degree of customization.

PANEL INVENTORY VISUALS – Visualizations of the number of panels of each type in a given façade.

INFILLING – Automatic infilling “leftover” surface regions with custom panels when the dimensions of massing surfaces are not evenly divisible by the panel dimensions.

SUBDIVISION OF CURVED SURFACES – Automatically subdividing single-curvature surfaces into panels of a consistent dimension.

SURFACE-PANEL MODE - (New on Version 0.5) Automatically creates panels matching the shape of virtually any quadrangular or triangular surfaces provided, enabling the generation of free-form structures.

Check out the new SkinDesigner tutorials in this YouTube playlist as well as our example files to get yourself familiar with typical SkinDesigner workflows.

You should also feel free to post any questions, feature requests, or bug reports to the SkinDesigner Grasshopper Group  as discussions. Finally, SkinDesigner is an open source project and all of the project’s source code is visible on SkinDesigner's Github site as well as within the Grasshopper components (by double-clicking on them). 
