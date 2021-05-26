import hou
import sys
import platform



OS = platform.system()

ScriptsPath = "/houdini/houdini16.5/scripts/python/python27"
LibraryPath = "/libs/python27"


if OS == 'Linux':

   try:
       LinPath = ("/ppi/Ldrv/Library/fx/work/mtsuzuki/kronos")
       sys.path.append(LinPath + ScriptsPath)
       sys.path.append(LinPath + LibraryPath)


   except:
       pass

if OS == 'Windows':

   try:
       WinPath = (r"L:/Library/fx/work/mtsuzuki/kronos")
       sys.path.append(WinPath + ScriptsPath)
       sys.path.append(WinPath + LibraryPath)


   except:
       pass



try:

    sys.path.append("/ppi/Ldrv/Library/fx/work/mtsuzuki/Projects/LVS/pkg/rev001/ScriptTool_LVS")

except:
    pass
