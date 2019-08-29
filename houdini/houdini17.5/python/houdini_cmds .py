import hou
import dep_system

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




def palette():
    """
    This func is Return Current Empty Geometry

    Samples***
    palette()
    """
    import hou

    root = hou.node("/obj")
    Pl_Node = root.createNode("geo","Palette",0)

    Pl_Node.moveToGoodPosition()

    NodeColor = hou.Color((0.5,0.7,0.0))
    Pl_Node.setColor(NodeColor)

    del hou



def render_palette():
    """
    This func is return Preset Empty Rendergeometry

    Samples***
    render_palette()
    """

    import hou

    root = hou.node("/obj")
    Pl_Node = root.createNode("geo","Render_Palette",1)

    NodeColor = hou.Color((0.2,0.5,0.5))
    Pl_Node.setColor(NodeColor)

    Pl_Node.moveToGoodPosition()

    Soppath = Pl_Node.path()


    Innet = hou.node(Soppath)
    importNode = Innet.createNode("object_merge","IMPORT")

    null = importNode.createOutputNode("null","RenderOut")
    null.setDisplayFlag(1)


    del hou

def BaseRenderSet():
    """
    This func is return Preset RenderROP&MatPath

    Samples***
    BaseRenderSet()
    """
    import hou
    root = hou.node("/obj")
    ROP_Node = root.createNode("ropnet","ROP")
    MAT_Node = root.createNode("matnet","MAT")

    #ROP sectiion
    RopPath = ROP_Node.path()
    MantraNode = hou.node(RopPath)
    MantraNode.createNode("ifd","PaletteRender")

    #MAT sectiion
    MatPath = MAT_Node.path()
    BuilderNode = hou.node(MatPath)
    BuilderNode.createNode("materialbuilder","Mat_Container")


    GetPos = hou.Vector2([0,0])


    ROP_Node.setPosition([GetPos[0],GetPos[1]])
    MAT_Node.setPosition([GetPos[0],GetPos[1]-1])

    netBox = root.createNetworkBox()
    netBox.addItem(ROP_Node)
    netBox.addItem(MAT_Node)
    netBox.setComment("RenderWorkSet")
    netBox.fitAroundContents()

    del hou





def CvtFillVolume():
    """
    This func is SOPLevel Script
    Create Convert Line VolumeTool

    Samples***
    selcted Current Nodetree
    CvtFillVolume()
    """
    import hou

    #Create Path
    select = hou.selectedItems()
    node_Path  = str(select[0].path())

    root = hou.node(node_Path)

    #============ Motion Trail Bigin ==============#
    #Bigin_Sop Tree
    bigin_null = root.createOutputNode("null","ConvertFillCurve")

    bigin_null.move([0,-1])
    bigin_null.setColor(hou.Color((0.5,0.4,0.0)))

    #=== for loop Start ===#

    #forLoop_Sop_bigin Tree
    loop_beginSop = bigin_null.createOutputNode("block_begin","foreach_bigin")
    loop_beginSop.move([-1,-0.5])
    loop_beginSop.setParms({'method' : 1, 'blockpath' : '../block_end'})
    Meta = loop_beginSop.parm('createmetablock').pressButton()


    #CarveSop_Tree
    CarveSop = loop_beginSop.createOutputNode("carve","carve")
    CarveSop.move([0,-0.2])
    CarveSop.setParms({"firstu":0,"secondu":1})


    #resampleSop_tree
    ResampleSop = CarveSop.createOutputNode("resample","resample")
    ResampleSop.setParms({'dolength':0,'dosegs' :1,'segs':'1000'})
    ResampleSop.move([0,-0.2])
    #ResampleSop.setParms({"docurveuattr":0})


    #forLoop_Sop_end Tree
    loopendSop = ResampleSop.createOutputNode("block_end","block_end")
    loopendSop.move([0,-0.2])
    loopendSop.setParms({'itermethod':1, 'method':1,'class':0, 'useattrib':0})
    loopendSop.setParms({'blockpath':"../foreach_bigin",'templatepath':"../foreach_bigin"})

    #WrangleSop tree
    WrangleSop = loopendSop.createOutputNode("attribwrangle","rastaring")
    WrangleSop.move([0.3,-0.7])

    WranglePram = WrangleSop.parm("snippet")
    WranglePram.set('float curve = chramp("curve",@curveu);\n\n@pscale = curve*0.035;\n\
                    \n@density = fit(rand(@primnum),0,1,0.5,1);')



    #VDBSOP
    VDBSop = WrangleSop.createOutputNode("vdb","VDB")
    VDBSop.move([-2.5,0.5])
    VDBSop.setInput(0,None) #DisConenct

    VDBSop.setParms({'name1':'density','voxelsize':'0.01'})

    #rastaraiseSop tree
    rasterizeSop = WrangleSop.createOutputNode('volumerasterizeparticles','Rerasterize_point')
    rasterizeSop.move([-1.5,-0.5])
    rasterizeSop.setInput(0,VDBSop)
    rasterizeSop.setInput(1,WrangleSop)

    #End NullSop tree

    EndNullSop = rasterizeSop.createOutputNode("null","ConvertFillCurve_End")
    EndNullSop.move([0,-0.5])
    EndNullSop.setColor(hou.Color((0.5,0.4,0.0)))

    #FileCacheSop
    FileCache = EndNullSop.createOutputNode("filecache","FillVolume_Cache")
    FileCache.move([0,-0.4])
    FileCache.setParms({'loadfromdisk' : '1'})
    FileCache.setParmExpressions({'f1': '$PSTART-15','f2':'$PEND+2'})
    #===Flag===#
    FileCache.setRenderFlag(1)
    FileCache.setDisplayFlag(1)
    FileCache.setCurrent(1,1)

    del hou




