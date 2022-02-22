# FreeMacros

FreeCAD Macros in order to automate some manual processes.

- [FreeMacros](#freemacros)
  - [Available macros](#available-macros)
    - [Create technical drawing](#create-technical-drawing)
    - [Export files](#export-files)
    - [Take pictures](#take-pictures)
  - [Take pictures on `.jpg` and `.png` file format from different cameras perspectives. The images are saved on a `Images` folder within the same directory as the document the pictures are taken from.](#take-pictures-on-jpg-and-png-file-format-from-different-cameras-perspectives-the-images-are-saved-on-a-images-folder-within-the-same-directory-as-the-document-the-pictures-are-taken-from)
  - [Install dependencies for development](#install-dependencies-for-development)
  - [Generate Macros](#generate-macros)
  - [Automatic deployment](#automatic-deployment)
## Available macros

### Create technical drawing
Create basic technical design page per object on the document with all possible views (without measurements).

### Export files
Export all objects on documents into `.stl` and `.step` file format. Each file format will be saved into a folder named as the file formats (`STEP`, `STL`) with each object in each folder.

### Take pictures

Take pictures on `.jpg` and `.png` file format from different cameras perspectives. The images are saved on a `Images` folder within the same directory as the document the pictures are taken from.
---

## Install dependencies for development

This step is not mandatory as we'll be heavily using docker for development and for executing the code on this repository.

- Clone this repository
  - `git clone https://github.com/yeyeto2788/FreeMacros.git`
- Create the virtual environment and activate it
  - `poetry shell`
- Install dependencies
  - `poetry install`
- Instantiate the pre-commit plugin
  - `poetry run pre-commit install`

## Generate Macros

As I could see all macro files created on the FreeCAD application are actually renamed python files into `.FCMacro` files. In order to make the conversion is as simple as executing the `./scripts/convert_files.py` script.

For running the script you need at least to install `click` python library by executing `pip install click` on the terminal and a zip folder will be created on the `release` folder within the root directory of this repository.

```console
(.venv) yeyeto2788@juan-thinkbook:~/workspace/FreeCADMacros$ ./scripts/convert_files.py 
Release zip file './release/FreeCADMacros_v0.1.0.zip' created.
```

## Automatic deployment

Still WIP but I'm planning to get the zip release file and place it onto the FreeCAD macro folder.