import random
import time
from server.components.MovableComponent import MovableComponent


class RobotEnemy(object):

    def __init__(self, id, position, initial_life_points):
        self.id = id
        self.current_life_points = random.randint(25, 32)
        self.max_life_points = initial_life_points
        self.marked_destroyed = False
        self.marked_changed = False

        self.components = {}
        self.components["MovableComponent"] = MovableComponent(position)

    def get_moving_component(self):
        return self.components["MovableComponent"]

    def get_current_life_points(self):
        return self.current_life_points

    def get_max_life_points(self):
        return self.max_life_points

    def remove_hitpoints(self, hitpoint):
        if self.current_life_points - hitpoint <= 0:
            self.current_life_points = 0
            return True
        self.current_life_points -= hitpoint
        return False

    def handle_bullet_hit(self, bullet):
        # Make sure that a bullet doesn't affect things twice
        if not bullet.is_marked_hit():
            bullet.mark_hit()
            damage = bullet.get_damage()

            if self.remove_hitpoints(damage):
                self.marked_destroyed = True

            self.mark_changed()

    def is_marked_destroyed(self):
        return self.marked_destroyed

    def get_id(self):
        return self.id

    def mark_changed(self):
        self.marked_changed = True

    def get_and_reset_mark_changed(self):
        d = self.marked_changed
        self.marked_changed = False
        return d


class RoboticVacuumCleaner(RobotEnemy):

    INITIAL_LIFE_POINTS = 32

    def __init__(self, enemy_id, position):
        RobotEnemy.__init__(self, enemy_id, position, RoboticVacuumCleaner.INITIAL_LIFE_POINTS)