# version h.19.5.919

import hou

def make_stage():
  #GetToCurrentContextfromSOP
  getParentContext = hou.pwd().parent() 
  #createNode("node_name,new_name)
  lopstageNode = getParentContext.createNode('lopnet','stage')






#NEWVER
  # version h.19.5.919
import hou

def make_stage():
    current_context = hou.pwd().parent()
    
    #current_context.createNode('lopnet')
    #serch_currentContextNodes
    nodeResource = current_context.glob("*")
    nodelist =[] 
    for i in  current_context.glob("*"):
    
        nodelist.append(i) 
        
        
    print (nodelist)           
               
  
make_stage()


  


    

