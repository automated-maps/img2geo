import argparse
import shutil
import os
from osgeo import gdal, osr
from PIL import Image
from utils import toGCP, parseToPoints, quadKeyToip

def img2tiff(in_img, out_tiff):
    print("Converting to tiff...\t\tdone!")
    img = Image.open(in_img)
    img.save(out_tiff+'-.tiff')

# python .\img2geo.py -i .\result_z19.jpeg  -o test -c 53.3497,-6.2873,53.3584,-6.2741
def tiff2geo(tiff_file, raw_coordinates, coordination_system):
    """
    convert tiff image to geo-referenced tiff with given coordinates
    Keyword arguments:
    """
    print("Building geo-referenced tiff...\tdone!")
    
    tiff2_file = tiff_file.split("-")[0]+".tiff"
    
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

def main():
    parser = argparse.ArgumentParser(description="Convert images to geo-referenced format")
    parser.add_argument("-i", "--input", required=True, metavar="", help="path to input image")
    parser.add_argument("-o", "--output", required=True, metavar="", help="path to output image")
    parser.add_argument("-c", "--coordinates", required=False, metavar="", help="coordinates to apply to the image(comma sepetated, <lat1,lon1,lat2,lon2>)")
    parser.add_argument("-q", "--quadkey", default=False, required=False, metavar="", help="Specify the quadkey image")
    args = vars(parser.parse_args())
    # User variables
    in_img = args["input"]
    out_img = args["output"]
    raw_coordinates = args["coordinates"]# 53.3497,-6.2873,53.3584,-6.2741

    # app variables
    coordination_system = 3857 #WGS-84

    if(args["quadkey"]):
        # print("quad key object detected")
        key = in_img.split("\\")[len(in_img.split("\\"))-1].split(".")[0]
        print("quadkey: ", key)
        img2tiff(in_img, out_img)
        lst_ip = quadKeyToip(key)
        tiff2geo(out_img+"-.tiff", lst_ip, 3857)
        print("Removing temporary files...\tdone!")
        os.remove(out_img+"-.tiff")
        print("\nRun gdalinfo to list the geo tags")
    else:
        if(raw_coordinates is not None):
            # print("Other type detected!")
            if in_img.lower().endswith(('.png', '.jpg', '.jpeg')):
                img2tiff(in_img, out_img)
                tiff2geo(out_img+'-.tiff', raw_coordinates, coordination_system)
                os.remove(out_img+'-.tiff')
            else:
                tiff2geo(out_img, raw_coordinates, coordination_system)
            print("\nRun gdalinfo to list the geo tags")
        else:
            print("Missing coordinates")
def test():
    data_dir = os.path.join("data")
    quadKeyImage = "031310313222122222.jpeg"
    img_path = os.path.join(data_dir, quadKeyImage)

    key = quadKeyImage.split('.')[0]
    
    save_path = os.path.join(data_dir, key)
    img2tiff(img_path, save_path)

    lst_ip = quadKeyToip(key)
    tiff2geo(save_path+".tiff", lst_ip, 3857)


if __name__=="__main__":
    main()
    # test()