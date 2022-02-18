#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export objects into STL and STEP format."""

import os
from collections import namedtuple

import FreeCAD
import FreeCADGui
import ImportGui
import Mesh
from PySide import QtCore
from PySide import QtGui

DEBUG = False
_statuses = {"FAIL": "FAIL", "SUCCESS": "SUCESS"}
STATUS = namedtuple("status", _statuses.keys())(*_statuses)


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


def get_objects_to_export(document: FreeCAD.ActiveDocument):
    """Get all visible objects to be exported.

    Args:
        document (FreeCAD.ActiveDocument): [description]

    Returns:
        [type]: [description]
    """
    objects_to_export = list()

    for object in document.Objects:
        # Line added due to failing on export > hasattr(object.ViewObject, "Deviation")
        if object.ViewObject.isVisible() and hasattr(object.ViewObject, "Deviation"):
            object.ViewObject.Deviation = 0.01
            object.ViewObject.AngularDeflection = 5.0

            objects_to_export.append(object)

    return objects_to_export


def create_directories(directories: list):
    """Create needed output directories if do not exists.

    Args:
        directories (list): List of paths to be created.
    """
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)


def export_objects(objects: list, filename: str) -> bool:
    """Export objects to a given format based on the name.

    Basically done in order not to duplicate code.

    Args:
        objects (list): Objects to be exported.
        filename (str): Output filename.

    Returns:
        [bool]: Operation result
    """
    try:
        if filename.endswith("step"):
            ImportGui.export(objects, filename)
        else:
            Mesh.export(objects, filename)

        return True
    except TypeError as exec_error:
        print(exec_error)
        return False


def create_dialog(msg: str, dialog_type: str):
    """Create dialog window on the screen.

    Args:
        msg (str): Message to be displayed.
        dialog_type (str): Type of dialog window.
    """
    if dialog_type == "warning":
        box_type = QtGui.QMessageBox.Warning
    else:
        box_type = QtGui.QMessageBox.Information

    diag = QtGui.QMessageBox(box_type, "Error in macro MessageBox", msg)
    diag.setWindowModality(QtCore.Qt.ApplicationModal)
    diag.exec_()


def main():
    """Executes the main logic of the application."""  # noqa: D401
    if DEBUG:
        # Clear report view in debug mode
        FreeCADGui.getMainWindow().findChild(QtGui.QTextEdit, "Report view").clear()
    documents = FreeCAD.listDocuments()
    messages = list()
    overall_dialog_type = "info"

    for document_name in documents:

        FreeCAD.setActiveDocument(document_name)

        # Get active document
        doc = FreeCAD.ActiveDocument

        doc_directory = os.path.dirname(doc.FileName)
        step_folder = os.path.join(doc_directory, "STEP")
        stl_folder = os.path.join(doc_directory, "STL")

        # Create directories if do not exists
        create_directories(directories=[step_folder, stl_folder])
        objects = get_objects_to_export(document=doc)

        # Export to STEP
        filename = os.path.join(step_folder, f"{doc.Name}.step")
        step_export = export_objects(objects=objects, filename=filename)

        # Export to stl
        filename = os.path.join(stl_folder, f"{doc.Name}.stl")
        stl_export = export_objects(objects=objects, filename=filename)

        if step_export and stl_export:
            dialog_type = "info"
            message = f"Export successfull of:\n{os.path.join(step_folder, doc.Name)}\n"
            message += f"{os.path.join(stl_folder, doc.Name)}"

        else:
            dialog_type = "warning"
            message = f"STEP export status: {STATUS.SUCCESS if step_export else STATUS.FAIL}\n"
            message = (
                f"STL export status: {STATUS.SUCCESS if stl_export else STATUS.FAIL}"
            )

        # Close and open not saving changes
        document_filename = doc.FileName
        FreeCAD.closeDocument(doc.Name)
        FreeCAD.open(document_filename)

        if dialog_type != "info":
            overall_dialog_type = "Warning"

        messages.append(message)

    overall_message = "\n\n".join(messages)
    create_dialog(msg=overall_message, dialog_type=overall_dialog_type)


if __name__ == "__main__":
    main()
