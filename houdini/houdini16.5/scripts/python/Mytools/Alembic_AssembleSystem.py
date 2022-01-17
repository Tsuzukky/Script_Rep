import hou

def Assenble_bgeo():
    """
    This fuc is
    Selected Alembic objects Convert_HoudiniGeometry& write_bgeoFile

    Samples***
    selcted obj alembicNode...
    Assenble_bgeo()
    """

    import hou
    import dep_system

    select = hou.selectedItems()
    root = hou.node("/obj")


    for shapenode in select:

        Nodepath = str(shapenode.path())

        alembicNode = hou.node(Nodepath)

        Child = alembicNode.children()
        Child_Path = str(Child[0].path())

        #====== Create CahceAssembles======#
        Cache_AssembleNode = root.createNode("geo",None,0)
        Cache_AssembleNode.setName(str(Child[0]) + '_bgeo')
        Cache_AssembleNode.setColor(hou.Color((0.3,0.4,0.3)))
        Cache_AssembleNode.moveToGoodPosition()

        Assemble_root = hou.node(Cache_AssembleNode.path())

        #objectMergeSop
        objmergeSop = Assemble_root.createNode('object_merge')
        objmergeSop.setName('Import_' + str(Child[0]) + '_ABC')
        objmergeSop.setParms({'objpath1':Child_Path,'xformtype':1})
        objmergeSop.setColor(hou.Color((0.7,0,0.4)))

        #PythonSOP
        PythonSop = objmergeSop.createOutputNode('python','Unpacking_process')
        PythonSop.move([0.3,-0.3])
        PythonSop.parm('python').set("node = hou.pwd()\ngeo = node.geometry()\nresultgeo = hou.Geometry()\
                                      \n\nsops = hou.sopNodeTypeCategory()\n#unpack\n\nunpack_py = sops.nodeVerb('unpack')\
                                      \nunpack_py.setParms({'transfer_attributes': 'path'})\nunpack_py.execute(geo,[geo])\
                                      \n\n#reconvert_ShapeName\nfor prim in geo.iterPrims():\n    path = prim.attribValue('path')\
                                      \n    shape = path.split('/')[-1]\n\n    prim.setAttribValue('path',shape)\n\n#normal\
                                      \nnormal_py = sops.nodeVerb('normal')\nnormal_py.execute(resultgeo,[geo])\n\n\
                                      \nnode.geometry().clear()\nnode.geometry().merge(resultgeo)")
        #nullSop
        EndnullSop = PythonSop.createOutputNode('null')
        EndnullSop.setName("unpacking_" + str(Child[0]) + "_OUT")
        EndnullSop.move([0,-0.3])
        EndnullSop.setColor(hou.Color((0.5,0.4,0.0)))
        EndnullSop.setCurrent(1,1)
        EndnullSop.setDisplayFlag(1)
        EndnullSop.setRenderFlag(1)

        dep_system.createDepsys("obj")



        #FileCache
        #FilecacheSop = EndnullSop.createOutputNode('filecache')
        #FilecacheSop.setName('bgeo_' + str(Child[0]))
        #FilecacheSop.move([0,-0.3])
        #FilecacheSop.setParms({'loadfromdisk' : '1','missingframe':1})

        #FilecacheSop.setParmExpressions({'f1': '$PSTART-30','f2':'$PEND+2'})

        #OutnullSop
        #OUTnullSop = FilecacheSop.createOutputNode('null')
        #OUTnullSop.setName( str(Child[0])+'_OUT')
        #OUTnullSop.move([0,-0.5])
        #OUTnullSop.setColor(hou.Color((0.5,0.4,0.0)))
        #SelectionFlag
        #FilecacheSop.setCurrent(1,1)
        #OUTnullSop.setDisplayFlag(1)
        #OUTnullSop.setRenderFlag(1)

        #===event===#
        #Post_Select = hou.selectedItems()
        #Post_Path  = str(Post_Select[0].path())

        #EventNode = hou.node(Post_Path)
        #EventNode.parm("execute").pressButton()
