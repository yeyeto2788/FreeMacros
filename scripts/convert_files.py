#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import shutil
import subprocess
from zipfile import ZipFile

REPO_DIR = os.path.dirname(os.path.dirname(__file__))
MACROS_DIR = os.path.join(REPO_DIR, "macros")
RELEASE_DIR = os.path.join(REPO_DIR, "release")


def main():

    if not os.path.exists(RELEASE_DIR):
        os.makedirs(RELEASE_DIR, exist_ok=True)

    macro_files = [
        file
        for file in filter(
            lambda filename: filename != "__init__.py", os.listdir(MACROS_DIR)
        )
    ]

    release_macros = list()

    for file in macro_files:
        macro_filename = f"{file.replace('.py', '.FCMacro')}"
        source_file = os.path.join(MACROS_DIR, file)
        destination_file = os.path.join(RELEASE_DIR, macro_filename)

        shutil.copy2(src=source_file, dst=destination_file)
        release_macros.append(destination_file)

    app_version = subprocess.run(
        ["poetry", "version", "-s"], capture_output=True, text=True
    ).stdout.rstrip()
    zip_filename = os.path.join(RELEASE_DIR, f"FreeCADMacros_v{app_version}.zip")

    if os.path.exists(zip_filename):
        raise ValueError(
            f"Zip file '{zip_filename}' already exists.\nDid you change version?"
        )
    else:
        with ZipFile(zip_filename, "w") as zip_obj:
            for file in release_macros:
                # Add file to archive folder.
                zip_obj.write(filename=file, arcname=os.path.basename(file))
                # Delete file created
                os.remove(file)
        print(f"Release zip file '{zip_filename}' created.")


if __name__ == "__main__":
    main()
