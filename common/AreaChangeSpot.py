# -*- coding:utf-8 -*-


class AreaChangeSpot(object):

    def __init__(self, source_position, target_level_id, target_position):
        self.source_position = source_position
        self.target_level_id = target_level_id
        self.target_position = target_position

    def get_source_coordinates(self):
        return self.source_position

    def get_target_level_id(self):
        return self.target_level_id

    def get_target_position(self):
        return self.target_position

    @staticmethod
    def from_tiled_object(tiled_object):
        """ This is the method building area change spots from the map files """
        assert u'type' in tiled_object
        assert u'y' in tiled_object
        assert u'y' in tiled_object
        assert u'x' in tiled_object
        assert u'properties' in tiled_object
        assert u'area_transition' in tiled_object[u'properties']

        tarea, tdirection, tx, ty = tiled_object[u'properties'][u'area_transition'].split(",")
        tarea, tdirection, tx, ty = int(tarea), int(tdirection), int(tx), int(ty)

        assert 1 <= tdirection <= 4
        assert 0 <= tx
        assert 0 <= ty
        assert 0 <= tarea

        assert tiled_object[u'x'] == int(tiled_object[u'x']), "The object with id %i is not placed properly" % type
        assert tiled_object[u'y'] == int(tiled_object[u'y']), "The object with id %i is not placed properly" % type
        assert tiled_object[u'rotation'] == 0

        fx, fy = tiled_object[u'x']+16, tiled_object[u'y']-1
        fx, fy = fx / 32,  fy/32

        return AreaChangeSpot(source_position=(fx, fy),
                              target_level_id=tarea,
                              target_position=(tdirection, tx, ty))

    def __repr__(self):
        return "AreaChange Spot with Source {} and Target {} with LevelTarget {}".format(self.source_position,
                                                                                         self.target_position,
                                                                                         self.target_level_id)