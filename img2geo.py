import argparse
import shutil, os
from osgeo import gdal, osr
from PIL import Image
from utils import toGCP

parser = argparse.ArgumentParser(description="Convert images to geo-referenced format")
parser.add_argument("-i", "--input", required=True, help="path to input image")
parser.add_argument("-o", "--output", required=True, help="path to output image")
parser.add_argument("-c", "--coordinates", required=True, help="coordinates to apply to the image(comma sepetated, <lat1,lon1,lat2,lon2>)")

args = vars(parser.parse_args())

# User variables
in_img = args["input"]
out_img = args["output"]
raw_coordinates = args["coordinates"]# 53.3497,-6.2873,53.3584,-6.2741

# app variables
coordination_system = 3857#4326 #WGS-84

def img2tiff(in_img, out_tiff):
    print("Converting to tiff...\t\tdone!")
    img = Image.open(in_img)
    img.save(out_tiff+'.tiff')


def tiff2geo(tiff_file, raw_coordinates, coordination_system):
    """
    convert tiff image to geo-referenced tiff with given coordinates

    Keyword arguments:
    """
    print("Building geo-referenced tiff...\tdone!")
    tiff2_file = "geo_tagged-"+tiff_file
    shutil.copy(tiff_file, tiff2_file)
    destination_tiff = gdal.Open(tiff_file, gdal.GA_Update)

    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(coordination_system)
    crs_wkt = spatial_ref.ExportToWkt()
    
    im = Image.open(tiff_file)
    width, height = im.size
    # Enter the GCPs
    #   Format: [map x-coordinate(longitude)], [map y-coordinate (latitude)], [elevation],
    #   [image column index(x)], [image row index (y)]
    ground_coord_points = []
    ground_coord_points = toGCP(raw_coordinates, width, height, 0)
    # ground_coord_points.append(gdal.GCP(-699899.0344645489,7049569.344027515,0,0,0))
    # ground_coord_points.append(gdal.GCP(-698429.6171860776,7049569.344027515,0,4921,0))
    # ground_coord_points.append(gdal.GCP(-699899.0344645489,7047946.742847497,0,0,5435))
    # ground_coord_points.append(gdal.GCP(-698429.6171860776,7047946.742847497,0,4921,5435))
    destination_tiff.SetProjection(crs_wkt)
    destination_tiff.SetGCPs(ground_coord_points, spatial_ref.ExportToWkt())
    gdal.Warp(tiff2_file, destination_tiff, dstSRS='EPSG:3857', format='gtiff')
    destination_tiff=None


if in_img.lower().endswith(('.png', '.jpg', '.jpeg')):
    img2tiff(in_img, out_img)
    tiff2geo(out_img+'.tiff', raw_coordinates, coordination_system)
    os.remove(out_img+'.tiff')
else:
    tiff2geo(out_img, raw_coordinates, coordination_system)