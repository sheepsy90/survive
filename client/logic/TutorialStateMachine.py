# -*- coding:utf-8 -*-

import uuid
from common.constants.ScriptingConstants import ScriptingConstants


class TutorialStateMachine(object):

    def __init__(self, voice_acting_engine, sound_engine, client_level_manager, marker_logic):
        self.voice_acting_engine = voice_acting_engine
        self.sound_engine = sound_engine
        self.client_level_manager = client_level_manager
        self.marker_logic = marker_logic

        self.current_state = self.wait_for_level_loading_complete_to_play_first_voice_over

        self.marker_a_id = uuid.uuid4()
        self.marker_b_id = uuid.uuid4()
        self.marker_c_id = uuid.uuid4()

    def wait_for_level_loading_complete_to_play_first_voice_over(self):
        """ Initial State - It waits for the Level Manager to get ready so we can play the first voice message """

        curr_level = self.client_level_manager.get_current_level()
        if curr_level is not None and curr_level.get_player_manager().has_me():
            self.voice_acting_engine.perform_voice_acting("tutorial_1")
            self.current_state = self.wait_for_tutorial_one_voice_to_finish
            self.marker_logic.add_marker_to_show(self.marker_a_id, "arrow", 22, 10)

    def wait_for_tutorial_one_voice_to_finish(self):
        """ Just wait until the voice over is over """
        if not self.voice_acting_engine.still_active("tutorial_1"):
            self.current_state = self.track_player_position_and_wait_until_he_reaches_cabinet_then_play_second_voice_acting

    def track_player_position_and_wait_until_he_reaches_cabinet_then_play_second_voice_acting(self):
        me = self.client_level_manager.get_current_level().get_player_manager().get_me()

        position = me.get_position()
        o, x, y = position

        if int(x) == 22 and int(y) == 11:
            self.voice_acting_engine.perform_voice_acting("tutorial_2")
            self.current_state = self.wait_for_second_voice_acting_finish
            self.marker_logic.delete_marker_to_show(self.marker_a_id)

    def wait_for_second_voice_acting_finish(self):
        if not self.voice_acting_engine.still_active("tutorial_2"):
            self.voice_acting_engine.perform_voice_acting("tutorial_3")
            self.current_state = self.wait_for_third_voice_acting_finish

    def wait_for_third_voice_acting_finish(self):
        if not self.voice_acting_engine.still_active("tutorial_3"):
            self.current_state = self.wait_for_player_to_wear_mask

    def wait_for_player_to_wear_mask(self):
        if self.client_level_manager.get_wearing_manager().is_wearing_mask():
            self.voice_acting_engine.perform_voice_acting("tutorial_4")
            self.current_state = self.wait_for_player_reaching_rescue_capsule
            self.marker_logic.add_marker_to_show(self.marker_b_id, "arrow", 37, 31)

    def wait_for_player_reaching_rescue_capsule(self):
        me = self.client_level_manager.get_current_level().get_player_manager().get_me()

        position = me.get_position()
        o, x, y = position

        if int(x) == 37 and int(y) == 33:
            self.voice_acting_engine.perform_voice_acting("tutorial_5")
            self.marker_logic.delete_marker_to_show(self.marker_b_id)
            self.current_state = self.wait_for_voice_tutorial_5_over

    def wait_for_voice_tutorial_5_over(self):
        if not self.voice_acting_engine.still_active("tutorial_5"):
            self.current_state = self.wait_for_player_to_use_object

    def wait_for_player_to_use_object(self):
        using_history = self.client_level_manager.get_using_history()

        if using_history.has_entry_in_history(ScriptingConstants.NOTHING_CHANGED):
            # That did not work. Something with the electronics. Maybe there is a replacement near the robot supply cabinet.
            self.voice_acting_engine.perform_voice_acting("tutorial_6")
            self.marker_logic.add_marker_to_show(self.marker_c_id, "arrow", 35, 8)
            self.current_state = self.wait_for_voice_tutorial_6_over

    def wait_for_voice_tutorial_6_over(self):
        if not self.voice_acting_engine.still_active("tutorial_6"):
            self.current_state = self.wait_for_player_reaching_electronics_cabinet

    def wait_for_player_reaching_electronics_cabinet(self):
        me = self.client_level_manager.get_current_level().get_player_manager().get_me()

        position = me.get_position()
        o, x, y = position

        if int(x) == 35 and int(y) == 9:
            # The electronics are in here - but i need to assemble them <c>.
            self.voice_acting_engine.perform_voice_acting("tutorial_7")
            self.marker_logic.delete_marker_to_show(self.marker_c_id)
            self.current_state = self.wait_for_voice_tutorial_7_over

    def wait_for_voice_tutorial_7_over(self):
        if not self.voice_acting_engine.still_active("tutorial_7"):
            self.current_state = self.wait_for_component_crafted

    def wait_for_component_crafted(self):
        item_watcher_dict = self.client_level_manager.get_general_item_watcher()

        for item in item_watcher_dict.values():
            if item.item_tid == 20:
                # Perfect. Now I take this in my hands <RMB> and use it with the capsule. That should do it.
                self.voice_acting_engine.perform_voice_acting("tutorial_8")
                self.current_state = self.wait_for_voice_tutorial_8_over
                return

    def wait_for_voice_tutorial_8_over(self):
        if not self.voice_acting_engine.still_active("tutorial_8"):
            self.current_state = self.wait_for_player_repaired_capsule

    def wait_for_player_repaired_capsule(self):
        using_history = self.client_level_manager.get_using_history()
        if using_history.has_entry_in_history(ScriptingConstants.REPAIRED):
            # The status tells me that it is back to normal. Now I can start it.
            self.voice_acting_engine.perform_voice_acting("tutorial_9")
            self.current_state = self.wait_for_player_use_capsule

    def wait_for_player_use_capsule(self):
        using_history = self.client_level_manager.get_using_history()
        if using_history.has_entry_in_history(ScriptingConstants.RESCUE_ACTIVATED):
            self.sound_engine.play("rescue_capsule_activated")
            self.current_state = self.finished
            self.marker_logic.delete_marker_to_show(self.marker_a_id)
            self.marker_logic.delete_marker_to_show(self.marker_b_id)
            self.marker_logic.delete_marker_to_show(self.marker_c_id)

    def finished(self):
        pass