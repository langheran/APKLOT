import json
import math
import os
import tile_extract as te
import pandas as pd
import numpy as np
import cv2
from math import ceil
from shutil import copy
import time

# ZOOM = 20 #this is the zoom used for the thesis
ZOOM = 21


def is_locked(filepath):
    """Checks if a file is locked by opening it in append mode.
    If no exception thrown, then the file is not locked.
    """
    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            # print("Trying to open %s." % filepath)
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                # print("%s is not locked." % filepath)
                locked = False
        except IOError:
            # print("File is locked (unable to open in append mode). %s." % \
                  # message)
            locked = True
        finally:
            if file_object:
                file_object.close()
                # print("%s closed." % filepath)
    # else:
        # print("%s not found." % filepath)
    return locked


def get_ground_truth(main_json, limit=-1):
    parkings = filter_parkings(main_json, "testing")
    rows = []
    columns = ['id', 'name', 'bounding_coords',
               'roi_coords', 'spots', 'lane', 'complement']
    i = 0
    for p in parkings:
        id = p['id']
        name = p['tags']['name']
        bounding_coords = get_bounding_coords_gt(p, main_json)
        roi_coords = get_roi_coords_gt(p, main_json)
        spots = []
        lane = []
        # get_complement_coords_gt(p, main_json,bounding_coords)
        complement = []
        if(i < limit or limit == -1):
            save_aerial_image(id, bounding_coords)
            # save_roi_overlay_bycoords(id, bounding_coords, roi_coords, "./roi_images")
            # save_parking_spots_roi(id)
            # save_mask(id)

        rows.append([id, name, bounding_coords,
                     roi_coords, spots, lane, complement])
        i += 1
    new_df = pd.DataFrame(rows, columns=columns)
    return new_df


def save_mask(id):
    src = os.path.join("./images", "{}.png".format(id))
    img = cv2.imread(src, 1)
    shapes = get_parking_spots(id)
    for i, shape in enumerate(shapes):
        shape.append(shape[0])
        shape = [[int(round(pt[0], 0)), int(round(pt[1], 0))] for pt in shape]
        pts = np.array(shape)
        roi_pts = pts.reshape((-1, 1, 2))
        mask = np.zeros((img.shape[0], img.shape[1]))
        cv2.fillConvexPoly(mask, roi_pts, 1)
        mask = mask.astype(np.bool)
        out = np.zeros_like(img)
        out[mask] = 255
        cv2.imwrite(os.path.join("./parking_spot_mask_images",
                                 "{}-{}.png".format(id, i)), out)


def save_parking_spots_roi(id):
    shapes = get_parking_spots(id)
    if(len(shapes) > 0):
        filename = os.path.join("./images", "{}.png".format(id))
        dst = os.path.join("./parking_spot_roi_images", "{}.png".format(id))
        if(os.path.exists(dst)):
            return
        if(not os.path.exists(filename)):
            return
        copy(filename, dst)
        for x in range(0, 2):
            for shape in shapes:
                shape.append(shape[0])
                shape = [[int(round(pt[0], 0)), int(round(pt[1], 0))]
                         for pt in shape]
                save_roi_overlay_bypoints(id, np.array(
                    shape), dst, dst, (0, 255, 0), 1)
                while is_locked(dst):
                    time.sleep(1)
                time.sleep(0.5)


def get_parking_spots(id):
    filename = os.path.join("./images", "{}.json".format(id))
    if os.path.exists(filename):
        data = load_data(filename)
        pts = [shape["points"]
               for shape in data["shapes"] if shape["label"] == "1"]
        return pts
    else:
        return []

# def get_complement_coords_gt(node, main_json,bounding_coords):


def save_aerial_image(name, bounding_coords):
    if(not os.path.exists(os.path.join("./images", "{}.png".format(name)))):
        te.tile_extract(name=str(name), dir="images", NW_lat_long=(bounding_coords['up'], bounding_coords['left']),
                        SE_lat_long=(bounding_coords['down'], bounding_coords['right']), zoom=ZOOM)


def convert_coord_point_to_pixel_point(p, bounding_coords, zoom=ZOOM):
    ullat, ullon = (bounding_coords['up'], bounding_coords['left'])
    lrlat, lrlon = (p[0], p[1])

    # Set some important parameters
    scale = 1
    maxsize = 640

    # convert all these coordinates to pixels
    ulx, uly = te.latlontopixels(ullat, ullon, zoom)
    lrx, lry = te.latlontopixels(lrlat, lrlon, zoom)

    # calculate total pixel dimensions of final image
    dx, dy = lrx - ulx, uly - lry

    # calculate rows and columns
    x, y = int(ceil(dx / maxsize)), int(ceil(dy / maxsize))
    return [dx, dy]


