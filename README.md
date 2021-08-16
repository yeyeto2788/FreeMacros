# FreeMacros

FreeCAD Macros in order to automate some manual processes

## Install dependencies for development

This step is not mandatory as we'll be heavily using docker for development and for executing the code on this repository.

- Clone this repository
  - `git clone https://github.com/yeyeto2788/FreeMacros.git`
- Create the virtual environment and activate it
  - `poetry shell`
- Install dependencies
  - `poetry install`
- Instanciate the pre-commit pluging
  - `poetry run pre-commit install`

## Generate Macros

As I could see all macro files created on the FreeCAD application are actually renamed python files into `.FCMacro` files. In order to make the convertion is as simple as executing the `./scripts/convert_files.sh` script.

## Automatic deployment
