#GameDesignFinal 
#3DattemptGameDesign

#from google.colab import drive
import numpy as np
import math
from PIL import Image
#drive.mount('/content/drive')
#%cd /content/drive/My Drive/0 Randolph


def objReader(file):
  with open(file) as blend:
    x_offset = 0
    y_offset = -0.5
    z_offset = 3
    verticies = []
    tris = []

    for line in blend.readlines():
      line = line.strip() # if given "  brad s  " strip will return "brad s"
      if not line:
        continue
      #color = np.array(randColor())
      parts = line.split()
      if parts[0] == 'v':
        x = float(parts[1]) + x_offset
        y = float(parts[2]) + y_offset
        z = float(parts[3]) + z_offset

        point = ([x,y,z])
        verticies.append(point)
      if parts[0] == 'f':
        v0 = verticies[int(parts[1])-1]
        v1 = verticies[int(parts[2])-1]
        v2 = verticies[int(parts[3])-1]

        tri = (v0,v1,v2,color)
        tris.append(tri)
    return tris



class Texture:
	def __init__(self,img):
		self.image = np.array(Image.open(img))
		self.x,self.y = img.shape
		self.size = (self.x,self.y)
	def get_texture(self):
		return self.image
	def get_size(self):
		return self.size
	def textureMap(self,i,j):
		while i >= size[0]:
  			if i >= size[0]:
  				i =  i - size[0]
		while j >= size[1]:
			if j >= size[1]:
				j =  j - size[1]
		return (i,j)


class Equations:


# v, a, and b are 3-tuples; s is scalar

	#return a dot b
	def dot(a,b):
		return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

	#return a cross b
	def cross(a,b):
		return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

	#return magnitude of v
	def mag(v):
		return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

	#return normalized v
	def normalize(v):
		m = mag(v)
		return (v[0]/m, v[1]/m, v[2]/m)

	#return a - b
	def sub(a,b):
		return (a[0]-b[0],a[1]-b[1],a[2]-b[2])

	#return a + b
	def add(a,b):
		return (a[0]+b[0],a[1]+b[1],a[2]+b[2])

	#return a / s
	def div(a,s):
		return (a[0]/s, a[1]/s, a[2]/s)

	#return a * s
	def mult(a,s):
		return (a[0]*s, a[1]*s, a[2]*s)

class ThreeD:
	def __init__(img,point,scrn,objs,dis,background,ight):

		#image
		self.image = img
		#background
		self.background = background
		#light
		self.light = light
		#where camera is
		self.cameraCords = point
		#where img is being put
		self.screen = scrn
		#distance of camera to screen
		self.fd=dis
		self.objects = objs
		#size of length and width
		self.x = img.shape[0] -1
		self.y = img.shape[1] -1
		self.ratio = y/x
	
	def create():
		sY=0
	#pixels x location on screen
		sX=0
	#quick rename to simplify code
		e = self.cameraCords
		closestSphere=None
		min_intersect = 30000
		sem = [int(rd.random()*342),int(rd.random()*523)]
		setter = textureMap(sem[0],sem[1])
		for i in range(self.x+1):
			for j in range(self.y+1):
				sX = j * (2/self.x) - 1
				sY = -1 * (i * (2/self.y) - 1)
			#pixels location
				s = [sX,sY,fd]
				v = sub(s,e)
				d = normalize(v)
				setter = textureMap(setter[0],setter[1])
				closestObj, minT, cC = self.setTriangles(e,objects,e,d,self.light,setter)
				if closestObj is None:
					pixelColor = self.background
					image[i,j]=pixelColor
					continue
				pixelColor = cC
				P = add(e , mult(d,minT)) #3D coordinate
				normP = normalize(sub(P,closestObj[0])) #surface normal
			#if not normalized, p-C would be the radius
				L = light #normalize(light - P)
				shadows,minTS, o = setTriangles(P,objects,e,L,light,setter)
				if shadows is not None:
					pixelColor = np.array([0,0,0])
				else:
					pixelColor = np.array(pixelColor)
				image[i, j] = pixelColor
		return image



