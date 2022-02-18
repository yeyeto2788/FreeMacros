#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create technical drawing pages based on the objects on the FreeCAD document."""
import os
import traceback

import FreeCAD
import FreeCADGui
from PySide import QtGui

DEBUG = True


ALLOWED_BODIES = [
    "PartDesign::AdditiveCone",
    "PartDesign::AdditiveCylinder",
    "PartDesign::Chamfer",
    "PartDesign::Fillet",
    "PartDesign::Pad",
    "PartDesign::Pocket",
    "PartDesign::PolarPattern",
    "PartDesign::AdditiveCylinder",
    "PartDesign::SubtractiveCylinder",
]
TEMPLATES = {
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


def console_message(msg: str):
    """Print message in console.

    Args:
        msg (str): Message to be printed
    """
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintMessage(msg)


def console_warning(msg: str):
    """Print warning in console.

    Args:
        msg (str): Message to be printed
    """
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintWarning(msg)


def console_error(msg):
    """Print error in console.

    Args:
        msg (str): Message to be printed
    """
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintError(msg)


def console_debug(msg):
    """Print message in console.

    Args:
        msg (str): Message to be printed
    """
    if DEBUG:
        FreeCAD.Console.PrintMessage("\n")
        FreeCAD.Console.PrintMessage("Debug : " + str(msg))


def get_visible_objects(document: FreeCAD.ActiveDocument):
    """Get all visible objects to be exported.

    Args:
        document (FreeCAD.ActiveDocument): [description]

    Returns:
        [type]: [description]
    """
    objects_to_export = list()

    for object in document.Objects:

        if (
            object.ViewObject.isVisible()
            and hasattr(object.ViewObject, "Deviation")
            and str(object.TypeId) in ALLOWED_BODIES
        ):  # should be a sketch
            objects_to_export.append(object)

    return objects_to_export


def create_technical_page(
    document: FreeCAD.ActiveDocument, object, page_name: str, template_dir: str
):
    """Create technical page using a template and assinging projection groups to it.

    Args:
        document (FreeCAD.ActiveDocument): Document on which to create the technical pages.
        object (_type_): _description_
        page_name (str): Name for the page.
        template_dir (str): Path to the template to use.
    """
    # Select visible object that would be use to generate the page of.
    FreeCAD.Gui.Selection.addSelection(document.Name, object.Name)
    # Add a technical page based on a template.
    page_obj = FreeCAD.activeDocument().addObject("TechDraw::DrawPage", page_name)
    template_obj = FreeCAD.activeDocument().addObject(
        "TechDraw::DrawSVGTemplate", f"Template_{object.Label}"
    )
    # Assign template of the template from directory.
    template_obj.Template = template_dir
    # Assign page template.
    page_obj.Template = template_obj
    # Add the Projection views
    project_group_object = FreeCAD.activeDocument().addObject(
        "TechDraw::DrawProjGroup", f"ProjGroup_{object.Label}"
    )
    page_obj.addView(project_group_object)
    # Set the source of the views to be the visible object.
    project_group_object.Source = FreeCAD.getDocument(document.Name).getObject(
        object.Name
    )

    try:
        project_group_object.addProjection("Front")
    except TypeError:
        FreeCAD.activeDocument().removeObject("TechDraw::DrawPage", page_name)
        FreeCAD.activeDocument().removeObject(
            "TechDraw::DrawSVGTemplate", f"Template_{object.Label}"
        )
        FreeCAD.activeDocument().removeObject(
            "TechDraw::DrawProjGroup", f"ProjGroup_{object.Label}"
        )
    else:
        project_group_object.ScaleType = "Automatic"
        project_group_object.Anchor.Direction = FreeCAD.Vector(0.000, -1.000, 0.000)
        project_group_object.Anchor.RotationVector = FreeCAD.Vector(1.000, 0.000, 0.000)
        project_group_object.Anchor.XDirection = FreeCAD.Vector(1.000, 0.000, 0.000)
        project_group_object.Anchor.recompute()
        FreeCAD.ActiveDocument.recompute()

        # Add views on the technical drawing
        project_group_object.addProjection("Right")
        project_group_object.addProjection("Top")
        project_group_object.addProjection("Left")
        project_group_object.addProjection("Bottom")
        project_group_object.addProjection("FrontBottomLeft")
        project_group_object.addProjection("FrontTopRight")
        project_group_object.addProjection("FrontTopLeft")
        project_group_object.addProjection("FrontBottomRight")
        FreeCAD.ActiveDocument.recompute()

    FreeCAD.Gui.ActiveDocument.resetEdit()
    # Clear selection
    FreeCAD.Gui.Selection.clearSelection()


def main():
    """Executes the main logic of the application."""  # noqa: D401
    if DEBUG:
        # Clear report view in debug mode
        FreeCADGui.getMainWindow().findChild(QtGui.QTextEdit, "Report view").clear()

    # Fit view to screen
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    # Set the view to be front view
    FreeCAD.Gui.activeDocument().activeView().viewFront()
    current_document = FreeCAD.ActiveDocument
    visible_objects = get_visible_objects(document=current_document)

    templates_dir = os.path.join(
        FreeCAD.ConfigGet("AppHomePath"), "share", "Mod", "TechDraw", "Templates"
    )
    template_filename = TEMPLATES[9]
    template_full_dir = os.path.join(templates_dir, template_filename)

    for _, object in enumerate(visible_objects):

        try:
            console_debug(f"Working on {object.Label}")
            page_name = f"Page_{object.Label}"
            create_technical_page(
                document=current_document,
                object=object,
                page_name=page_name,
                template_dir=template_full_dir,
            )
        except TypeError as exec_error:
            msg = f"Error with object {str(object.Label)}, error: {exec_error.__str__()}, "
            msg += f"traceback: {traceback.format_exc()}"
            console_error(msg)


if __name__ == "__main__":
    main()
