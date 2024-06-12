#bind to parent node
 hou.parent()
#bind yo node name from pythonSOP
 hou.pwd()

#create parameters for python
node = hou.pwd()
g = node.parmTemplateGroup()
p = hou.FloatParmTemplate("name","label",3,[1,1,1])   #_init_("name",'label',.......)
g.append(p)
node.setParmTemplateGroup(g)


#create Flipbooks
cur_desktop = hou.ui.curDesktop()
scene_viewer = hou.paneTabType.SceneViewer
scene = cur_desktop.paneTabOfType(scene_viewer)
scene.flipbookSettings().stash()
flip_book_options = scene.flipbookSettings()

flip_book_options.output('A:\\flipbook.$F4.jpeg') # Provide flipbook full path with padding.
flip_book_options.frameRange((0, 5)) # Enter Frame Range Here in x & y
flip_book_options.useResolution(1)
flip_book_options.resolution((1080, 720)) # Based on your camera resolution
scene.flipbook(scene.curViewport(), flip_book_options)


#Interapet Progress 
hou.InterruptableOperation class
Use this class to turn any Python code block into an interruptable operation.

Note

hou.InterruptableOperation does not work in the Python Shell. For testing purposes, use a shelf tool instead.

METHODS
Filter

Original order
 Collapse AllExpand All
__init__(operation_name, long_operation_name=None, open_interrupt_dialog=False)

Construct a new InterruptableOperation.
updateLongProgress(percentage=-1.0, long_op_status=None)

Update the progress percentage and status of the long, or high-level, operation.
updateProgress(percentage=-1.0)

Update the progress percentage of the operation.



##Selection Nodes##
#Import Houdini's Command Module
import hou
#Store path to Subnet in variable "rig"
rig = hou.node("/obj/geo1")
#For Loop - iterate through network, in search of nodes that match pattern "*_anim"
for ctrl in rig.glob("*foo*"):
    #Select all nodes that match pattern "*_anim" | NOTE: ctrl.setSelected(1, 0) also works :)
    ctrl.setSelected(True, clear_all_selected=False)
