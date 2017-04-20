from math import sin, cos, atan, exp, log, pi
from PIL import Image
import cv2
import numpy as np
import urllib


LATITUDE_RANGE = (-85.05112878, 85.05112878)
LONGITUDE_RANGE = (-180., 180.)
EARTH_RADIUS = 6378137

def clip(n, minMax):
    return min(max(n, minMax[0]), minMax[1])

def map_size(level):
    return 256 << level

def ground_resolution(lat, level):
    lat = clip(lat, LATITUDE_RANGE)
    return cos(lat * pi / 180) * 2 * pi * EARTH_RADIUS / map_size(level)

def map_scale(lat, level, dpi):
    return ground_resolution(lat, level) * dpi / 0.0254

def geo_to_pixel(geo, level):
    lat, lon = float(geo[0]), float(geo[1])
    lat = clip(lat, LATITUDE_RANGE)
    lon = clip(lon, LONGITUDE_RANGE)
    x = (lon + 180) / 360
    sin_lat = sin(lat * pi / 180)
    y = 0.5 - log((1 + sin_lat) / (1 - sin_lat)) / (4 * pi)
    mapsize = map_size(level)
    pixel_x = int(clip(x * mapsize + 0.5, (0, mapsize - 1)))
    pixel_y = int(clip(y * mapsize + 0.5, (0, mapsize - 1)))
    return pixel_x, pixel_y

def pixel_to_tile(pixel):
    return pixel[0] / 256, pixel[1] / 256

def tile_to_quadkey(tile, level):
    tile_x = tile[0]
    tile_y = tile[1]
    quadkey = ""
    for i in xrange(level):
        bit = level - i
        digit = ord('0')
        mask = 1 << (bit - 1)  # if (bit - 1) > 0 else 1 >> (bit - 1)
        if (tile_x & mask) is not 0:
            digit += 1
        if (tile_y & mask) is not 0:
            digit += 2
        quadkey += chr(digit)
    return quadkey

def from_geo(geo, level):
    pixel = geo_to_pixel(geo, level)
    tile = pixel_to_tile(pixel)
    return tile

def get_images(keys):
    ext = ".jpeg"
    #urlA = 'http://t0.tiles.virtualearth.net/tiles/a'
    #urlB = '.jpeg?g=854&mkt=en-US&token=Anz84uRE1RULeLwuJ0qKu5amcu5rugRXy1vKc27wUaKVyIv1SVZrUjqaOfXJJoI0'
    urlA = 'http://h0.ortho.tiles.virtualearth.net/tiles/h'
    urlB = '.jpeg?g=131'
    #023131022213211200
    
    
    for i in range(0,len(keys)):
        filename = str(i+1)+ext
        
        url = urlA + keys[i] + urlB
        urllib.urlretrieve(url,filename)

def stitch_image():
    img1 = cv2.imread('1.jpeg')
    img2 = cv2.imread('2.jpeg')
    img3 = cv2.imread('3.jpeg')
    img4 = cv2.imread('4.jpeg')
    
    img5 = cv2.imread('5.jpeg')
    img6 = cv2.imread('6.jpeg')
    img7 = cv2.imread('7.jpeg')
    img8 = cv2.imread('8.jpeg')
    
    img9 = cv2.imread('9.jpeg')
    img10 = cv2.imread('10.jpeg')
    img11 = cv2.imread('11.jpeg')
    img12 = cv2.imread('12.jpeg')
    
    
    i = [[img1,img2,img3,img4],[img5,img6,img7,img8],[img9,img10,img11,img12]]
    
    result = np.hstack((np.vstack(i[0]),np.vstack(i[1]),np.vstack(i[2])))
    
    cv2.imwrite('result.jpeg',result)

def main():
   #Lat1 & Lon 1 is Cloud Gate
    lat1 = 41.8757944
    lon1 = -87.621137
   #Lat2 & Lon 2 is Buckingham Fountain
    lat2 = 41.8826013
    lon2 = -87.6245621
    print("--Tiles generating for given 2 points--")
    x = from_geo((lat1,lon1), 17)
    y = from_geo((lat2,lon2), 17)
    print("---Tiles generating between 2 points---")
    zipped = []
    if (x[0]>y[0]):
        t = y
        y = x
        x = t
    for i in range(x[0],y[0]+1):
        for j in range(x[1],y[1]+1):
            zipped.append((i,j))
    print("Total tiles generated: %d" %len(zipped))
    print("--Generating Quadkeys for generated tiles--")
    keys = []
    for i in range(0,len(zipped)):
        print(zipped[i])
        keys.append(tile_to_quadkey(zipped[i], 17))
    print("--Quadkeys Generated--")
    print("--Downloading images for quadkeys--")
    get_images(keys)
    print("--Stiching images--")
    stitch_image()
    print("Final image generated.")

if __name__ == '__main__':
    main()
