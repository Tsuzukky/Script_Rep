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
