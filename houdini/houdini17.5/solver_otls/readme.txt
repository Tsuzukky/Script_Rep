#2019/08/29
#Houdini Solver_otls
#Created by Masato Tsuzuki

#PointVorticles

v@up = qconvert(quaternion(fit(rand(@ptnum),0,1,-1,1),normalize(curlnoise(@P))));
