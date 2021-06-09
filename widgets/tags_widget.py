from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from db_files.db_cursor import DBCursor
from windows.records.tag_window import TagWindow
from windows.utility.message_boxes import YesNoWindow, InfoBox
from widgets.tag_info import TagInfo


class TagWidget(QWidget):

    signal_edit_tag = pyqtSignal(str, str, int)
    signal_add_tag = pyqtSignal(str, int)
    signal_delete_tag = pyqtSignal(str)
    signal_unselect_tag = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TagWidget, self).__init__()

        self.db_cursor = DBCursor.getInstance()
        self.edit_section_mode = False
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.__tags = dict()
        self.init_available_tags()

        self.__new_tag_button()
        self.change_geometry()

    @property
    def tags(self):
        return self.__tags

    @property
    def tag_amount(self):
        return len(self.db_cursor.get_tag_and_colour)

    @tags.setter
    def tags(self, tag_tuple):
        self.__tags[tag_tuple[0]] = tag_tuple[-1]

    @classmethod
    def check_tags(cls, tags, colours, login_name=None):
        db_cursor = DBCursor.getInstance()
        login_tags = db_cursor.get_tags_by_login_name(login_name)
        print(login_tags)
        exist_tags = db_cursor.get_tag_names
        tags_list = []
        for i in exist_tags:
            tags_list.append(i[0])
        if tags[0] == 0:
            if login_name != None:
                db_cursor.delete_login_from_intermediate(login_name)
        else:
            for i in tags:
                colour = colours[tags.index(i)]
                colour_id = db_cursor.get_colour_by_name(colour)
                
                colour_id = colour_id[0][0]
                print(colour, colour_id)
                if i in tags_list:
                    db_cursor.edit_tag(i, i, colour_id)
                elif i not in tags_list:
                    db_cursor.add_new_tag(i, colour_id)

    def set_edit_section_mode(self):
        self.edit_section_mode = True

    def init_available_tags(self, edit_tag=False):
        if not edit_tag:
            tag_name_and_colour = self.db_cursor.get_tag_and_colour

            for i in tag_name_and_colour:
                temp_tag_info = TagInfo()
                temp_tag_info.tag_description = {'colour': i[-1]}
                self.tags = (i[0], temp_tag_info)
        else:
            for i in edit_tag:
                temp_tag_info = TagInfo()
                temp_tag_info.tag_description = {'colour': i[-1]}
                self.tags = (i[0], temp_tag_info)

    def reinit_tags(self):
        self.__tags = dict()
        self.init_available_tags()

    def __new_tag_button(self):
        self.custom_tag_button = QPushButton(self)
        self.custom_tag_button.setText('+')
        button_style = """border-radius: 8px; color: black; text-align: center;
                            font-size: 16px; border: 2px solid black;"""
        self.custom_tag_button.setStyleSheet(button_style)
        self.custom_tag_button.clicked.connect(self.new_custom_tag)

    def change_geometry(self, height=None, width=None):
        tags_amount = self.tag_amount
        height_coefficient = 15
        if tags_amount % 2:
            height = height_coefficient*tags_amount + 100
        else:
            height = (height_coefficient + 5)*tags_amount + 100
        self.setFixedHeight(height)

    def paintEvent(self, e):
        painter = QPainter(self)
        self.change_geometry()

        text_font = painter.font()
        text_font.setPixelSize(18)
        painter.setFont(text_font)
        check_tags, noncheck_tags = {}, {}
        tags_dict = self.tags
        for tag_name, tag_info in tags_dict.items():
            if tag_info.pressed_state:
                check_tags[tag_name] = tag_info
            else:
                noncheck_tags[tag_name] = tag_info
        check_tags.update(noncheck_tags)
        font_metrics = QFontMetrics(text_font)
        all_text_width = 0
        start_x = 30
        x_pos, y_pos, abscissa_shift = start_x, 70, 35

        for tag_name, tag_info in check_tags.items():
            tag_text = tag_name
            tag_width, tag_height = font_metrics.width(tag_text), font_metrics.height()

            color, tag_colour = QColor(), tag_info.tag_description['colour']
            color.setNamedColor(tag_colour)

            pen, pen_width = QPen(), 2
            pen.setColor(color)
            pen.setWidth(pen_width)
            painter.setPen(pen)

            rect = QRect(QPoint(x_pos, y_pos - tag_height),QSize(tag_width, tag_height + 5))
            if tag_info.pressed_state:
                painter.fillRect(x_pos, y_pos-tag_height, tag_width, tag_height+5, color)
                painter.setPen(Qt.black)
                painter.drawText(x_pos, y_pos, tag_text)
            else:
                painter.drawRect(rect)
                painter.setPen(Qt.black)
                painter.drawText(x_pos, y_pos, tag_text)
            tag_info.tag_description = {
                                        'colour': tag_colour,
                                        'rect': rect,
                                        'rect_param': [x_pos, y_pos-tag_height, tag_width, tag_width]
                                    }
            all_text_width += tag_width
            if (all_text_width + self.width()/2 + 20) > self.width():
                x_pos = start_x
                y_pos += tag_height + 40
                all_text_width = 0
            else:
                x_pos += tag_width + abscissa_shift
                temp_point = QPoint(x_pos, y_pos-tag_height)
                temp_rect = QRect(temp_point, QSize(tag_width,tag_height+5))
                if temp_rect.contains(x_pos-tag_width-40, y_pos):
                    x_pos += tag_width + abscissa_shift + 100

        self.set_pos_for_tag_butn()
        self.adjustSize()
        painter.end()

    def mouseReleaseEvent(self, QMouseEvent):
        self.x_pos, self.y_pos = QMouseEvent.x(), QMouseEvent.y()
        temp = self.is_pressed_tag(self.x_pos, self.y_pos)

        if temp.get('no_tag'):
            return

        tag_name = temp['tag_name']
        if temp['answer'] and QMouseEvent.button() == Qt.RightButton:
            self.edit_press_tag = temp
            self.clicked_name = tag_name
            self.contextMenuEvent(QMouseEvent)
            return
        elif temp['answer'] and QMouseEvent.button() == Qt.LeftButton:
            if not self.tags[tag_name].pressed_state:
                self.tags[tag_name].pressed_state = True
                self.repaint()
            else:
                if self.edit_section_mode:
                    return
                else:
                    self.tags[tag_name].pressed_state = False
                    self.repaint()

    def contextMenuEvent(self, event):
        x_pos, y_pos = event.x(), event.y()

        self.edit_menu = QMenu()
        edit_action = self.edit_menu.addAction('Edit Tag')
        delete_action = self.edit_menu.addAction('Delete Tag')
        unselect_action = int()
        if self.edit_section_mode:
            unselect_action = self.edit_menu.addAction('Unselect Tag')
        self.edit_menu.setGeometry(x_pos, y_pos, 60, 60)
        self.edit_menu.show()
        action = self.edit_menu.exec_(self.mapToGlobal(event.pos()))

        tag_name = self.edit_press_tag['tag_name']

        if action == edit_action:
            tag_info = self.edit_press_tag['tag_info']

            self.edit_tag(tag_name, tag_info.tag_description['colour'])
            self.tags[tag_name].pressed_state = True
            self.repaint()
        if action == delete_action:
            self.delete_current_tag()

        if action == unselect_action:
            self.signal_unselect_tag.emit(tag_name)
            self.tags[tag_name].pressed_state = False
            self.repaint()

    def is_pressed_tag(self, x_current, y_current):
        for tag_name, tag_info in self.tags.items():
            if tag_info.tag_description['rect'].contains(x_current, y_current):
                return {'answer': True,
                        'tag_name': tag_name,
                        'tag_info': tag_info}
        return {'no_tag': True}

    def edit_tag(self, tag_name, colour):
        self.edit_window = TagWindow()
        self.clicked_name = tag_name
        self.colour_id = (self.db_cursor.get_colour_by_name(colour))[0][0]
        self.edit_window.edit_mode([tag_name, self.colour_id-1])

        self.edit_window.edit_tag_signal.connect(self.update_tag)
        self.edit_window.show()

    def update_tag(self, new_name, new_colour):
        new_colour_name = self.db_cursor.get_colour_by_id(new_colour)[0][0]
        if new_name == self.clicked_name:
            temp = self.tags[self.clicked_name].tag_description['colour']
            if new_colour_name == temp:
                self.edit_window.close()
            else:
                self.tags[self.clicked_name].tag_description['colour'] = new_colour_name
                self.edit_signal(new_colour=new_colour)
                self.repaint()
                self.edit_window.close()
        elif self.is_unique_tag(self.edit_window, new_name):
            temp_tag_info = self.tags.get(self.clicked_name)
            temp_tag_info.tag_description['colour'] = new_colour_name
            self.tags.setdefault(new_name, temp_tag_info)
            self.edit_signal(new_name=new_name, new_colour=new_colour)
            self.tags.pop(self.clicked_name)
            self.tags[new_name].pressed_state = True

            self.change_geometry()
            self.repaint()
            self.edit_window.close()

    def edit_signal(self, new_name=None, new_colour=None):
        temp_name = self.tags[self.clicked_name].tag_description['colour']
        old_id = self.db_cursor.get_colour_by_name(temp_name)[0][0]
        if new_colour:
            self.signal_edit_tag.emit(self.clicked_name, self.clicked_name, new_colour)
        if new_name:
            self.signal_edit_tag.emit(self.clicked_name, new_name, old_id)
        if new_name and new_colour:
            self.signal_edit_tag.emit(self.clicked_name, new_name, new_colour)

    def is_unique_tag(self, my_parent, tag_name):
        if tag_name in list(self.tags.keys()):
            InfoBox(my_parent, 'Such tag already exist')
            return False
        else:
            return True

    def delete_current_tag(self):
        if len(self.db_cursor.get_intermediate_tag_id(self.clicked_name)) > 0:
            message = "You can not remove this tag"
            InfoBox(self, window_name='Info', message=message)
            self.tags[self.clicked_name].pressed_state = False
        else:
            is_delete = YesNoWindow(self, 'Really delete this tag?')
            answer = is_delete.yes_no()
            if answer:
                self.signal_delete_tag.emit(self.clicked_name)
                self.tags.pop(self.clicked_name)
                self.repaint()
            else:
                return

    def new_custom_tag(self):
        self.tag_window = TagWindow()
        self.tag_window.add_tag_signal.connect(self.init_new_tag)
        self.tag_window.setModal(True)
        self.tag_window.show()

    def init_new_tag(self, tag_name, selected_colour):
        colour_name = (self.db_cursor.get_colour_by_id(selected_colour))[0][0]
        if self.is_unique_tag(self.tag_window, tag_name):
            temp_tag_info = TagInfo()
            temp_tag_info.pressed_state = True
            temp_tag_info.tag_description = {'colour': colour_name}
            self.tags = (tag_name, temp_tag_info)
            self.change_geometry()
            self.signal_add_tag.emit(tag_name, selected_colour)
            self.repaint()
            self.tag_window.close()

    @property
    def pressed_tags(self):
        pressed_tags_list = []
        for tag_name, tag_info in self.tags.items():
            if tag_info.pressed_state:
                pressed_tags_list.append(tag_name)
        return pressed_tags_list

    def set_pos_for_tag_butn(self):
        x_pos = int(self.width()/2) - int(self.width()/10)
        y_pos, button_w, button_h = 0, 50, 30
        self.custom_tag_button.setGeometry(x_pos, y_pos, button_w, button_h)
