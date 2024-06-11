# version h.19.5.919

import hou

def make_stage():
  #GetToCurrentContextfromSOP
  getParentContext = hou.pwd().parent() 
  
