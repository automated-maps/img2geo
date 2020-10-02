import math
from osgeo import gdal
from PIL import Image
from pyproj import Transformer
import mercantile


EarthRadius = 6378137;
MinLatitude = -85.05112878;
MaxLatitude = 85.05112878;
MinLongitude = -180;
MaxLongitude = 180;

class Point():
	def __init__(self,lat,lon):
		self.lat = float(lat)
		self.lon = float(lon)

	def getLat(self):
		return self.lat

	def getLon(self):
		return self.lon

	def __str__(self):
		return str((self.getLat(),self.getLon()))

	def str(self):
		return str(self.getLat()) + ',' + str(self.getLon())

# Parsing the lat and lon to 4 points
# p1:top-left p2:top-right p3:bottom-left p4:bottom-right
def parseToPoints(ip):
	x1,y1,x2,y2 = map(float,ip.split(','))
	X1 = max(x1,x2)
	X2 = min(x1,x2)
	Y1 = min(y1,y2) 
	Y2 = max(y1,y2)
	return Point(X1,Y1),Point(X1,Y2),Point(X2,Y1),Point(X2,Y2)

def projection_3857(point):
	transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
	x, y =  transformer.transform( point.getLat(), point.getLon())
	return x, y

def toGCP(coordinates, width, height, elevation):
	arr  = parseToPoints(coordinates)
	arr2 = [[0,0], [width,0], [0,height], [width,height]]
	gcp = []
	for i in range(len(arr)):
		lon,lat = projection_3857(arr[i]) 
		gcp.append(gdal.GCP(lon, lat, elevation, arr2[i][0], arr2[i][1]))
		# print("ground_coord_points.append(gdal.GCP({},{},0,{},{}))".format(lon, lat, arr2[i][0],arr2[i][1]))
	return gcp

def quadKeyToip(qyadkey):
	tile = mercantile.quadkey_to_tile(qyadkey)
	[left,bottom,right,top] = mercantile.bounds(tile.x, tile.y, tile.z)
	return [left,bottom,right,top]

# bbox = quadKeyToip("0313103132223020121")
# print(",".join([str(i) for i in bbox]))