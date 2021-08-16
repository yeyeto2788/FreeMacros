#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import FreeCAD


available_templates = {
    0: "A0_Landscape_blank.svg",
    1: "A0_Landscape_ISO7200_Pep.svg",
    2: "A0_Landscape_ISO7200TD.svg",
    3: "A1_Landscape_blank.svg",
    4: "A1_Landscape_ISO7200_Pep.svg",
    5: "A1_Landscape_ISO7200TD.svg",
    6: "A2_Landscape_blank.svg",
    7: "A2_Landscape_ISO7200_Pep.svg",
    8: "A2_Landscape_ISO7200TD.svg",
    9: "A3_Landscape_blank.svg",
    10: "A3_Landscape_EN_m52.svg",
    11: "A3_Landscape_FR_m52.svg",
    12: "A3_Landscape_ISO7200_Pep.svg",
    13: "A3_Landscape_ISO7200TD.svg",
    14: "A3_Landscape_IT_m52.svg",
    15: "A3_LandscapeTD.svg",
    16: "A4_Landscape_blank.svg",
    17: "A4_Landscape_ISO7200_Pep.svg",
    18: "A4_Landscape_ISO7200TD.svg",
    19: "A4_LandscapeTD.svg",
    20: "A4_Portrait_blank.svg",
    21: "A4_Portrait_ISO7200Pep.svg",
    22: "A4_Portrait_ISO7200TD.svg",
    23: "ANSIB_Portrait.svg",
    24: "ANSIB.svg",
    25: "Arch_A_Landscape.svg",
    26: "Arch_A_Portrait.svg",
    27: "Arch_B_Landscape.svg",
    28: "Arch_B_Portrait.svg",
    29: "Arch_C_Landscape.svg",
    30: "Arch_C_Portrait.svg",
    31: "Arch_D_Landscape.svg",
    32: "Arch_D_Portrait.svg",
    33: "Arch_E1_Landscape.svg",
    34: "Arch_E1_Portrait.svg",
    35: "Arch_E2_Landscape.svg",
    36: "Arch_E2_Portrait.svg",
    37: "Arch_E3_Landscape.svg",
    38: "Arch_E3_Portrait.svg",
    39: "Arch_E_Landscape.svg",
    40: "Arch_E_Portrait.svg",
    41: "HowToExample.svg",
    42: "USLetter_Landscape_blank.svg",
    43: "USLetter_Landscape.svg",
}


def get_visible_objects(document: FreeCAD.ActiveDocument):
    """Get all visible objects to be exported.

    Args:
        document (FreeCAD.ActiveDocument): [description]

    Returns:
        [type]: [description]
    """
    objects_to_export = list()

    for object in document.Objects:

        if object.ViewObject.isVisible() and hasattr(
            object.ViewObject, "Deviation"
        ):  # should be a sketch
            objects_to_export.append(object)

    return objects_to_export


# Fit view to screen
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
# Set the view to be front view
FreeCAD.Gui.activeDocument().activeView().viewFront()
current_document = FreeCAD.ActiveDocument
visible_objects = get_visible_objects(document=current_document)

templates_dir = os.path.join(
    FreeCAD.ConfigGet("AppHomePath"), "share", "Mod", "TechDraw", "Templates"
)
template_filename = available_templates[16]
template_full_dir = os.path.join(templates_dir, template_filename)

for index, object in enumerate(visible_objects):
    page_name = f"Page{index}"
    # Select visible object that would be use to generate the page of.
    FreeCAD.Gui.Selection.addSelection(current_document.Name, object.Name)
    # Add a page based on a template.
    FreeCAD.activeDocument().addObject("TechDraw::DrawPage", page_name)
    FreeCAD.activeDocument().addObject("TechDraw::DrawSVGTemplate", "Template")
    FreeCAD.activeDocument().Template.Template = template_full_dir
    # `__getattribute__` dunder method used in order to retrieve the page created.
    FreeCAD.activeDocument().__getattribute__(
        page_name
    ).Template = FreeCAD.activeDocument().Template
    # Add the Projection views
    FreeCAD.activeDocument().addObject("TechDraw::DrawProjGroup", "ProjGroup")
    FreeCAD.activeDocument().__getattribute__(page_name).addView(
        FreeCAD.activeDocument().ProjGroup
    )
    # Set the source of the views to be the visible object.
    FreeCAD.activeDocument().ProjGroup.Source = FreeCAD.getDocument(
        current_document.Name
    ).getObject(object.Name)
    FreeCAD.activeDocument().ProjGroup.addProjection("Front")
    FreeCAD.activeDocument().ProjGroup.ScaleType = "Page"
    FreeCAD.activeDocument().ProjGroup.Anchor.Direction = FreeCAD.Vector(
        0.000, -1.000, 0.000
    )
    FreeCAD.activeDocument().ProjGroup.Anchor.RotationVector = FreeCAD.Vector(
        1.000, 0.000, 0.000
    )
    FreeCAD.activeDocument().ProjGroup.Anchor.XDirection = FreeCAD.Vector(
        1.000, 0.000, 0.000
    )
    FreeCAD.activeDocument().ProjGroup.Anchor.recompute()
    FreeCAD.ActiveDocument.recompute()

    # Add views on the technical drawing
    FreeCAD.activeDocument().ProjGroup.addProjection("Right")
    FreeCAD.activeDocument().ProjGroup.addProjection("Top")
    FreeCAD.activeDocument().ProjGroup.addProjection("Left")
    FreeCAD.activeDocument().ProjGroup.addProjection("Bottom")
    FreeCAD.activeDocument().ProjGroup.addProjection("FrontBottomLeft")
    FreeCAD.activeDocument().ProjGroup.addProjection("FrontTopRight")
    FreeCAD.activeDocument().ProjGroup.addProjection("FrontTopLeft")
    FreeCAD.activeDocument().ProjGroup.addProjection("FrontBottomRight")
    FreeCAD.Gui.ActiveDocument.resetEdit()
