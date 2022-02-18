#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Take pictures from views of an object."""
import os

import FreeCAD
import FreeCADGui
from PySide import QtGui

DEBUG = True
IMAGES_SIZES = [
    [640, 480],
    [1024, 720],
]


def console_message(msg):
    """Print message in console.

    Args:
        msg (str): Message to be printed
    """
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintMessage(msg)


def console_warning(msg):
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


def main():
    """Executes the main logic of the application."""  # noqa: D401
    if DEBUG:
        # Clear report view in debug mode
        FreeCADGui.getMainWindow().findChild(QtGui.QTextEdit, "Report view").clear()

    current_document = FreeCAD.ActiveDocument
    FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False)

    output_dir = os.path.join(os.path.dirname(current_document.FileName), "Images")

    console_debug(f"Images will be saved at {output_dir}")

    if not os.path.exists(output_dir):
        console_debug(f"Creating directory for images at '{output_dir}'")
        os.makedirs(output_dir, exist_ok=True)

    for camera_type in ["PerspectiveCamera", "OrthographicCamera"]:
        FreeCADGui.SendMsgToActiveView(camera_type)
        for view in ["ViewAxo", "ViewFront", "ViewTop"]:
            # Fit entire design on view
            FreeCADGui.SendMsgToActiveView("ViewFit")
            # Set view to take picture of
            FreeCADGui.SendMsgToActiveView(view)
            for width, height in IMAGES_SIZES:
                # Create filename based on parameters
                filename = f"{os.path.basename(FreeCAD.ActiveDocument.FileName)[:-6]}"
                filename += f"_{camera_type}_{view}_{str(width)}x{str(height)}"

                jpg_file = os.path.join(output_dir, f"{filename}.jpg")
                FreeCADGui.ActiveDocument.ActiveView.saveImage(
                    jpg_file, width, height, "White"
                )
                console_debug(f"Image '{jpg_file}' created.")

                png_file = os.path.join(output_dir, f"{filename}.png")
                FreeCADGui.ActiveDocument.ActiveView.saveImage(
                    png_file, width, height, "Transparent"
                )
                console_debug(f"Image '{png_file}' created.")

    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.ActiveDocument.ActiveView.viewIsometric()


if __name__ == "__main__":
    main()
