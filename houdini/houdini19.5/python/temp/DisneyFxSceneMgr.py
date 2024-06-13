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
        
        makeLooadShot = stageContext.createNode('null','SHOT')
        makeLooadShot = stageContext.createNode('dpipe_LoadShot_v1')
        
        
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
        
     
     

make_stage()