def MotionTrail():
    """
    This func isThis func is SOPLevel Script
    Create Motion Trail Base System

    Samples***
    selcted Current Nodetree
    MotionTrail()
    """
    import hou

    #Create Path
    select = hou.selectedItems()
    node_Path  = str(select[0].path())

    root = hou.node(node_Path)

    #============ Motion Trail Bigin ==============#
    #Bigin_Sop Tree
    bigin_null = root.createOutputNode("null","MotionTrail")

    bigin_null.move([0,-1])
    bigin_null.setColor(hou.Color((0.5,0.4,0.0)))

    #TimeShiftSop
    timeShiftSop = bigin_null.createOutputNode("timeshift")
    timeShiftSop.move([-2,-0.3])
    timeShiftSop.setParmExpressions({"frame":'101'})

    #ScatterSop
    ScatterSop = timeShiftSop.createOutputNode("scatter")
    ScatterSop.move([0,-0.2])
    ScatterSop.setParmExpressions({"npts" : "500","relaxpoints":'0',"useprimnumattrib" : "1", "useprimuvwattrib":"1"})

    #InterPolateSop
    InterPolateSop = ScatterSop.createOutputNode("attribinterpolate")
    InterPolateSop.move([1.8,-0.3])
    InterPolateSop.setInput(1,bigin_null)

    #WrangleSop
    WrangleSop = InterPolateSop.createOutputNode("attribwrangle","Set_id")
    WrangleSop.move([0.3,-0.4])
    WrangleSop.setParms({'snippet' : 'i@id = @ptnum;'})

    #trailvelSop
    TrailvelSop = WrangleSop.createOutputNode("trail","set_velocity")
    TrailvelSop.move([0,-0.3])
    TrailvelSop.setParmExpressions({'result': '3','computeangular' : '1'})

    #trailSop
    TrailSop = TrailvelSop.createOutputNode("trail","set_Trail")
    TrailSop.move([0,-0.3])
    TrailSop.setParmExpressions({'result':'0','length':'10'})
    TrailSop.setColor(hou.Color((0.7,0,0.4)))

    #addSop
    AddSop = TrailSop.createOutputNode("add",'Conect_Pts')
    AddSop.move([0,-0.3])
    Parm = AddSop.parm('add').set(4)

    AddSop.setParms({'attrname' : 'id'})
    ParmRadio = AddSop.setParms({'stdswitcher1': '1','switcher1':'1'})
         #temp = AddSop.asCode()

    #resampleSop
    ResampleSop = AddSop.createOutputNode("resample")
    ResampleSop.move([0,-0.3])
    ResampleSop.setParms({'length' : '0.05'})

    #Endnull
    EndnullSop = ResampleSop.createOutputNode("null","Motion_Trail_OUT")
    EndnullSop.move([0,-0.3])
    EndnullSop.setColor(hou.Color((0.5,0.4,0.0)))

    #FileCacheSop
    FileCache = EndnullSop.createOutputNode("filecache","Source_MotionTrail_Cache")
    FileCache.move([1.5,-0.4])
    FileCache.setParms({'loadfromdisk' : '1'})
    FileCache.setParmExpressions({'f1': '$PSTART-15','f2':'$PEND+2'})
    #===Flag===#
    FileCache.setRenderFlag(1)
    FileCache.setDisplayFlag(1)
    FileCache.setCurrent(1,1)
    #===event===#
    #Post_Select = hou.selectedItems()
    #Post_Path  = str(Post_Select[0].path())

    #EventNode = hou.node(Post_Path)
    #EventNode.parm("execute").pressButton()

    del hou




