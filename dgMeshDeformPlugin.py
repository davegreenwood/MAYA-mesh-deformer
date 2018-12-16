import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.mel as mel
import sys
import linecache

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------


# plug-in global variables
kAuthor = 'David Greenwood'
kVersion = '0.1'
kArch = 'Any'
kPluginId = OpenMaya.MTypeId(0xAEEF8)
kNodeName = 'dgDeformNode'

# OpenMaya global values
kOutputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom
kInputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_inputGeom


# -----------------------------------------------------------------------------
# Plug-in Class
# -----------------------------------------------------------------------------


class Node(OpenMayaMPx.MPxDeformerNode):

    ptsfile = OpenMaya.MObject()
    time = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)

    def readline(self, fname, time):
        line = linecache.getline(fname, time)
        try:
            data = [float(i) for i in line.split()]
        except:
            return None
        return data

    @classmethod
    def creator(cls):
        '''Maya API node creator
        '''
        return OpenMayaMPx.asMPxPtr(cls())

    @classmethod
    def initializer(cls):
        '''
        Maya API node initialize, establish all the attributes
        '''
        tAttr = OpenMaya.MFnTypedAttribute()
        cls.ptsfile = tAttr.create("ptsFile", "pf", OpenMaya.MFnData.kString)
        tAttr.setStorable(True)
        tAttr.setKeyable(False)

        nAttr = OpenMaya.MFnNumericAttribute()
        cls.time = nAttr.create("time", "t", OpenMaya.MFnNumericData.kInt, 1)
        nAttr.setKeyable(True)

        # add attributes
        try:
            cls.addAttribute(cls.ptsfile)
            cls.addAttribute(cls.time)
            cls.attributeAffects(cls.ptsfile, kOutputGeom)
            cls.attributeAffects(cls.time, kOutputGeom)
        except:
            msg = 'Failed to create attributes of {} node\n'.format(kNodeName)
            sys.stderr.write(msg)
        pass

    def deform(self, pDataBlock, pGeometryIterator,
               pLocalToWorldMatrix, pGeometryIndex):
        ''' Deform each vertex using the geometry iterator.
        No checks are made to ensure the number of points read from the file
        matches the number of points in the output geometry.
        '''
        fname = pDataBlock.inputValue(self.ptsfile).asString()
        time = pDataBlock.inputValue(self.time).asInt()

        data = self.readline(fname, time)
        if not data:
            return

        while not pGeometryIterator.isDone():
            i = pGeometryIterator.index()
            x, y, z = data[3 * i], data[3 * i + 1], data[3 * i + 2]
            point = OpenMaya.MPoint(x, y, z)
            pGeometryIterator.setPosition(point)
            pGeometryIterator.next()
        # sys.stderr.write('{}, {}'.format(time, data))


# -----------------------------------------------------------------------------
# initialize the script plug-in
# -----------------------------------------------------------------------------

def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(kNodeName, kPluginId,
                             Node.creator,
                             Node.initializer,
                             OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise "Failed to register node: %s" % kNodeName


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginId)
    except:
        raise "Failed to deregister node: %s" % kNodeName


# -----------------------------------------------------------------------------
# AE template mel NB. Maya needs to reboot to reflect changes in the mel_cmd
# -----------------------------------------------------------------------------

mel_cmd = '''
global proc AEdgDeformNodeTemplate(string $nodeName) {{
    editorTemplate -beginScrollLayout;
    editorTemplate -beginLayout "PTS File" -collapse 0;
    editorTemplate -callCustom "dgDeformNodeFileLoad"
                                    "dgDeformNodeFileRefresh" "ptsFile";
    editorTemplate -endLayout;
    AEdependNodeTemplate $nodeName;
    editorTemplate -addExtraControls;
    editorTemplate -endScrollLayout;
}}

global proc dgDeformNodeFileLoad(string $attribute) {{
    setUITemplate -pst attributeEditorTemplate;
    columnLayout -rowSpacing 4;
    rowLayout -nc 3 -cw 2 210;

    text -label "Points File:";
    textField -editable 1 -text "" dgDeformNodeTxt0;
    iconTextButton -i1 "navButtonBrowse.xpm"
    -w 60 -h 20
    -c ("dgDeformNodeFileBrowse(\\"" + $attribute + "\\");")
    dgDeformNodeBtn0;

    setParent ..;
}}

global proc dgDeformNodeFileBrowse(string $attribute) {{
    string $result[] = `fileDialog2 -fm 1 -dialogStyle 2`;
    if (size($result) > 0) {{
        setAttr $attribute -type "string" $result[0];
    }} else {{
        setAttr $attribute -type "string"
            `textField -q -text dgDeformNodeTxt0`;
    }}
    connectControl -fileName dgDeformNodeTxt0 $attribute;
}}

global proc dgDeformNodeFileRefresh(string $attribute) {{
    string $fname = `getAttr $attribute`;
    setAttr $attribute -type "string" $fname;
}}

global proc dgdeform(){{
    string $sel[] = `ls -sl`;
    if (size($sel) > 0) {{
        string $a[] = `deformer -typ dgDeformNode`;
        connectAttr -f time1.outTime ($a[0] + ".time");
    }} else {{
    print "nothing selected";
    }}
}}
'''

mel.eval(mel_cmd)

# -----------------------------------------------------------------------------
# End
# -----------------------------------------------------------------------------
