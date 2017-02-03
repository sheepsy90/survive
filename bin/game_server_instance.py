""" This is a game serve r instance which handles one area to be computed """
import logging
import socket
import threading
import sys

from client.network.ClientToServerNetworkCommands import ClientInteractsForWearingItem, \
    ClientSendsFinishedDescriptionOfCraftingResult
from common.constants.ClientPackagePrefixes import ClientPackagePrefixes
from common.constants.ContainerConstants import ContainerConstants
from common.constants.ServerToClientNetworkCommands import NewConnectionMessage
from common.helper import send_message, determine_package_length
from server.api.ItemSpawnSystem import ItemSpawnSystem
from server.client_command_dispatcher.ClientCommandDispatcher import ClientCommandDispatcher
from server.constants.constans import EnemySystemQueueConstants
from server.health_modifier.DamageFromEnemiesModifier import ShockedDamageModifier
from server.health_modifier.SpecifiedModifiers import *
from server.local_services.AtmosphericSystem import AtmosphericSystem
from server.local_services.EnemySystem import EnemySystem
from server.local_services.GameLogicSimulationMethods import GameLogicSimulationMethods
from server.local_services.OnlinePlayerLoader import OnlinePlayerLoader
from server.local_services.OnlinePlayerSystem import OnlinePlayerSystem
from server.local_services.SimulationStepObjectBufferQueueSystem import SimulationStepBufferQueueSystem, \
    SimulationStepBufferQueue
from server.local_services.BulletSystem import BulletSystem
from server.local_services.CombatSystem import CombatSystem
from server.local_services.ContainerOpenedService import ContainerOpenedMemorizeService
from server.network.ConnectionHandler import ConnectionHandler
from server.network.ServerCommandWrapper import ServerCommandWrapper
from server.setup.AreaService import AreaService
from server.world_objects.object_components.ContainerComponent import Container
from server.xmlrpc_services.crafting.CraftingServiceClient import CraftingServiceClient
from server.xmlrpc_services.gameservermanager.GameServerManagerClient import GameServerManagerClient
from server.xmlrpc_services.item_list_entry_logger.ItemListEntryLoggerClient import ItemListEntryLoggerClient
from server.xmlrpc_services.items.ItemServiceClient import ItemServiceClient
from server.xmlrpc_services.player.PlayerHandlerServiceClient import PlayerHandlerServiceClient


logger = logging.getLogger(__name__)


class TutorialFlowHandler(object):

    def __init__(self, area_id):
        self.tutorial_server = area_id == 3
        self.handles_player = False

    def is_tutorial_server(self):
        return self.tutorial_server

    def activate(self):
        self.handles_player = True

    def check(self):
        """ This method is called when there is no player connected -
            if we handled a player we need to reset the instance """
        return self.handles_player


