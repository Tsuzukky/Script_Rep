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
