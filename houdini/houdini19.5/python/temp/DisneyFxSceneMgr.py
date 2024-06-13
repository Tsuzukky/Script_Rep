# version h.19.5.919
import hou

def make_stage():
    current_context = hou.pwd().parent()
    
   
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
            
                    
               
  
make_stage()


  


    
