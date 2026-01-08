# Description

This macro helps batch converting to mesh and exporting STL and OBJ files. It adds a GUI for speeding up the conversion and file saving of selected objects.

**This is a fork** of the original [Batch Export to Mesh](https://github.com/pgilfernandez/FreeCAD_Macro_Batch_Export_To_Mesh) by Pablo Gil Fernández.

## Fork Additions

* **Save as Assembly** - Combine multiple selected objects into a single mesh file instead of exporting them as separate files. Useful for exporting complete assemblies as one STL/OBJ for 3D printing or other applications.
  * **Part containers** (App::Part) are automatically expanded to include all child bodies
  * **OBJ files** export with separate named objects for each body (named as `PartName_BodyName`), making them easy to work with in Blender and other 3D software
  * **STL files** combine all geometry into a single mesh
* **3MF (Assembly)** - new: export assembly as a single .3mf package with one named object per Part→Body; no external dependencies required. The writer encodes a Part->Body hierarchy (parent Part objects referencing child body objects) so importers like OrcaSlicer can preserve the logical grouping.

![Batch export to mesh](/../media/img/screenshot1.png?raw=true "Batch export to mesh")


![Batch export to mesh](/../media/img/screenshot2.png?raw=true "Batch export to mesh")


# Features

* FreeCAD ''standard'' meshing option
* Custom names (object, project or custom)
* Converts/exports one or several objects at once
* **Save as Assembly** - combine multiple objects into one mesh file (NEW)
* Convert objects into the active FreeCAD project or
* Export objects to STL or OBJ files
* Absolute or relative paths are allowed
* Select local or global coordinates (useful for 3D print design)
* Creates folders if needed
* Opens folder in file explorer
* Preset loading/saving
* Remember last preset used


# Licence

Original work Copyright 2024 Pablo Gil Fernández.
Fork modifications Copyright 2026 WillJohns0n.

This work is licensed under GNU Lesser General Public License (LGPL). To view a copy of this license, visit:

https://www.gnu.org/licenses/lgpl-3.0.html
