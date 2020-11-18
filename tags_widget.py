from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from db_files.db_cursor import DBCursor
from tags_window import TagWindow
from message_boxes import YesNoWindow, InfoBox


class TagInfo:
    def __init__(self):
        self.tags_dict = {}
        self.is_pressed = False


    @property
    def tags_info(self):
        return (self.tags_dict, self.is_pressed)

    @property
    def is_checked(self):
        return self.is_pressed
    
    def change_main_key(self, old_key, new_key):
        temp_object = self.tags_dict.get(old_key)
        self.tags_dict.clear()
        self.tags_dict.setdefault(new_key, temp_object)

    @is_checked.setter
    def is_checked(self, yes):
        self.is_pressed = yes

    @tags_info.setter
    def tags_info(self, tag_info):
        self.tags_dict[tag_info[0]] = tag_info[-1]


class TagWidget(QWidget):

    signal_edit_tag = pyqtSignal(int, str, int)
    signal_add_tag = pyqtSignal(int, str, int)
    signal_delete_tag = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TagWidget, self).__init__()

        self.db_cursor = DBCursor.getInstance()
        self.tags_list = self.db_cursor.get_tag_and_colour
        self.timer_message = ""

        self.init_add_tag_buttom()
        self.tag_labels = [TagInfo() for i in range(len(self.tags_list))]
        self.change_geometry()

        
    def get_tag_label_by_name(self, name):
        for i in self.tag_labels:
            for k, v in i.tags_dict.items():
                if k == name:
                    return self.tag_labels.index(i)

    def init_add_tag_buttom(self):
        self.custom_tag_button = QPushButton(self)
        self.custom_tag_button.clicked.connect(self.new_custom_tag)

    def change_geometry(self, height=None, width=None):
        tags_amount = len(self.tags_list)
        height_coefficient = 35
        if tags_amount % 2:
            height = height_coefficient*tags_amount + 100
        else:
            height = (height_coefficient + 5)*tags_amount + 100
        self.setFixedHeight(height)

    def paintEvent(self, e):
        painter = QPainter(self)
        self.change_geometry()

        tags_amount = len(self.tags_list)
        font = painter.font()
        font.setPixelSize(18)
        self.font_metrics = QFontMetrics(font)
        text_width = 0
        x_pos, y_pos, x_shift = 10, 100, 50

        for i in range(tags_amount):
            tag_text = self.tags_list[i][0]
            tag_width, tag_height = self.font_metrics.width(tag_text), self.font_metrics.height()

            painter.setFont(font)

            color = QColor()
            pen = QPen()
            color.setNamedColor(self.tags_list[i][-1])
            pen.setColor(color)
            pen.setWidth(2)
            painter.setPen(pen)
            rect = QRect(QPoint(x_pos, y_pos-tag_height),QSize(tag_width,tag_height+5))
            if self.tag_labels[i].is_pressed:
                painter.fillRect(x_pos, y_pos-tag_height, tag_width, tag_height+5, color)
                painter.setPen(Qt.black)
                painter.drawText(x_pos, y_pos, tag_text)
            else:
                painter.drawRect(rect)
                painter.setPen(Qt.black)
                painter.drawText(x_pos, y_pos, tag_text)
            if 'rect' not in (self.tag_labels[i].tags_dict.keys()):
                self.init_new_tag_item(self.tag_labels[i], self.tags_list[i][0], self.tags_list[i][-1], 
                                        rect, x_pos, y_pos-tag_height, tag_width, tag_width)

            text_width += tag_width
            if (text_width + self.width()/2 + 5) > self.width():
                x_pos = 10
                y_pos += tag_height + 40
                text_width = 0
            else:
                x_pos += tag_width + x_shift
                temp_rect = QRect(QPoint(x_pos, y_pos-tag_height), QSize(tag_width,tag_height+5))
                if temp_rect.contains(x_pos-tag_width-40, y_pos):
                    x_pos += tag_width + x_shift + 100
                    
        self.new_tag_button()
        painter.end()

    def init_new_tag_item(self, element, tag_text, tag_colour, rect, x, y, h, w):
        temp_dict = {
                            'colour': tag_colour, 
                            'rect': rect,
                            'rect_param': [x, y, h, w]
                    }
        element.tags_info = [tag_text, temp_dict]


    def mousePressEvent(self, event):
        self.timer_last = "click"

    def mouseReleaseEvent(self, event):
        if self.timer_last == "click":
            self.x_pos, self.y_pos = event.x(), event.y()
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                self.__performSingleClickAction)
            temp = self.is_pressed_tag(self.x_pos, self.y_pos)
            if temp.get('no_tag'):
                return
            else:
                tag_index = temp['index']
                if temp['answer']:
                    if not self.tag_labels[tag_index].is_pressed:
                        self.tag_labels[tag_index].is_pressed = True
                        self.repaint()
                    else:
                        self.tag_labels[tag_index].is_pressed = False
                        self.repaint()
        else:
            self.timer_message = "Double Click"
            self.update()

    def __performSingleClickAction(self):
        if self.timer_last == "click":
            self.timer_message = "click"
            self.update()

    def is_pressed_tag(self, x_current, y_current):
        for index in range(len(self.tag_labels)):
            temp_dict = (self.tag_labels[index].tags_info)[0]
            for tag_name, tag_info in temp_dict.items():
                if tag_info['rect'].contains(x_current, y_current):
                    return {'answer': True, 'index': index, 
                            'tag_name': tag_name, 'tag_info': tag_info}
        return {'no_tag': True}

    def mouseDoubleClickEvent(self, event):
        self.timer_last = "Doble click"

        x_pos = event.x()
        y_pos = event.y()
        pressed_rect = self.is_pressed_tag(x_pos, y_pos)
        if pressed_rect.get('no_tag'):
            return
        else:
            tag_index = pressed_rect['index']
            tag_name = pressed_rect['tag_name']
            tag_info = pressed_rect['tag_info']

            if pressed_rect['answer']:
                self.old_tag_info(self.tag_labels[tag_index])
                self.edit_tag(tag_name, tag_info['colour'])
                self.tag_labels[tag_index].is_pressed = True
                self.repaint()

    def edit_tag(self, tag_name, colour):
        self.tag_edit_window = TagWindow()
        self.del_tag_name = tag_name
        self.colour_id = (self.db_cursor.get_colour_by_name(colour))[0][0]
        self.tag_edit_window.edit_mode([tag_name, self.colour_id-1])

        self.tag_edit_window.edit_tag_signal.connect(self.update_tag)
        self.tag_edit_window.delete_button.clicked.connect(self.delete_current_tag)

        self.tag_edit_window.show()

    def is_unique_tag(self, my_parent, tag_name):
        for i in self.tags_list:
            if i[0] == tag_name:
                InfoBox(my_parent, 'Such tag already exist')
                return False
        return True

    def edit_tag_item(self, tag_name, tag_colour, new_name=None, new_colour=None, edit=True):
        tag_index = self.tags_list.index((tag_name, tag_colour))
        
        if edit:
            self.tags_list[tag_index] = (new_name, (self.db_cursor.get_colour_by_id(new_colour))[0][0])
            self.change_geometry()
            self.tag_labels[tag_index].change_main_key(self.old_name, new_name)
        else:
            self.tags_list.pop(tag_index)
            self.tag_labels.pop(tag_index)

    def delete_current_tag(self):
        colour_name = (self.db_cursor.get_colour_by_id(self.colour_id))[0][0]
        tag_index = self.tags_list.index((self.del_tag_name, colour_name))
        if len(self.db_cursor.get_intermediate_tag_id(tag_index)) > 0:
            InfoBox(self, window_name='Info', message="You can not remove this tag")
            self.tag_labels[tag_index].is_pressed = False
            self.tag_edit_window.close()
        else:
            is_delete = YesNoWindow(self.tag_edit_window, 'Really delete this tag?')
            if is_delete.yes_no():
                self.signal_delete_tag.emit(tag_index)
                self.edit_tag_item(self.del_tag_name, colour_name, edit=False)
                self.tag_edit_window.close()
                self.repaint()
            else:
                return

    # signal functions
    def edit_signal(self, new_name=None, new_colour=None):
        tag_index = self.tag_labels.index(self.old_object) + 1
        old_colour_id = self.db_cursor.get_colour_by_name(self.old_colour)[0][0]
        if new_colour:
            self.signal_edit_tag.emit(tag_index, self.old_name, new_colour)
        if new_name:
            self.signal_edit_tag.emit(tag_index, new_name, old_colour_id)
        if new_name and new_colour:
            self.signal_edit_tag.emit(tag_index, new_name, new_colour)

    def update_tag(self, new_name, new_colour):
        if new_name == self.old_name:
            new_colour_name = self.db_cursor.get_colour_by_id(new_colour)[0][0]
            if new_colour_name == self.old_colour:
                self.tag_edit_window.close()
            else:
                self.tag_labels[self.get_tag_label_by_name(self.old_name)].tags_dict[self.old_name]['colour'] = new_colour_name
                self.edit_signal(new_colour=new_colour)
                for i in range(len(self.tags_list)):
                    if self.tags_list[i][0] == self.old_name:
                        self.tags_list[i] = (self.old_name, new_colour_name)
                self.repaint()
                self.tag_edit_window.close()
        elif self.is_unique_tag(self.tag_edit_window, new_name):
            self.edit_tag_item(self.old_name, self.old_colour, new_name, new_colour)
            self.edit_signal(new_name=new_name, new_colour=new_colour)
            
            self.change_geometry()
            temp = TagInfo()
            temp.is_pressed = True
            self.tag_labels.append(temp)
            self.repaint()
            self.tag_edit_window.close()

    def old_tag_info(self, old_object):
        old_obj_dict = old_object.tags_dict
        self.old_object = old_object
        self.old_name = list(old_obj_dict.keys())[0]
        self.old_colour = old_object.tags_dict[self.old_name]['colour']

    def new_custom_tag(self):
        self.tag_window = TagWindow()
        self.tag_window.delete_button.hide()
        self.tag_window.add_tag_signal.connect(self.init_new_tag)
        self.tag_window.setModal(True)
        self.tag_window.show()

    def init_new_tag(self, tag_name, selected_colour):
        colour_name = self.db_cursor.get_colour_by_id(selected_colour)
        if self.is_unique_tag(self.tag_window, tag_name):
            self.tags_list.append((tag_name, colour_name[0][0]))
            tag_index = len(self.tags_list)
            self.change_geometry()
            temp = TagInfo()
            temp.is_pressed = True
            self.tag_labels.append(temp)
            self.signal_add_tag.emit(tag_index, tag_name, selected_colour)
            self.repaint()

            self.tag_window.close()

    @property
    def pressed_tags(self):
        pressed_tags_list = []
        for i in self.tag_labels:
            if i.is_checked:
                pressed_tags_list.append(self.tag_labels.index(i) + 1)
        return pressed_tags_list

    def new_tag_button(self):
        x_pos, y_pos, button_w, button_h = int(self.width()/2) - int(self.width()/8), 30, 50, 30
        self.custom_tag_button.setText('+')
        button_style = """border-radius: 8px;
                            color: black;
                            text-align: center;
                            font-size: 16px;
                            border: 2px solid orange;"""
        self.custom_tag_button.setStyleSheet(button_style)
        self.custom_tag_button.setGeometry(x_pos, y_pos, button_w, button_h)