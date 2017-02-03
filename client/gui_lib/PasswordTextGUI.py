from client.gui_lib.TextGUI import TextGUI


class PasswordTextGUI(TextGUI):

    def __init__(self, name, rect, maxlength=10, initial_value='', shadow_value=""):
        TextGUI.__init__(self, name, rect, maxlength, initial_value=initial_value, shadow_value=shadow_value)

    def determine_value(self):
        return ''.join(['*' for i in range(len(self.value))])


