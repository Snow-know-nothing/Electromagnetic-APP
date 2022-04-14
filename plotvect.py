import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

ao = 22.86
bo = 10.16
d  = 15
H0 = 1
f  = 9.375 * pow(10, 9)
print(f)
a=ao/1000
b=bo/1000
lc=2*a    
l0=(3*pow(10, 8))/f
u=4*math.pi*pow(10, -7)
#t = np.linspace(0,20,200)/(3*pow(10, 8))

lg=l0/(math.sqrt(1-pow((l0/lc),2)))
c=lg
print(c)
B=2*math.pi/lg
w=2*math.pi*f
x=np.linspace(0,a,d)
y=np.linspace(0,b,d)
z=np.linspace(0,c,d)
        #  t = np.linspace(0, 1.0, 100)
        #  for i in range(len(t)):

x1,y1,z1= np.meshgrid(x,y,z) 
ex=np.zeros_like(x1)
ey=w*u*a*H0*np.sin(np.pi/a*x1)*np.sin(w*0-B*z1)/np.pi
ez=np.zeros_like(x1)

hy=np.zeros_like(x1)
hx=B*a*H0*np.sin(np.pi/a*x1)*(-np.sin(w*0-B*z1))/np.pi
hz=H0*np.cos(np.pi/a*x1)*np.cos(w*0-B*z1)

fig = plt.figure()
ax = Axes3D(fig,auto_add_to_figure=False)
fig.add_axes(ax)
#plt.gca().set_box_aspect((3, 5, 2)) 
#ax = plt.figure().add_subplot(projection='3d')figsize=plt.figaspect(0.5)*1.5
ax.set_box_aspect((c,a,b))
ax.quiver(z1,x1,y1,ez,ex,ey,color='red',length=0.0008, normalize=True)
ax.quiver(z1,x1,y1,hz,hx,hy,color='blue',length=0.0008, normalize=True)
plt.show()


# Make the grid

# x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.2),
#                       np.arange(-0.8, 1, 0.2),
#                       np.arange(-0.8, 1, 0.8))

# # Make the direction data for the arrows
# u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
# v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
# w = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
#      np.sin(np.pi * z))

# ax.quiver(x, y, z, u, v, w, length=0.1,normalize=True)

# plt.show()