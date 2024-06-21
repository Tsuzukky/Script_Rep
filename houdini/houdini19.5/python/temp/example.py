# version h.19.5.919
import hou




def make_stage():
    current_context = hou.pwd().parent()
    currentNodepos = hou.pwd().position()
    
    #serch_currentContextNodes
    nodeResource = current_context.glob("*")
    nodeNamelist =[]
    
    for i in  nodeResource:
    
       nodeNamelist.append(i.name())
        
        
    if 'stage' in nodeNamelist :
                 
        pass
        
    else:
        stageNode = current_context.createNode('lopnet','stage')
        stageNode.setColor(hou.Color((0.5,0.4,0.0)))
        #Organize nodeposition
        stageNode.shiftPosition(currentNodepos)
        stageNode.move([-1.5,-1])
        
        #stageNode.
        #inside_Stage_inside
        stageContext = hou.node(stageNode.path())
        

        makeLooadShot = stageContext.createNode('dpipe_LoadShot_v1')
        makeconfigurenode =  makeLooadShot.createOutputNode('configurestage','loadmask_asset')
        makenullnode =  makeconfigurenode .createOutputNode('null','SHOT')
        makenullnode.setDisplayFlag(1)
        
        #update parms #you can check parmname from parmName.eval()
        makeconfigurenode.setParms({'editload':'addremove'})
        
def make_ROP():
    
    current_context = hou.pwd().parent()
    currentNodepos = hou.pwd().position()
    
    #serch_currentContextNodes
    nodeResource = current_context.glob("*")
    nodeNamelist =[]
    
    for i in  nodeResource:
    
       nodeNamelist.append(i.name())
        
        
    if 'ROP' in nodeNamelist :
                 
        pass
        
    else:
        ROPNode = current_context.createNode('ropnet','ROP')
        #Organize nodeposition
        ROPNode.shiftPosition(currentNodepos)
        ROPNode.move([1.5,-1])
        
     
     
def make_parameters():
    
    #create parameters for python
    node = hou.pwd()
    parmtempGroup = node.parmTemplateGroup()
    #ButtomParmTemplate
    parm1 = hou.ButtonParmTemplate('Build_structure','Build_structure')
    parm2 = hou.LabelParmTemplate(
    parmtempGroup.append(parm1)
    node.setParmTemplateGroup(parmtempGroup)

    
    
make_parameters()
