# MAYA mesh deformer

Python plugin to read a file of point data. The point data deforms a mesh in
the Maya scene.

## Usage

Install `dgMeshDeformPlugin.py` to the `MAYA_PLUGIN_PATH`. The file contains the
required MEL scripts as a string - no other installation is necessary.
Load the plugin in the Maya Plugin Manager.

To use in the scene, select a polygon mesh and issue the command: `dgdeform`.
Then select a "points" file in the attribute editor.

A points file is a simple text file with x, y, z, x, y, z... values for each
point in the mesh on each line for each deforming frame. No checks are made to
ensure the number of points match.

The files `cube.obj` and `testdata.pts` are provided, to demonstrate usage.