class Server(threading.Thread):

    def __init__(self, area_id, udp_ip, udp_port):
        threading.Thread.__init__(self)
        self.daemon = True
        self.reset = False

        self.tutorial_flow_handler = TutorialFlowHandler(area_id)

        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.area_to_serve = area_to_serve

        logging.basicConfig(format='[%(levelname)s] [%(name)s] %(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='logs/game_server_log_%(port)s_%(area)s.log' % {
                                "port": str(udp_port),
                                "area": str(area_to_serve)},
                            level=logging.INFO)

        # Get all the necessary service clients
        self.game_server_manager_client = GameServerManagerClient()
        self.players_service_client = PlayerHandlerServiceClient()
        self.item_list_entry_logger_client = ItemListEntryLoggerClient()
        self.crafting_service_client = CraftingServiceClient()
        self.item_service_client = ItemServiceClient()

        self.item_spawn_service = ItemSpawnSystem(self.item_service_client, self.crafting_service_client)

        # First get the area to simulate
        self.server_level = AreaService().get_area_specifications(self.area_to_serve)

        self.simulation_step_buffer_queue_system = SimulationStepBufferQueueSystem()
        self.simulation_step_buffer_queue_system.register(SimulationStepBufferQueue.PLAYER_LEFT_AREA)
        self.simulation_step_buffer_queue_system.register(SimulationStepBufferQueue.PLAYER_UPDATE)
        self.simulation_step_buffer_queue_system.register(SimulationStepBufferQueue.WORLD_OBJECTS_CHANGED)
        self.simulation_step_buffer_queue_system.register(SimulationStepBufferQueue.WORLD_OBJECTS_DELETED)

        self.server_level.prepare(self.simulation_step_buffer_queue_system)

        # Get the Enemy Handler
        self.enemy_system = self.server_level.get_enemy_system()

        # The bullet system for moving parts
        self.bullet_system = BulletSystem()
        self.combat_system = CombatSystem(self.server_level, self.bullet_system)

        # A Memorizer for Open containers
        self.container_state_mem_system = ContainerOpenedMemorizeService()

        # Create a locale service to handle online players
        self.online_player_system = OnlinePlayerSystem()

        # Create a WeatherService
        atmospheric_temperature, atmospheric_type = self.server_level.get_atmospheric_data()
        self.atmospheric_system = AtmosphericSystem(atmospheric_temperature, atmospheric_type)
        self.start_time = time.time()

        # A Locale Handler for Connections
        self.connection_handler = ConnectionHandler()

        # The UDP Socket we use to accept incoming things and send things over
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.udp_ip, self.udp_port))

        # Create Wrapper that encapsulates the commands that the server can send to the client
        self.server_command_wrapper = ServerCommandWrapper(self.sock)

        self.online_player_loader = OnlinePlayerLoader(area_id,
                                                       self.connection_handler,
                                                       self.server_command_wrapper,
                                                       self.players_service_client,
                                                       self.crafting_service_client,
                                                       self.item_service_client,
                                                       self.online_player_system,
                                                       self.container_state_mem_system)

        self.game_logic_simulation_methods = GameLogicSimulationMethods(self.server_command_wrapper,
                                                                        self.simulation_step_buffer_queue_system,
                                                                        self.server_level,
                                                                        self.item_service_client,
                                                                        self.atmospheric_system)

        # Register at the game_server_instance
        self.game_server_manager_client.register_game_service(self.tutorial_flow_handler.is_tutorial_server(),
                                                              self.area_to_serve,
                                                              self.udp_ip,
                                                              self.udp_port)
        self.gsm_last_notified = time.time()
        logger.info("Registered at GameServerManager")

        self.print_details()

    def print_details(self):
        print "#################################################################################"
        print
        print "Server On {}:{}".format(self.udp_ip, self.udp_port)
        print "Serving Area: {}".format(self.area_to_serve)
        print
        print "#################################################################################"

    def listen(self):
        while not self.reset:
            # Read at most 1024 bytes per package
            # Currently there are 2bytes + max(255) bytes in each package
            self.sock.settimeout(5.0)
            try:

                # Contact the game Server Manager to tell him we are still there
                if time.time() - self.gsm_last_notified > 5:
                    self.gsm_last_notified = time.time()
                    self.game_server_manager_client.ping(self.tutorial_flow_handler.is_tutorial_server(),
                                                         self.area_to_serve,
                                                         self.udp_ip,
                                                         self.udp_port)

                # Blocking Read with timeout
                data, addr = self.sock.recvfrom(1024)

                # First check if there is already a connection and if so dispatch the command
                if self.connection_handler.has_connection(addr):
                    conn = self.connection_handler.get_connection(addr)
                    self.dispatch_client_command(conn, data)
                else:
                    # Create a new player if there is no one registered under that addr key
                    if not self.online_player_loader.create_new_player(addr, data):
                        logger.error("Player Creation failed!")
            except socket.timeout:
                logger.info("Socket UPD Timeout to check if we are still running!")
            except Exception as e:
                print e

        logger.info("Listen Loop finished!")

    def handle_enemy_death_spawns_stuff(self):
        # Enemies that need to be updated within the client

        destroyed_enemies = self.enemy_system.remove_destroyed_enemies()
        for destroyed_enemy in destroyed_enemies:
            d, x, y = destroyed_enemy.get_moving_component().get_discrete_position()
            wo = self.server_level.get_world_object_manager().create_world_object(x, y)
            c = Container(refreshable=True, shape=(5, 5), container_type=ContainerConstants.CONTAINER_TYPE_NORMAL,
                          searchable_type="lunch_package", read_only=True, vanish_on_empty=True)
            wo.add_component(c)
            self.server_level.get_world_object_manager().add_components_to_cache(wo.get_object_id())
            self.simulation_step_buffer_queue_system.push(SimulationStepBufferQueue.WORLD_OBJECTS_CHANGED, wo)



    def perform_general_simulation(self, all_players):
        """ This method is called as the core routine handling all steps necessary during one simulation step
            of the game system.
        :param all_players:
        :param player_updates_for_all:
        :param special_updates_for_all:
        :return:
        """

        player_sim_step_update_queue = \
            self.simulation_step_buffer_queue_system.get_queue(SimulationStepBufferQueue.PLAYER_UPDATE)

        # Update Moving
        moving_players = self.online_player_system.moving_players.values()
        for mplayer in moving_players:
            # First of all - all players that are moving need to put into update queue
            player_sim_step_update_queue.push(mplayer)

            if mplayer.get_moving_component().is_moving_finished():
                # Send it anyway but remove the player from the moving list
                self.online_player_system.remove_moving_player(mplayer.get_id())

                d, x, y = mplayer.get_moving_component().get_discrete_position()
                if self.server_level.is_change_area_spot(x, y):
                    if self.change_area_with_player(mplayer):
                        self.simulation_step_buffer_queue_system.push(SimulationStepBufferQueue.PLAYER_LEFT_AREA, mplayer)

        # Update the Bullet Physics and send current bullet positions to players
        self.bullet_system.calculate_all_bullet_positions()
        self.server_command_wrapper.update_bullet_positions_for_all_players(self.sock,
                                                                            self.bullet_system.get_bullets(),
                                                                            all_players)

        # Move all the enemy robots
        self.enemy_system.perform_robot_scripting()

        # This method iterates over positions of bullets and enemies and calculate the effect of the
        # bullets on the enemies
        self.combat_system.handle(all_players, self.enemy_system.get_all_enemies())
        # Get all bullets which are marked as hit and send that info to all players
        # Then remove all those bullets from the bullet system
        bullets_marked_destroyed = self.bullet_system.get_bullets_marked_destroyed()
        self.server_command_wrapper.send_destroyed_bullets_to_all_players(bullets_marked_destroyed,
                                                                          all_players)
        self.bullet_system.remove_destroyed_bullets()

        enemy_which_attack = self.enemy_system.get_enemy_system_buffer_queue().get_queue_content(EnemySystemQueueConstants.ATTACKING_ENEMIES)
        self.server_command_wrapper.send_enemies_start_attacking(enemy_which_attack, all_players)

        for player in all_players:
            for enemy in enemy_which_attack:

                pd, px, py = player.get_moving_component().get_position_based_on_movement()
                ed, ex, ey = enemy.get_moving_component().get_position_based_on_movement()

                dx = abs(px - ex)
                dy = abs(py - ey)

                if dx <= 2 and dy <= 2:
                    hmc = player.get_health_modifier_component()
                    hmc.add_status_modifier_to_queue(StatusModifierQueueElement(
                    ShockedDamageModifier(), 0))

        self.handle_enemy_death_spawns_stuff()

        # This method handles the stepable updates
        #self.update_steppable_components(all_players)

        # this method calculates all the necessary health modifier stuff and notifies the players
        self.game_logic_simulation_methods.update_health_modifier(all_players)

        self.game_logic_simulation_methods.handle_script_schedule()

        # Check which players need to be disconnected due to to much TTL Delay
        for player in all_players:
            # TODO This needs just to be performed each 5 seconds
            if player.get_connection().get_time_since_last_ttl() > 15:
                logger.info("Removing player %s due to too much delay in TTL" % str(player))
                player.mark_disconnecting()

        # This method checks which item properties have changed/ which are deleted and sends packages for
        # updating the specific client.
        self.game_logic_simulation_methods.update_items_for_client(all_players)

        # This is the method call for making sure that all BufferStepQueues are worked
        self.game_logic_simulation_methods.consume_simulation_step_buffer_queue_system(all_players)

        # Iterate over all players and remove the connection from the system so he
        # absolutely vanishes from this game_instance
        for player in all_players:
            if player.is_disconnecting():
                self.remove_player_from_server(player)

    def handle_player_command_queue(self, client_command_dispatcher, all_players):
        """ This is the main method which processes all the commands that where given by the players
        :param client_command_dispatcher:
        :param all_players:
        :param player_updates_for_all:
        :return:
        """

        # Get the player update queue so it can be used
        player_sim_step_update_queue = \
            self.simulation_step_buffer_queue_system.get_queue(SimulationStepBufferQueue.PLAYER_UPDATE)

        world_object_deletion_update_queue = \
            self.simulation_step_buffer_queue_system.get_queue(SimulationStepBufferQueue.WORLD_OBJECTS_DELETED)

        for player in all_players:
            # Persist the player if necessary
            if player.get_persistable_component().needs_persistence():
                self.persist_player_state(player)
                player.get_persistable_component().touch_last_time_persisted()

            # Work on all commands
            while player.has_open_command():
                # Iterate over all open commands and perform them
                comm, info = player.get_open_commands()

                # Check that the command which comes from the client is valid and element of this list
                if comm not in [OnlinePlayerLoader.FULL_DATA_PROPAGATION,
                                    # TODO - Make sure that can't be requested by the client at will
                                ClientPackagePrefixes.CLIENT_WANTS_TO_MOVE,
                                ClientPackagePrefixes.CLIENT_SENDS_TTL,
                                ClientPackagePrefixes.CLIENT_WANTS_CLOSE_CONTAINER,
                                ClientPackagePrefixes.CLIENT_WANTS_OPEN_CONTAINER,
                                ClientPackagePrefixes.CLIENT_WANTS_TO_MOVE_ITEM,
                                ClientPackagePrefixes.CLIENT_WANTS_TO_CRAFT,
                                ClientPackagePrefixes.CLIENT_SENDS_FINISHED_DESCRIPTION,
                                ClientPackagePrefixes.CLIENT_WANTS_TO_WEAR_ITEM,
                                ClientPackagePrefixes.CLIENT_WANTS_TO_USE]:
                    # Reject the client due to invalid behaviour
                    logger.error("Client %s send command %s which was not allowed to come from the client"
                                 % (str(player), comm))
                    continue

                # TimeToLive package to notify the server that the client is still there
                if comm == ClientPackagePrefixes.CLIENT_SENDS_TTL:
                    player.get_connection().update_last_interaction()
                    continue

                # FullDataPropagation means that the client of this player needs a refresh of the world
                if comm == OnlinePlayerLoader.FULL_DATA_PROPAGATION:
                    client_command_dispatcher.handle_full_data_propagation_to_client(all_players,
                                                                                     self.server_level,
                                                                                     player,
                                                                                     self.enemy_system,
                                                                                     self.atmospheric_system,
                                                                                     player_sim_step_update_queue)
                    continue

                # Movement command issued by a client to move the character
                if comm == ClientPackagePrefixes.CLIENT_WANTS_TO_MOVE:
                    client_command_dispatcher.handle_player_movement(self.server_level, self.online_player_system,
                                                                     player, self.container_state_mem_system, info)
                    continue

                # An open container command
                if comm == ClientPackagePrefixes.CLIENT_WANTS_OPEN_CONTAINER:
                    client_command_dispatcher.handle_client_wants_to_open_a_container(info, player,
                                                                                      self.container_state_mem_system,
                                                                                      self.server_level,
                                                                                      self.item_spawn_service)
                    continue

                # A close container command
                if comm == ClientPackagePrefixes.CLIENT_WANTS_CLOSE_CONTAINER:
                    client_command_dispatcher.handle_client_wants_to_close_a_container(info,
                                                                                       self.container_state_mem_system,
                                                                                       player,
                                                                                       self.server_level,
                                                                                       world_object_deletion_update_queue)
                    continue

                if comm == ClientPackagePrefixes.CLIENT_WANTS_TO_MOVE_ITEM:
                    client_command_dispatcher.handle_client_wants_to_move_item(info, player,
                                                                               self.container_state_mem_system)
                    continue

                if comm == ClientPackagePrefixes.CLIENT_WANTS_TO_USE:
                    """ This is the command where the player can use items that hey have in their hands """
                    client_command_dispatcher.handle_client_wants_to_use(self.bullet_system, player, self.server_level)
                    continue

                if comm == ClientPackagePrefixes.CLIENT_WANTS_TO_CRAFT:
                    client_command_dispatcher.handle_client_wants_to_craft(player,
                                                                           self.container_state_mem_system,
                                                                           self.crafting_service_client,
                                                                           self.item_service_client)
                    continue

                if comm == ClientInteractsForWearingItem.prefix():
                    client_command_dispatcher.handle_client_interacts_for_wearing_item(info, player,
                                                                                       self.container_state_mem_system)
                    continue

                if comm == ClientSendsFinishedDescriptionOfCraftingResult.prefix():
                    item_type, text = ClientSendsFinishedDescriptionOfCraftingResult.from_string(info)
                    self.item_list_entry_logger_client.log_crafting_result(player.get_id(), item_type, text)
                    continue

    def run(self):
        """ Main Game Loop which handles the player commands and the simulation steps """
        client_command_dispatcher = ClientCommandDispatcher(self.server_command_wrapper)

        while not self.reset:
            # Get all players
            all_players = self.online_player_system.online_players.values()

            # If there are no players freeze don't do anything
            if len(all_players) == 0:
                time.sleep(0.2)
                logger.info("No players connected - check reset condition!")
                if self.tutorial_flow_handler.is_tutorial_server() and self.tutorial_flow_handler.check():
                    # If this returns true we need to reset the instance
                    logger.info("Reset necessary!")
                    self.reset = True
                continue
            else:
                if self.tutorial_flow_handler.is_tutorial_server():
                    self.tutorial_flow_handler.activate()

            self.handle_player_command_queue(client_command_dispatcher, all_players)
            self.perform_general_simulation(all_players)

            if self.tutorial_flow_handler.is_tutorial_server():
                for player in all_players:
                    value = player.is_finished_tutorial()
                    if value is not None:
                        if time.time() - value > 12:
                            self.change_area_with_player_with_values(player, 1, (1, 29, 39))
                        else:
                            self.players_service_client.save_tutorial_state(player.get_character_id(), 0)


            # TODO Write the code necessary for constant FPS
            time.sleep(0.025)

        logger.info("Main Game Loop finished!")


    def dispatch_client_command(self, conn, data):
        """ This method does the client command dispatch.
            Each command coming from the client is broken down to the instruction code and
            the payload which is then put into the player objects queue from where it is taken
            and processed in the main game loop """

        # First determine the package length
        package_length_bytes = data[0:2]
        package_length = determine_package_length(package_length_bytes)

        # Extract the complete data
        data = data[2:package_length+2]

        # The first three chars are the command the rest is payload
        command, information = data[0:3], data[3:]

        # Put the command to the player queue
        player = self.online_player_system.get_player_on_connection(conn)
        player.add_command(command, information)

    def change_area_with_player_with_values(self, player, new_area_id, start_position):
        # Inform the players XMLRPCService about the change

        still_tutorial_int = player.is_player_still_tutorial()

        # Get the necessary information for that area
        new_game_server_instance = self.game_server_manager_client.get_game_service_for_area(still_tutorial_int, new_area_id)

        if new_game_server_instance is None:
            logger.warn("Player {} walked on AreaChangeSpot but the area {} was not available"
                        .format(player, new_area_id))
            return False

        self.players_service_client.set_character_to_new_area(player.get_account_id(),
                                                                     player.get_character_id(),
                                                                     new_area_id, start_position)

        # Build a package for the client to notify him which instance shall handle him now
        message = NewConnectionMessage.build_package(still_tutorial_int,
                                                     new_game_server_instance[0], new_game_server_instance[1])
        send_message(self.sock, message, player.get_connection().addr)

        # Mark the player for deletion after the complete game loop so that he doesn't stay connected here
        player.mark_disconnecting()
        return True

    def change_area_with_player(self, player):
        """ This method is called when the player enters a change area spot on the map
            calling the game server manager and asking for the game_server_instance which
            handles that particular area """

        # Get the player position and the new area id and the start position there
        direction, posx, posy = player.get_moving_component().get_discrete_position()
        area_change_spot = self.server_level.get_change_area(posx, posy)

        new_area_id = area_change_spot.get_target_level_id()
        start_position = area_change_spot.get_target_position()

        return self.change_area_with_player_with_values(player, new_area_id, start_position)

    def persist_player_state(self, player):
        """ This method should be called whenever the client is losing connection,
            explicitly disconnects and from time to time for players if they exceed a certain
            time limit so that they are persisted if something happens """
        account_id = player.get_account_id()
        character_id = player.get_character_id()
        discrete_position = player.get_moving_component().get_discrete_position()

        inventory_container = player.get_inventory()

        health_modifier = player.get_health_modifier_component()
        modifier_dict = health_modifier.get_modifiers()
        currently_worn_items = player.get_character_wearing_handler().get_worn_items_ids_as_list()

        self.players_service_client.save_player_position(account_id, character_id, discrete_position)
        self.players_service_client.save_backpack_content(character_id, inventory_container.content, inventory_container.item_root_positions)
        self.players_service_client.save_wearing_states(character_id, currently_worn_items)
        self.players_service_client.save_health_modifiers(character_id, modifier_dict)

        logger.info("Persisted player {}".format(str(player)))

    def remove_player_from_server(self, player):
        logger.info("Removed player from server {}".format(str(player)))
        self.online_player_system.remove_player(player)
        self.connection_handler.del_connection(player.get_connection().addr)
        self.container_state_mem_system.remove_all_open_containers_for_player(player)
        del player


if __name__ == "__main__":

    assert len(sys.argv) == 4
    udp_ip = sys.argv[1]
    udp_port = int(sys.argv[2])
    area_to_serve = int(sys.argv[3])

    while True:
        # This restarts the server if necessary (like in a tutorial area case)
        s = Server(area_to_serve, udp_ip, udp_port)
        s.start()
        s.listen()
        time.sleep(1)