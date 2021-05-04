class TagInfo:
    def __init__(self):
        self.__tag_info = {}
        self.__is_pressed = False


    @property
    def tag_description(self):
        return self.__tag_info

    @tag_description.setter
    def tag_description(self, tag_info_dict: dict):
        self.__tag_info = tag_info_dict

    @property
    def pressed_state(self):
        return self.__is_pressed
    
    @pressed_state.setter
    def pressed_state(self, yes_no: bool):
        if yes_no not in [True, False]:
            raise Exception('Setter value must be True or False')
        else:
            self.__is_pressed = yes_no