def setPyroSim(scale):
    """
    This func is Set Pyro Simulation

    Samples***
    setPyroSim(1)
    scale... Boundry Size
    """

    import hou

    Obj = hou.node("/obj")
    #obj Network opetater
    PyroNode = Obj.createNode("geo","Pyro_Tool",run_init_scripts = 0)
    PyroNode.moveToGoodPosition()
    #Sop Network Operater
    Sect_Pyro = hou.node(PyroNode.path())

    BoundaryGuide = Sect_Pyro.createNode("box","BoundaryArea")
    BoundaryGuide.setPosition([-2.1,0.9])
    BoundaryGuide.setParms({"sizex":scale,"sizey":scale,"sizez":scale})
    BoundaryGuide.setParmExpressions({"ty":"ch('sizey')/2"})

    #local variables Pyro
    BdSizex = BoundaryGuide.parm("sizex")
    BdSizey = BoundaryGuide.parm("sizey")
    BdSizez = BoundaryGuide.parm("sizez")

    Bdtx = BoundaryGuide.parm("tx")
    Bdty = BoundaryGuide.parm("ty")
    Bdtz = BoundaryGuide.parm("tz")

    Dop_Pyro = Sect_Pyro.createNode("dopnet","LVS_PyroNetwork")

    #Dop NetWork Operater
    DopNode_Pyro = hou.node(Dop_Pyro.path())
    delOutput = (Dop_Pyro.path() + '/output' )
    hou.node(delOutput).destroy()
    #SolverGeometry
    PyroObj = DopNode_Pyro.createNode("smokeobject","Pyro")
    PyroObj.setParms({"multifield_densityfield":'density'})
    PyroObj.setParms({"multifield_showguide":1})
    PyroObj.setParms({"density_showguide":0})

    PyroObj.setParms({"sizex":BdSizex,"sizey":BdSizey,"sizez":BdSizez});
    PyroObj.setParms({"tx":Bdtx,"ty":Bdty,"tz":Bdtz});
    #Pyroobj.setParms({"closedends":0});


    #Solver
    PyroSolver = PyroObj.createOutputNode("pyrosolver","PyroSolver")
    PyroSolver.setPosition([2,-2])
    #create Resize Node
    dpresize = DopNode_Pyro.createNode("gasresizefluiddynamic","Resize_Grid")
    dpresize.setPosition([2.0,0.7]);
    PyroSolver.setInput(1,dpresize);


    #Create Gravity dop
    Gravitydop = PyroSolver.createOutputNode("gravity","Gravity")
    Gravitydop.setPosition([2.2,-3.5]);
    #create null dop
    Dopnull = Gravitydop.createOutputNode("null","OUT")
    DopnullColor = hou.Color((1.0,1.0,0.4))
    Dopnull.setPosition([2.2,-5.0])
    Dopnull.setColor(DopnullColor)
    Dopnull.setDisplayFlag(1)

    del hou





def setAlienSim(scale):
    """
    This func is Set Pyro Simulation

    Samples***
    setsetAlienSim(1)
    scale... Boundry Size
    """

    import hou

    Obj = hou.node("/obj")
    #obj Network opetater
    AlienNode = Obj.createNode("geo","Alien_Tool",run_init_scripts = 0)
    AlienNode.moveToGoodPosition()
    #Sop Network Operater
    Sect_Alien = hou.node(AlienNode.path())

    BoundaryGuide = Sect_Alien.createNode("box","BoundaryArea")
    BoundaryGuide.setPosition([-2.1,0.9])
    BoundaryGuide.setParms({"sizex":scale,"sizey":scale,"sizez":scale})
    BoundaryGuide.setParmExpressions({"ty":"ch('sizey')/2"})

    #local variables Pyro
    BdSizex = BoundaryGuide.parm("sizex")
    BdSizey = BoundaryGuide.parm("sizey")
    BdSizez = BoundaryGuide.parm("sizez")

    Bdtx = BoundaryGuide.parm("tx")
    Bdty = BoundaryGuide.parm("ty")
    Bdtz = BoundaryGuide.parm("tz")

    Dop_Alien = Sect_Alien.createNode("dopnet","LVS_AlienNetwork")

    #Dop NetWork Operater
    DopNode_Alien = hou.node(Dop_Alien.path())
    delOutput = (Dop_Alien.path() + '/output' )
    hou.node(delOutput).destroy()
    #SolverGeometry
    AlienObj = DopNode_Alien.createNode("Alien_Object","Alien")


    AlienObj.setParms({"sizex":BdSizex,"sizey":BdSizey,"sizez":BdSizez});
    AlienObj.setParms({"tx":Bdtx,"ty":Bdty,"tz":Bdtz});
    #Pyroobj.setParms({"closedends":0});


    #Solver
    AlienSolver = AlienObj.createOutputNode("Alien_Volumesolver","Alien_volume")
    AlienSolver.setPosition([2,-2])
    #create Resize Node
    dpresize = DopNode_Alien.createNode("gasresizefluiddynamic","Resize_Grid")
    dpresize.setPosition([2.0,0.7]);
    AlienSolver.setInput(1,dpresize);


    #Create Gravity dop
    Gravitydop = AlienSolver.createOutputNode("gravity","Gravity")
    Gravitydop.setPosition([2.2,-3.5]);
    #create null dop
    Dopnull = Gravitydop.createOutputNode("null","OUT")
    DopnullColor = hou.Color((1.0,1.0,0.4))
    Dopnull.setPosition([2.2,-5.0])
    Dopnull.setColor(DopnullColor)
    Dopnull.setDisplayFlag(1)

    del hou
