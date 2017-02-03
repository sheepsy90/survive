# -*- coding:utf-8 -*-


class CombatSystem():

    def __init__(self, server_level, bullet_system):
        self.bullet_system = bullet_system
        self.server_level = server_level

    def handle(self, players, enemies):
        # First check for every bullet that is flying if it hits something
        for bullet in self.bullet_system.get_bullets():
            bx = int(bullet.get_bullet_x())
            by = int(bullet.get_bullet_y())

            for enemy in enemies:
                mc = enemy.get_moving_component()
                if mc.is_moving():
                    position = mc.get_interpolated_position()
                else:
                    position = mc.get_discrete_position()

                d, x, y = position

                if bx == int(x) and  by == int(y):
                    enemy.handle_bullet_hit(bullet)

            # TODO - Check if the bullet behaviour through guard spots is correct
            walkable_result = self.server_level.is_walkable(bx, by)

            if not walkable_result.is_walkable:
                if not bullet.is_marked_hit():
                    bullet.mark_hit()