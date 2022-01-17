import hou
import time

roothierarchy = ('/')

def createDepsys(context):
    """
    This Fincton is Auto Setup DependencyROP

    Samples**
    createDepsys('obj'):
    -context-
    >>obj
    >>shop
    """

    global roothierarchy

    rootdephierarchy = roothierarchy + str(context)

    if context == 'out':
       depRop = hou.node(rootdephierarchy)


    if context =='obj':
       depRop = hou.node(rootdephierarchy)

       if depRop.recursiveGlob('Dep_ROP') == ():

          objRop = depRop.createNode('ropnet','Dep_ROP')
          objRop.setColor(hou.Color((0.8,0.4,0.3)))
          objRop.moveToGoodPosition()



    if context =='shop':
       depRop = hou.node(rootdephierarchy)

       if depRop.recursiveGlob('Dep_ROP') == ():

          ShopRop = depRop.createNode('ropnet','Dep_ROP')
          ShopRop.moveToGoodPosition()
          ShopRop.setColor(hou.Color((0.3,0.4,0.8)))



    #=== Send currentNode Dep_Rop
    currentDep =  hou.node(roothierarchy).recursiveGlob('Dep_ROP')[0].path()



    try: #version 15 is not hou.selectedItems
       getcurrentnode = hou.selectedItems()

    except TypeError:
       getcurrentnode = hou.selectedNodes()

    except AttributeError:
       getcurrentnode = hou.selectedNodes()

    ropDepNode = hou.node(currentDep)

    timevariables = dict(pstart = hou.getenv("PSTART"),pend = hou.getenv("PEND"))
    dependency_Name = "_Dependency_Cache"

    for current in getcurrentnode:

        current_dict =  dict(name = str(current.name()),path = (str(current.path())))



        if ropDepNode.recursiveGlob(current_dict["name"]+dependency_Name) == ():
           depJobNode = ropDepNode.createNode('geometry')
           depJobNode.moveToGoodPosition()
           depJobNode.setColor(hou.Color((0.3,0.7,0.2)))


           depJobNode.setName(current_dict["name"] + dependency_Name)
           #=== PPI Setting ===#

           try:
              submitNode = depJobNode.createOutputNode("submitDeadlineHoudini")
              submitNode.move([0,-0.8])

              submitNode.setParms({'framesPerTask':100000})
              ##submit for Auto
              submitNode.parm('submit').pressButton()

           except :
              pass


           #reratuvePath_for_nullSop
           rerativePath = hou.node(current_dict["path"])
           AnkerName = "_Cache_Dep_Marker"
           if rerativePath.recursiveGlob(current_dict["name"]) == ():
              rerativeNode = rerativePath.createOutputNode('null',current_dict["name"]+AnkerName)
              rerativeNode.setColor(hou.Color((0.3,0.1,0.2)))
              rerativeNode.move([0.5,-0.3])

              cacheNode = rerativeNode.createOutputNode('filecache',depJobNode.name())
              cacheNode.setParms({'loadfromdisk':1})
              cacheNode.move([0,-0.3])

              depEndNode = cacheNode.createOutputNode('null',"out_Dependenciy_tree")
              depEndNode.setColor(hou.Color((0.3,0.1,0.2)))
              depEndNode.move([0,-0.5])
              depEndNode.setDisplayFlag(1)
              depEndNode.setRenderFlag(1)

              ##Map for Dep reraative Node
              depJobNode.setParms({'soppath':rerativeNode.path()})
