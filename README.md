# Convert image to geo-referenced *tiff* file
### Input
- -i : input image (jpg, png, tiff)
- -o : output image name
- -c : coordinates of the image corners [min Longitude , min Latitude , max Longitude , max Latitude]

### Output
- geo-referenced tiff file

### Files
- img2geo.py : python program
- utils.py   : helper functions
- run.bat    : Windows .bat file that can be used to same functionality 

### How to run
```bash
python .\img2geo.py -i .\result_z19.jpeg  -o test -c 53.3497,-6.2873,53.3584,-6.2741
```
___

> Manual geo-referencing

![manual](results/manual_geo_referencing.png)

> Automated process 

![automated_1](results/geo-ref_2.png)