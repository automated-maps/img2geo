gdal_translate -of GTiff -gcp 0 0 -699899.0344645489 7049569.344027515 -gcp 4921 0 -698429.6171860776 7049569.344027515 -gcp 4921 5435 -698429.6171860776 7047946.742847497 -gcp 0 5435 -699899.0344645489 7047946.742847497 "C:/Users/lasit/Desktop/WorkSpace/img2geo/out.tiff" "C:/Users/lasit/Desktop/WorkSpace/img2geo/out_2.tiff"
gdalwarp -r near -order 1 -co COMPRESS=NONE  -t_srs EPSG:3857 "C:/Users/lasit/Desktop/WorkSpace/img2geo/out_2.tiff" "C:/Users/lasit/Desktop/WorkSpace/img2geo/result.tiff"
