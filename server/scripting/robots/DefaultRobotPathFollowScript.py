# -*- coding:utf-8 -*-
import random
import time
from server.constants.constans import EnemySystemQueueConstants


class DefaultRobotPathFollowScript():

    def __init__(self, server_level, enemy_system_buffer_queue, pathway_list, list_of_robots):
        self.server_level = server_level
        self.pathway_list = pathway_list
        self.list_of_robots = list_of_robots
        self.enemy_system_buffer_queue = enemy_system_buffer_queue

        self.current_path_positions = {
            e.get_id(): random.randint(0, len(self.pathway_list)) for e in self.list_of_robots
        }

        self.last_attack_time = {
            e.get_id(): time.time()+random.random() for e in self.list_of_robots
        }


    def initialize(self):
        """ This method is called immediately after the creation and makes
            sure the robots are placed correctly initially """
        pass

    def perform(self):

        # Movement
        for local_robot in self.list_of_robots:
            move_component = local_robot.get_moving_component()

            if not move_component.is_moving():
                index = self.current_path_positions[local_robot.get_id()]

                if len(self.pathway_list)-1 <= index + 1:
                    self.current_path_positions[local_robot.get_id()] = 0
                else:
                    self.current_path_positions[local_robot.get_id()] += 1

                index = self.current_path_positions[local_robot.get_id()]

                ti, tj = self.pathway_list[index]

                walkable_result = self.server_level.is_walkable(ti, tj)

                if walkable_result.is_walkable:
                    move_component.start_moving((1, ti, tj))
                else:
                    print "NOT WALKABLE"

            if move_component.is_moving():
                move_component.is_moving_finished()
                self.enemy_system_buffer_queue.push(EnemySystemQueueConstants.CHANGED_ENEMIES, local_robot)

        # Attacking
            if not local_robot.is_marked_destroyed():
                last_attacked = self.last_attack_time[local_robot.get_id()]

                if (time.time() - last_attacked) > 5:
                    if random.random() > 0.95:
                        self.last_attack_time[local_robot.get_id()] = time.time()
                        self.enemy_system_buffer_queue.push(EnemySystemQueueConstants.ATTACKING_ENEMIES, local_robot)
