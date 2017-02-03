# -*- coding:utf-8 -*-
import socket
import threading
import logging

logger = logging.getLogger(__name__)


class Instance():

    def __init__(self, area_id, ip, port):
        self.area_id = area_id
        self.ip = ip
        self.port = port
        self.unique_id = "{}:{}".format(str(ip), str(port))

    def get_unique_id(self):
        return self.unique_id

    def get_connection(self):
        return self.ip, self.port

    def get_area_id(self):
        return self.area_id

    def __repr__(self):
        return "Normal Instance - Area: {}, IP/Port: {}:{}".format(self.area_id, self.ip, self.port)


class TutorialInstance(Instance):

    def __init__(self, area_id, ip, port):
        Instance.__init__(self, area_id, ip, port)

        self.occupied = False

    def set_occupied(self):
        self.occupied = True

    def is_occupied(self):
        return self.occupied

    def __repr__(self):
        return "Tutorial Instance - Occupied: {}, Area: {}, IP/Port: {}:{}"\
            .format(self.occupied, self.area_id, self.ip, self.port)


class GameServerManager(object):

    def __init__(self):
        self.registered_normal_areas = {}
        self.registered_tutorial_areas = {}
        self.tutorial_area_lock = threading.Lock()

    def register_game_service(self, is_tutorial, area_id, udp_ip, udp_port):
        logger.error("New Instance tries to register: Tutorial: {}, Area: {}, IP/Port: {}:{}"
                     .format(is_tutorial, area_id, udp_ip, udp_port))

        if is_tutorial:
            tutorial_instance = TutorialInstance(area_id, udp_ip, udp_port)

            self.tutorial_area_lock.acquire()
            if tutorial_instance.get_unique_id() in self.registered_tutorial_areas:
                # We already have it so we need to check if it is occupied
                # If so all is good and we override it - if not we need to throw an error and don't accept
                old_tutorial_instance = self.registered_tutorial_areas.get(tutorial_instance.get_unique_id())
                if old_tutorial_instance.is_occupied():
                    logger.error("Override old tutorial Area with new one!")
                    self.registered_tutorial_areas[tutorial_instance.get_unique_id()] = tutorial_instance
                else:
                    logger.error("There was the attempt to replace an unoccupied Tutorial Area")
            else:
                self.registered_tutorial_areas[tutorial_instance.get_unique_id()] = tutorial_instance

            self.tutorial_area_lock.release()
        else:
            instance = Instance(area_id, udp_ip, udp_port)

            if instance.get_area_id() not in self.registered_normal_areas:
                self.registered_normal_areas[area_id] = [udp_ip, udp_port]
            else:
                """ TODO Build a mechanic that determines at this point if the new one is an replacement because
                the old one doesn't respond"""
                logger.error("A Normal Area connected with the same ID like an existing one!")

    def get_game_service_for_area(self, tutorial_state, area):
        # TODO Error handling if area not found
        if tutorial_state:
            return self.get_unoccupied_tutorial_area()
        else:
            return self.registered_normal_areas.get(area, None)

    def has_game_service_for_area(self, area):
        return area in self.registered_normal_areas.keys()

    def get_list_of_registered_game_services(self):
        return self.registered_normal_areas

    def get_unoccupied_tutorial_area(self):
        result = None
        self.tutorial_area_lock.acquire()
        available_areas = [e for e in self.registered_tutorial_areas.values() if not e.is_occupied()]

        if len(available_areas) > 0:
            result = available_areas[0]
            result.set_occupied()
            logger.info("A Tutorial Area was requested I gave the instance: {}".format(result))
            result = result.get_connection()
        self.tutorial_area_lock.release()
        return result

    def ping(self, is_tutorial, area_id, udp_ip, udp_port):
        print "Got Ping", is_tutorial, area_id, udp_port, udp_ip