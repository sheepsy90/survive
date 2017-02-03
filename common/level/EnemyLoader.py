# -*- coding:utf-8 -*-
import math



class TiledEnemy():

    def __init__(self, tile_list, robot_type, robot_count, robot_script_key):
        self.tile_list = tile_list
        self.robot_type = robot_type
        self.robot_count = robot_count
        self.robot_script_key = robot_script_key

    def get_pathway_list(self):
        return self.tile_list

    def get_robot_type(self):
        return self.robot_type

    def get_robot_count(self):
        return self.robot_count

    def get_robot_script_key(self):
        return self.robot_script_key

    @staticmethod
    def point_in_ellipse(x, y, xp, yp, h_diameter, v_diameter):
        #tests if a point[xp,yp] is within
        #boundaries defined by the ellipse
        #of center[x,y], diameter d D, and tilted at angle
        # DEFAULT ANGLE IS ZERO - This can be added again fi necessary
        cosa = math.cos(0)
        sina = math.sin(0)
        dd = (h_diameter/2)**2
        DD = (v_diameter/2)**2

        a = math.pow(cosa*(xp-x)+sina*(yp-y), 2)
        b = math.pow(sina*(xp-x)-cosa*(yp-y), 2)
        ellipse = (a/dd)+(b/DD)

        if ellipse <= 1:
            return True
        else:
            return False

    @staticmethod
    def calculate_tile_list_rect(object):

        x_start = object[u'x']
        y_start = object[u'y']
        width = object[u'width']
        height = object[u'height']

        tiled_point_list = []

        for i in range(int(x_start), int(x_start+width), 1):
            for j in range(int(y_start), int(y_start+height), 1):
                xl = int(i / 32.)
                yl = int(j / 32.)

                if (xl, yl) not in tiled_point_list:
                    tiled_point_list.append((xl, yl))

        print "TPL", tiled_point_list

        return tiled_point_list

    @staticmethod
    def calculate_tile_list_ellipse(object):

        x_start = object[u'x']
        y_start = object[u'y']
        width = object[u'width']
        height = object[u'height']

        center = (x_start+width/2, y_start+height/2)
        hradius = width/2
        vradius = height/2

        x_start = math.floor((center[0]-hradius) / 32.0)
        x_end = math.floor((center[0]+hradius) / 32.0) + 1
        y_start = math.floor((center[1]-vradius) / 32.0)
        y_end = math.floor((center[1]+vradius) / 32.0) + 1

        tiled_point_list = []

        for i in range(int(x_start), int(x_end), 1):
            for j in range(int(y_start), int(y_end), 1):

                found_one = False
                resolution = 2
                for k in range(0, 32, resolution):
                    for h in range(0, 32, resolution):
                        x, y = i*32+k, j*32+h
                        if TiledEnemy.point_in_ellipse(x, y, center[0], center[1], 2*hradius, 2*vradius):
                            found_one = True
                            break
                    if found_one:
                        break

                if found_one:
                    tiled_point_list.append((i, j))

        return tiled_point_list

    @staticmethod
    def calculate_tile_list_polyline(object):
        polyline_points = object[u'polyline']

        # Get the base points that the polyline object has
        x_base = object[u'x']
        y_base = object[u'y']

        # Reserve a storage for the points we need to test for
        xpnts = []
        ypnts = []

        # Create all points we want to test
        for i in range(len(polyline_points)-1):
            xa = polyline_points[i][u'x'] + x_base
            ya = polyline_points[i][u'y'] + y_base
            xb = polyline_points[i+1][u'x'] + x_base
            yb = polyline_points[i+1][u'y'] + y_base

            ts = [t/128.0 for t in range(128)]

            for element in ts:
                xn = xa*(1-element) + xb*element
                yn = ya*(1-element) + yb*element

                xpnts.append(xn)
                ypnts.append(yn)

        tile_point_list = []

        for i in range(len(xpnts)):
            xt = xpnts[i]
            yt = ypnts[i]

            xl = int(xt / 32.)
            yl = int(yt / 32.)

            if len(tile_point_list) == 0:
                tile_point_list.append((xl, yl))
            elif len(tile_point_list) > 0 and (xl, yl) != tile_point_list[-1]:
                tile_point_list.append((xl, yl))

        return tile_point_list
