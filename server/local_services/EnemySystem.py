from server.character_representations.RobotEnemy import RoboticVacuumCleaner
from server.constants.constans import EnemySystemQueueConstants
from server.scripting.robots.DefaultRobotPathFollowScript import DefaultRobotPathFollowScript

ROBOT_SCRIPT_MAPPING = {
    'center': DefaultRobotPathFollowScript,
    'path': DefaultRobotPathFollowScript
}

class EnemySystem(object):
    """ This is the enemy service which is bound to the server level """

    def __init__(self, server_level, tiled_enemies, sim_buf_queue):
        self.server_level = server_level
        self.tiled_enemies = tiled_enemies

        self.all_robots = {}
        self.robot_scripts = []

        self.current_robot_new_id = 0

        self.simulation_step_buffer_queue = sim_buf_queue
        self.simulation_step_buffer_queue.register(EnemySystemQueueConstants.MOVING_ENEMIES)
        self.simulation_step_buffer_queue.register(EnemySystemQueueConstants.ATTACKING_ENEMIES)
        self.simulation_step_buffer_queue.register(EnemySystemQueueConstants.CHANGED_ENEMIES)

    def get_new_robot_id(self):
        self.current_robot_new_id += 1
        return self.current_robot_new_id

    def initialize_enemies(self):

        for tiled_enemy in self.tiled_enemies:
            pathway_list = tiled_enemy.get_pathway_list()
            robot_type = tiled_enemy.get_robot_type()
            robot_count = tiled_enemy.get_robot_count()
            robot_script_key = tiled_enemy.get_robot_script_key()

            list_of_robots = self.create_robots(robot_type, robot_count)

            assert robot_script_key in ROBOT_SCRIPT_MAPPING

            robot_script = ROBOT_SCRIPT_MAPPING[robot_script_key](self.server_level, self.simulation_step_buffer_queue,
                                                                  pathway_list, list_of_robots)
            robot_script.initialize()

            self.robot_scripts.append(robot_script)

    def perform_robot_scripting(self):
        for script in self.robot_scripts:
            script.perform()

    def get_enemy_system_buffer_queue(self):
        return self.simulation_step_buffer_queue

    def get_enemies_that_changed(self):
        return self.simulation_step_buffer_queue.get_queue_content(EnemySystemQueueConstants.CHANGED_ENEMIES)

    def remove_destroyed_enemies(self):
        dead_enemies = [z for z in self.all_robots.values() if z.is_marked_destroyed()]
        alive_enemies = [z for z in self.all_robots.values() if not z.is_marked_destroyed()]
        self.all_robots = {z.get_id(): z for z in alive_enemies}
        return dead_enemies

    def get_all_enemies(self):
        return self.all_robots.values()

    def create_robots(self, robot_type, robot_count):
        list_of_robots = []

        for i in range(robot_count):
            robot_id = self.get_new_robot_id()

            # Currently we just support one robot
            if robot_type == 1:
                robot = RoboticVacuumCleaner(robot_id, (0, -10, -10))
                self.all_robots[robot_id] = robot
                list_of_robots.append(robot)

        return list_of_robots