def save_roi_overlay_bycoords(name, bounding_coords, roi_coords, foldername):
    pts = np.array(list(map(lambda c: convert_coord_point_to_pixel_point(
        c, bounding_coords), roi_coords)), np.int32)
    filename = os.path.join("./images", "{}.png".format(name))
    if (os.path.exists(filename)):
        dst = os.path.join(foldername, "{}.png".format(name))
        if (not os.path.exists(dst)):
            save_roi_overlay_bypoints(name, pts, filename, dst)


def save_roi_overlay_bypoints(name, roi_pts, src, dst, line_color=(0, 0, 255), line_width=5):
    img = cv2.imread(src, 1)
    roi_pts = roi_pts.reshape((-1, 1, 2))
    cv2.polylines(img, [roi_pts], True, line_color, line_width)
    cv2.imwrite(dst, img)


def get_roi_coords_gt(node, main_json):
    return [[i['lat'], i['lon']] for i in [[x for x in main_json['elements'] if x['id'] == n][0] for n in node['nodes']]]


def get_bounding_coords_gt(node, main_json):
    up = -math.inf  # node['max-lat']
    right = -math.inf  # node['max-lon']
    down = math.inf  # node['min-lat']
    left = math.inf  # node['min-lon']
    for n in node['nodes']:
        n = [x for x in main_json['elements'] if x['id'] == n][0]
        if (n['lat'] > up):
            up = n['lat']
        if (n['lon'] > right):
            right = n['lon']
        if (n['lat'] < down):
            down = n['lat']
        if (n['lon'] < left):
            left = n['lon']
    return {'up': up, 'right': right, 'down': down, 'left': left}


def load_data(filename='./OSM/madrid_parkings.js'):
    with open(filename, 'r', encoding='utf-8') as f:
        read_data = f.read()
    data = json.loads(read_data)
    return data


def filter_buildings(data):
    parkings = [x for x in data['elements'] if (
        x['type'] == 'way' and 'tags' in x.keys() and 'name' in x['tags'].keys() and (('building' in x['tags'].keys() and x['tags']['building'].lower() == 'yes') or ('parking' in x['tags'].keys() and x['tags']['parking'].lower() == 'underground')))]
    return parkings


def delete_image(parking):
    filename = os.path.join('./images', '{}.png'.format(parking['id']))
    if os.path.exists(filename):
        os.remove(filename)


def delete_buildings(data):
    buildings = filter_buildings(data)
    for x in buildings:
        delete_image(x)


def filter_parkings(data, idfolder=None):
    if idfolder is None:
        parkings = [x for x in data['elements'] if (
            x['type'] == 'way' and 'tags' in x.keys() and 'name' in x['tags'].keys() and not x['tags'][
                'name'].lower().startswith(
                'ret') and 'nodes' in x.keys() and len(x['nodes']) > 5 and not (('building' in x['tags'].keys() and x['tags']['building'].lower() == 'yes') or ('parking' in x['tags'].keys() and x['tags']['parking'].lower() == 'underground')))]
    else:
        fileids = [file.replace('.png', '').replace('.jpg', '')
                   for file in os.listdir(os.path.join(os.getcwd(), idfolder))]
        parkings = [x for x in data['elements'] if str(x['id']) in fileids]
    return parkings


if __name__ == "__main__":
    madrid_json = load_data()

    campinas_json = load_data("./OSM/campinas_parkings.js")
    santiago_json = load_data("./OSM/santiago_parkings.js")
    houston_json = load_data("./OSM/houston_parkings.js")
    chicago_json = load_data("./OSM/chicago_parkings.js")
    losangeles_json = load_data("./OSM/losangeles_parkings.js")
    newyork_json = load_data("./OSM/newyork_parkings.js")
    tokio_json = load_data("./OSM/tokio_parkings.js")
    madrid_json["elements"] += campinas_json["elements"]
    madrid_json["elements"] += santiago_json["elements"]
    madrid_json["elements"] += houston_json["elements"]
    madrid_json["elements"] += chicago_json["elements"]
    madrid_json["elements"] += losangeles_json["elements"]
    madrid_json["elements"] += newyork_json["elements"]
    madrid_json["elements"] += tokio_json["elements"]

    delete_buildings(madrid_json)
    df = get_ground_truth(madrid_json, 2000)
    df.to_csv('gt.csv', index=False)
