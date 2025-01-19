import os

from components import ThemedOptionCardPlane
from icons import IconDictionary
from PyQt5.Qt import QColor, QPoint
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QTextEdit
from settings_parser import SettingsParser
from todos_parser import TODOParser

from siui.components.widgets import (
    SiCheckBox,
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiSimpleButton,
    SiSvgLabel,
    SiSwitch,
    SiToggleButton,
)
from siui.core.animation import SiExpAnimation
from siui.core.color import Color
from siui.core.globals import NewGlobal, SiGlobal
from siui.gui.tooltip import ToolTipWindow

# 创建删除队列
SiGlobal.todo_list = NewGlobal()
SiGlobal.todo_list.delete_pile = []

# 创建锁定位置变量
SiGlobal.todo_list.position_locked = False

# 创建设置文件解析器并写入全局变量
SiGlobal.todo_list.settings_parser = SettingsParser("./options.ini")
SiGlobal.todo_list.todos_parser = TODOParser("./todos.ini")

def lock_position(state):
    SiGlobal.todo_list.position_locked = state


# 主题颜色
def load_colors(is_dark=True):
    if is_dark is True:  # 深色主题
        # 加载图标
        SiGlobal.siui.icons.update(IconDictionary(color="#e1d9e8").icons)

        # 设置颜色
        SiGlobal.siui.colors["THEME"] = "#e1d9e8"
        SiGlobal.siui.colors["PANEL_THEME"] = "#0F85D3"
        SiGlobal.siui.colors["BACKGROUND_COLOR"] = "#252229"
        SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"] = SiGlobal.siui.colors["INTERFACE_BG_A"]
        SiGlobal.siui.colors["BORDER_COLOR"] = "#3b373f"
        SiGlobal.siui.colors["TOOLTIP_BG"] = "ef413a47"
        SiGlobal.siui.colors["SVG_A"] = SiGlobal.siui.colors["THEME"]

        SiGlobal.siui.colors["THEME_TRANSITION_A"] = "#52389a"
        SiGlobal.siui.colors["THEME_TRANSITION_B"] = "#9c4e8b"

        SiGlobal.siui.colors["TEXT_A"] = "#FFFFFF"
        SiGlobal.siui.colors["TEXT_B"] = "#e1d9e8"
        SiGlobal.siui.colors["TEXT_C"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.75)
        SiGlobal.siui.colors["TEXT_D"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.6)
        SiGlobal.siui.colors["TEXT_E"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.5)

        SiGlobal.siui.colors["SWITCH_DEACTIVATE"] = "#D2D2D2"
        SiGlobal.siui.colors["SWITCH_ACTIVATE"] = "#100912"

        SiGlobal.siui.colors["BUTTON_HOVER"] = "#10FFFFFF"
        SiGlobal.siui.colors["BUTTON_FLASH"] = "#20FFFFFF"

        SiGlobal.siui.colors["SIMPLE_BUTTON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

        SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0)
        SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

    else:  # 亮色主题
        # 加载图标
        SiGlobal.siui.icons.update(IconDictionary(color="#0F85D3").icons)

        # 设置颜色
        SiGlobal.siui.colors["THEME"] = "#0F85D3"
        SiGlobal.siui.colors["PANEL_THEME"] = "#0F85D3"
        SiGlobal.siui.colors["BACKGROUND_COLOR"] = "#F3F3F3"
        SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"] = "#e8e8e8"
        SiGlobal.siui.colors["BORDER_COLOR"] = "#d0d0d0"
        SiGlobal.siui.colors["TOOLTIP_BG"] = "#F3F3F3"
        SiGlobal.siui.colors["SVG_A"] = SiGlobal.siui.colors["THEME"]

        SiGlobal.siui.colors["THEME_TRANSITION_A"] = "#2abed8"
        SiGlobal.siui.colors["THEME_TRANSITION_B"] = "#2ad98e"

        SiGlobal.siui.colors["TEXT_A"] = "#1f1f2f"
        SiGlobal.siui.colors["TEXT_B"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.85)
        SiGlobal.siui.colors["TEXT_C"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.75)
        SiGlobal.siui.colors["TEXT_D"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.6)
        SiGlobal.siui.colors["TEXT_E"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.5)

        SiGlobal.siui.colors["SWITCH_DEACTIVATE"] = "#bec1c7"
        SiGlobal.siui.colors["SWITCH_ACTIVATE"] = "#F3F3F3"

        SiGlobal.siui.colors["BUTTON_HOVER"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.0625)
        SiGlobal.siui.colors["BUTTON_FLASH"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.43)

        SiGlobal.siui.colors["SIMPLE_BUTTON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.6)

        SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0)
        SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

    SiGlobal.siui.reloadAllWindowsStyleSheet()


# 加载主题颜色
load_colors(is_dark=False)


class SingleSettingOption(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSpacing(2)

        self.title = SiLabel(self)
        self.title.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.title.setAutoAdjustSize(True)

        self.description = SiLabel(self)
        self.description.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.description.setAutoAdjustSize(True)

        self.addWidget(self.title)
        self.addWidget(self.description)
        self.addPlaceholder(4)

    def setTitle(self, title: str, description: str):
        self.title.setText(title)
        self.description.setText(description)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        self.description.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_D"]))


class SingleTODOOption(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setShrinking(True)

        self.check_box = SiCheckBox(self)
        self.check_box.resize(12, 12)
        self.check_box.setText(" ")
        self.check_box.toggled.connect(self._onChecked)

        self.text_label = SiLabel(self)
        self.text_label.resize(500 - 48 - 48 - 32, 32)
        self.text_label.setWordWrap(True)
        self.text_label.setAutoAdjustSize(True)
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_label.setFixedStyleSheet("padding-top: 2px; padding-bottom: 2px")

        self.addWidget(self.check_box)
        self.addWidget(self.text_label)

        self.move = self.moveTo

        # 添加索引属性，用于跟踪待办事项在列表中的位置
        self.todo_index = -1
        
        # 初始化时自动载入样式表
        self.reloadStyleSheet()

    def _onChecked(self, state):
        """处理复选框状态改变事件"""
        print(f"\n=== 待办事项状态改变 ===")
        print(f"索引: {self.todo_index}")
        print(f"文本: {self.text_label.text()}")
        print(f"状态: {'已完成' if state else '未完成'}")
        
        # 更新待办事项状态
        if self.todo_index >= 0:
            SiGlobal.todo_list.todos_parser.set_done(self.todo_index, state)
            # 更新文本样式
            if state:
                self.text_label.setFixedStyleSheet("padding-top: 2px; padding-bottom: 2px; text-decoration: line-through; color: gray")
            else:
                self.text_label.setFixedStyleSheet("padding-top: 2px; padding-bottom: 2px")
            
            # 立即保存到文件
            try:
                SiGlobal.todo_list.todos_parser.write()
                print("待办事项状态已保存到文件")
            except Exception as e:
                print(f"保存待办事项状态时出错: {str(e)}")
        
        print("=== 状态更新完成 ===\n")

    def setText(self, text: str, done: bool = False, index: int = -1):
        """设置待办事项文本和状态"""
        self.text_label.setText(text)
        self.todo_index = index
        # 设置复选框状态但不触发信号
        self.check_box.blockSignals(True)
        self.check_box.setChecked(done)
        self.check_box.blockSignals(False)
        # 更新文本样式
        if done:
            self.text_label.setFixedStyleSheet("padding-top: 2px; padding-bottom: 2px; text-decoration: line-through; color: gray")
        else:
            self.text_label.setFixedStyleSheet("padding-top: 2px; padding-bottom: 2px")

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.text_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))

    def adjustSize(self):
        self.setFixedHeight(self.text_label.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.text_label.setFixedWidth(event.size().width() - 48)
        self.text_label.adjustSize()
        self.adjustSize()


class AppHeaderPanel(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background_label = SiLabel(self)
        self.background_label.setFixedStyleSheet("border-radius: 8px")

        self.container_h = SiDenseHContainer(self)
        self.container_h.setAlignCenter(True)
        self.container_h.setFixedHeight(48)
        self.container_h.setSpacing(0)

        self.icon = SiSvgLabel(self)
        self.icon.resize(32, 32)
        self.icon.setSvgSize(16, 16)

        self.unfold_button = SiToggleButton(self)
        self.unfold_button.setFixedHeight(32)
        self.unfold_button.attachment().setText("0个待办事项")
        self.unfold_button.setChecked(True)

        self.settings_button = SiToggleButton(self)
        self.settings_button.resize(32, 32)
        self.settings_button.setHint("设置")
        self.settings_button.setChecked(False)

        self.add_todo_button = SiToggleButton(self)
        self.add_todo_button.resize(32, 32)
        self.add_todo_button.setHint("添加新待办")
        self.add_todo_button.setChecked(False)

        self.container_h.addPlaceholder(16)
        self.container_h.addWidget(self.icon)
        self.container_h.addPlaceholder(4)
        self.container_h.addWidget(self.unfold_button)

        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.settings_button, "right")
        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.add_todo_button, "right")

        # 按钮加入全局变量
        SiGlobal.todo_list.todo_list_unfold_button = self.unfold_button
        SiGlobal.todo_list.add_todo_unfold_button = self.add_todo_button
        SiGlobal.todo_list.settings_unfold_button = self.settings_button

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.resize(event.size().width(), 48)
        self.container_h.resize(event.size().width(), 48)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        # 按钮颜色
        self.unfold_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                         SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])
        self.settings_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                           SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])
        self.add_todo_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                           SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])

        # svg 图标
        self.settings_button.attachment().load(SiGlobal.siui.icons["fi-rr-menu-burger"])
        self.add_todo_button.attachment().load(SiGlobal.siui.icons["fi-rr-apps-add"])
        self.icon.load('<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" '
                       'data-name="Layer 1" viewBox="0 0 24 24" width="512" height="512"><path d="M0,8v-1C0,4.243,'
                       '2.243,2,5,2h1V1c0-.552,.447-1,1-1s1,.448,1,1v1h8V1c0-.552,.447-1,1-1s1,.448,1,1v1h1c2.757,0,'
                       '5,2.243,5,5v1H0Zm24,2v9c0,2.757-2.243,5-5,5H5c-2.757,0-5-2.243-5-5V10H24Zm-6.168,'
                       '3.152c-.384-.397-1.016-.409-1.414-.026l-4.754,4.582c-.376,.376-1.007,'
                       '.404-1.439-.026l-2.278-2.117c-.403-.375-1.035-.354-1.413,.052-.376,.404-.353,1.037,.052,'
                       '1.413l2.252,2.092c.566,.567,1.32,.879,2.121,.879s1.556-.312,2.108-.866l4.74-4.568c.397-.383,'
                       '.409-1.017,.025-1.414Z" fill="{}" /></svg>'.format(SiGlobal.siui.colors["SVG_A"]).encode())

        self.background_label.setStyleSheet("""background-color: {}; border: 1px solid {}""".format(
            SiGlobal.siui.colors["BACKGROUND_COLOR"], SiGlobal.siui.colors["BORDER_COLOR"]))
        self.unfold_button.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))


class TODOListPanel(ThemedOptionCardPlane):
    todoAmountChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("全部待办")
        self.setUseSignals(True)

        # 添加分组标签
        self.pending_label = SiLabel(self)
        self.pending_label.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.pending_label.setText("待办事项")
        self.pending_label.setAutoAdjustSize(True)
        self.pending_label.setAlignment(Qt.AlignLeft)
        self.pending_label.hide()

        self.completed_label = SiLabel(self)
        self.completed_label.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.completed_label.setText("已完成")
        self.completed_label.setAutoAdjustSize(True)
        self.completed_label.setAlignment(Qt.AlignLeft)
        self.completed_label.hide()

        self.no_todo_label = SiLabel(self)
        self.no_todo_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.no_todo_label.setAutoAdjustSize(True)
        self.no_todo_label.setText("当前没有待办哦")
        self.no_todo_label.setAlignment(Qt.AlignCenter)
        self.no_todo_label.hide()

        self.body().setUseMoveTo(False)
        self.body().setShrinking(True)
        self.body().setAdjustWidgetsSize(True)

        self.footer().setFixedHeight(64)
        self.footer().setSpacing(8)
        self.footer().setAlignCenter(True)

        self.complete_all_button = SiSimpleButton(self)
        self.complete_all_button.resize(32, 32)
        self.complete_all_button.setHint("全部完成")
        self.complete_all_button.clicked.connect(self._onCompleteAllButtonClicked)

        self.footer().addWidget(self.complete_all_button, "right")

        # 全局方法
        SiGlobal.todo_list.addTODO = self.addTODO

    def updateTODOAmount(self):
        """更新待办事项数量"""
        pending_count = 0
        completed_count = 0
        for widget in self.body().widgets_top:
            if isinstance(widget, SingleTODOOption):
                if widget.check_box.isChecked():
                    completed_count += 1
                else:
                    pending_count += 1

        # 只发送未完成的待办事项数量
        self.todoAmountChanged.emit(pending_count)
        
        # 更新标题显示
        if pending_count + completed_count == 0:
            self.setTitle("全部待办")
        else:
            self.setTitle(f"{pending_count}个待办事项")

        # 显示或隐藏分组标签
        if pending_count + completed_count > 0:
            if pending_count > 0:
                self.pending_label.show()
            else:
                self.pending_label.hide()
            
            if completed_count > 0:
                self.completed_label.show()
            else:
                self.completed_label.hide()
            
            self.no_todo_label.hide()
        else:
            self.pending_label.hide()
            self.completed_label.hide()
            self.no_todo_label.show()

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()
        self.complete_all_button.attachment().load(SiGlobal.siui.icons["fi-rr-list-check"])

    def _onCompleteAllButtonClicked(self):
        """处理"全部完成"按钮点击事件"""
        print("\n=== 标记所有待办事项为完成 ===")
        for obj in self.body().widgets_top:
            if isinstance(obj, SingleTODOOption) and not obj.check_box.isChecked():
                obj.check_box.setChecked(True)
        self._reorderTodoItems()  # 重新排序
        print("=== 完成 ===\n")

    def _reorderTodoItems(self):
        """重新排序待办事项，未完成的在上方，已完成的在下方"""
        print("\n=== 重新排序待办事项 ===")
        
        # 收集所有待办事项部件
        pending_items = []
        completed_items = []
        
        # 从body中移除所有待办事项
        widgets = self.body().widgets_top.copy()
        for widget in widgets:
            if isinstance(widget, SingleTODOOption):
                self.body().removeWidget(widget)
                if widget.check_box.isChecked():
                    completed_items.append(widget)
                else:
                    pending_items.append(widget)
            elif widget in [self.pending_label, self.completed_label, self.no_todo_label]:
                self.body().removeWidget(widget)
        
        # 添加未完成分组
        if pending_items:
            self.body().addWidget(self.pending_label)
            for item in pending_items:
                self.body().addWidget(item)
                item.show()
        
        # 添加已完成分组
        if completed_items:
            self.body().addWidget(self.completed_label)
            for item in completed_items:
                self.body().addWidget(item)
                item.show()
        
        # 如果没有待办事项，显示提示
        if not pending_items and not completed_items:
            self.body().addWidget(self.no_todo_label)
            self.no_todo_label.show()
        
        print(f"待办事项: {len(pending_items)}个")
        print(f"已完成: {len(completed_items)}个")
        print("=== 排序完成 ===\n")
        
        # 更新显示
        self.updateTODOAmount()
        if SiGlobal.todo_list.todo_list_unfold_button.isChecked():
            self.adjustSize()

    def addTODO(self, text, done=False, index=-1):
        """添加新的待办事项"""
        print(f"\n=== 添加新待办事项 ===")
        print(f"文本: {text}")
        print(f"状态: {'已完成' if done else '未完成'}")
        print(f"索引: {index}")

        # 创建新的待办事项
        new_todo = SingleTODOOption(self)
        new_todo.setText(text, done, index)
        new_todo.check_box.toggled.connect(lambda state: self._reorderTodoItems())
        
        # 先添加到界面
        if done:
            # 如果是已完成的，确保"已完成"标签存在
            if self.completed_label not in self.body().widgets_top:
                self.body().addWidget(self.completed_label)
            self.completed_label.show()
            self.body().addWidget(new_todo)
        else:
            # 如果是未完成的，确保"待办事项"标签存在
            if self.pending_label not in self.body().widgets_top:
                self.body().addWidget(self.pending_label)
            self.pending_label.show()
            self.body().addWidget(new_todo)
        
        # 显示新添加的待办事项
        new_todo.show()
        new_todo.adjustSize()
        
        # 隐藏"没有待办"提示
        self.no_todo_label.hide()
        
        # 重新排序所有待办事项
        self._reorderTodoItems()
        
        # 更新界面
        SiGlobal.todo_list.todo_list_unfold_button.setChecked(True)
        self.adjustSize()
        self.updateTODOAmount()
        
        print("=== 添加完成 ===\n")

    def showEvent(self, a0):
        super().showEvent(a0)
        self._reorderTodoItems()  # 显示时重新排序

    def adjustSize(self):
        self.body().adjustSize()
        super().adjustSize()

    def leaveEvent(self, event):
        super().leaveEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.no_todo_label.resize(event.size().width(), 150)


class AddNewTODOPanel(ThemedOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("添加新待办")
        self.setUseSignals(True)

        self.confirm_button = SiSimpleButton(self)
        self.confirm_button.resize(32, 32)
        self.confirm_button.setHint("确认并添加")

        self.cancel_button = SiSimpleButton(self)
        self.cancel_button.resize(32, 32)
        self.cancel_button.setHint("取消")

        self.header().addWidget(self.cancel_button, "right")
        self.header().addWidget(self.confirm_button, "right")

        self.instruction = SiLabel(self)
        self.instruction.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.instruction.setText("请输入待办内容")

        self.text_edit = QTextEdit(self)
        self.text_edit.setFixedHeight(70)
        self.text_edit.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.text_edit.lineWrapMode()

        self.body().setAdjustWidgetsSize(True)
        self.body().setSpacing(4)
        self.body().addWidget(self.instruction)
        self.body().addWidget(self.text_edit)

    def adjustSize(self):
        self.resize(self.width(), 200)

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()

        self.confirm_button.attachment().load(SiGlobal.siui.icons["fi-rr-check"])
        self.cancel_button.attachment().load(SiGlobal.siui.icons["fi-rr-cross"])
        self.instruction.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        self.text_edit.setStyleSheet(
            """
            border: 1px solid {};
            background-color: {};
            border-radius: 4px;
            padding-left: 8px; padding-right: 8px;
            color: {}
            """.format(SiGlobal.siui.colors["BORDER_COLOR"],
                       SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"],
                       SiGlobal.siui.colors["TEXT_B"])
        )

    def showEvent(self, a0):
        super().showEvent(a0)
        self.setForceUseAnimations(True)


class SettingsPanel(ThemedOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setTitle("设置")
        self.setUseSignals(True)

        # 启用深色模式
        self.use_dark_mode = SingleSettingOption(self)
        self.use_dark_mode.setTitle("深色模式", "在深色主题的计算机上提供更佳的视觉效果")

        self.button_use_dark_mode = SiSwitch(self)
        self.button_use_dark_mode.setFixedHeight(32)
        self.button_use_dark_mode.toggled.connect(load_colors)
        self.button_use_dark_mode.toggled.connect(
            lambda b: SiGlobal.todo_list.settings_parser.modify("USE_DARK_MODE", b))
        self.button_use_dark_mode.setChecked(SiGlobal.todo_list.settings_parser.options["USE_DARK_MODE"])

        self.use_dark_mode.addWidget(self.button_use_dark_mode)
        self.use_dark_mode.addPlaceholder(16)

        # 锁定位置
        self.fix_position = SingleSettingOption(self)
        self.fix_position.setTitle("锁定位置", "阻止拖动窗口以保持位置不变")

        self.button_fix_position = SiSwitch(self)
        self.button_fix_position.setFixedHeight(32)
        self.button_fix_position.toggled.connect(lock_position)
        self.button_fix_position.toggled.connect(
            lambda b: SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION", b))
        self.button_fix_position.setChecked(SiGlobal.todo_list.settings_parser.options["FIXED_POSITION"])

        self.fix_position.addWidget(self.button_fix_position)
        self.fix_position.addPlaceholder(16)

        # 添加到body (只添加需要保留的选项)
        self.body().setAdjustWidgetsSize(True)
        self.body().addWidget(self.use_dark_mode)
        self.body().addWidget(self.fix_position)
        
        # 添加退出按钮
        self.exit_option = SingleSettingOption(self)
        self.exit_option.setTitle("退出程序", "关闭待办事项程序")

        self.button_exit = SiSimpleButton(self)
        self.button_exit.setFixedHeight(32)
        self.button_exit.attachment().setText("退出程序")
        self.button_exit.clicked.connect(self._onExitButtonClicked)
        self.button_exit.adjustSize()

        self.exit_option.addWidget(self.button_exit)
        self.exit_option.addPlaceholder(16)

        # 添加到body
        self.body().setAdjustWidgetsSize(True)
        self.body().addWidget(self.exit_option)
        self.body().addPlaceholder(16)

    def _onExitButtonClicked(self):
        """处理退出按钮点击事件"""
        print("退出按钮被点击")
        # 获取主窗口并调用其 close 方法
        main_window = SiGlobal.siui.windows.get("MAIN_WINDOW")
        if main_window:
            print("正在关闭主窗口...")
            main_window.close()  # 这会触发 closeEvent
        else:
            print("未找到主窗口，直接退出")
            QCoreApplication.quit()

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()

        # 只保留退出按钮的样式设置
        self.button_exit.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])

    def showEvent(self, a0):
        super().showEvent(a0)
        self.setForceUseAnimations(True)


class TODOApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 窗口周围留白，供阴影使用
        self.padding = 48
        self.anchor = QPoint(self.x(), self.y())
        
        # 获取保存的位置，如果没有则使用默认位置（左上角）
        saved_x = SiGlobal.todo_list.settings_parser.options.get("FIXED_POSITION_X", 0)
        saved_y = SiGlobal.todo_list.settings_parser.options.get("FIXED_POSITION_Y", 0)
        self.fixed_position = QPoint(saved_x, saved_y)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 初始化全局变量
        SiGlobal.todo_list.todo_list_unfold_state = True
        SiGlobal.todo_list.add_todo_unfold_state = False

        # 初始化工具提示窗口
        SiGlobal.siui.windows["TOOL_TIP"] = ToolTipWindow()
        SiGlobal.siui.windows["TOOL_TIP"].show()
        SiGlobal.siui.windows["TOOL_TIP"].hide_()
        SiGlobal.siui.windows["MAIN_WINDOW"] = self

        # 创建移动动画
        self.move_animation = SiExpAnimation(self)
        self.move_animation.setFactor(1 / 4)
        self.move_animation.setBias(1)
        self.move_animation.setCurrent([self.x(), self.y()])
        self.move_animation.ticked.connect(self._onMoveAnimationTicked)

        # 创建垂直容器
        self.container_v = SiDenseVContainer(self)
        self.container_v.setFixedWidth(500)
        self.container_v.setSpacing(0)
        self.container_v.setShrinking(True)
        self.container_v.setAlignCenter(True)

        # 构建界面
        # 头
        self.header_panel = AppHeaderPanel(self)
        self.header_panel.setFixedWidth(500 - 2 * self.padding)
        self.header_panel.setFixedHeight(48 + 12)

        # 设置面板
        self.settings_panel = SettingsPanel(self)
        self.settings_panel.setFixedWidth(500 - 2 * self.padding)
        self.settings_panel.adjustSize()

        self.settings_panel_placeholder = SiLabel(self)
        self.settings_panel_placeholder.setFixedHeight(12)
        self._onSettingsButtonToggled(False)

        # 添加新待办面板
        self.add_todo_panel = AddNewTODOPanel(self)
        self.add_todo_panel.setFixedWidth(500 - 2 * self.padding)
        self.add_todo_panel.adjustSize()

        self.add_todo_panel_placeholder = SiLabel(self)
        self.add_todo_panel_placeholder.setFixedHeight(12)
        self._onAddTODOButtonToggled(False)

        # 全部待办面板
        self.todo_list_panel = TODOListPanel(self)
        self.todo_list_panel.setFixedWidth(500 - 2 * self.padding)

        self.todo_list_panel_placeholder = SiLabel(self)
        self.todo_list_panel_placeholder.setFixedHeight(12)
        self._onShowTODOButtonToggled(True)

        # <- 添加到垂直容器
        self.container_v.addWidget(self.header_panel)
        self.container_v.addWidget(self.settings_panel)
        self.container_v.addWidget(self.settings_panel_placeholder)
        self.container_v.addWidget(self.add_todo_panel)
        self.container_v.addWidget(self.add_todo_panel_placeholder)
        self.container_v.addWidget(self.todo_list_panel)
        self.container_v.addWidget(self.todo_list_panel_placeholder)

        # 绑定界面信号
        self.header_panel.unfold_button.toggled.connect(self._onShowTODOButtonToggled)
        self.header_panel.add_todo_button.toggled.connect(self._onAddTODOButtonToggled)
        self.header_panel.settings_button.toggled.connect(self._onSettingsButtonToggled)

        self.settings_panel.resized.connect(self._onTODOWindowResized)
        self.add_todo_panel.resized.connect(self._onTODOWindowResized)
        self.todo_list_panel.resized.connect(self._onTODOWindowResized)

        self.add_todo_panel.confirm_button.clicked.connect(self._onAddTODOConfirmButtonClicked)
        self.add_todo_panel.cancel_button.clicked.connect(self._onAddTODOCancelButtonClicked)

        self.todo_list_panel.todoAmountChanged.connect(self._onTODOAmountChanged)

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(48)
        self.setGraphicsEffect(shadow)

        self.resize(500, 800)
        self.move(self.fixed_position.x(), self.fixed_position.y())
        SiGlobal.siui.reloadAllWindowsStyleSheet()

        # 读取 todos.ini 添加到待办
        print("\n=== 开始加载待办事项 ===")
        todos = SiGlobal.todo_list.todos_parser.todos
        print(f"从文件读取到 {len(todos)} 个待办事项")
        for index, todo in enumerate(todos):
            print(f"添加待办事项: {todo}")
            self.todo_list_panel.addTODO(todo["text"], todo["done"], index)
        print("=== 加载完成 ===\n")

    def adjustSize(self):
        h = (self.header_panel.height() + 12 +
             self.settings_panel.height() + 12 +
             self.add_todo_panel.height() + 12 +
             self.todo_list_panel.height() +
             2 * self.padding)
        self.resize(self.width(), h)
        self.container_v.adjustSize()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.container_v.move(0, self.padding)

    def showEvent(self, a0):
        super().showEvent(a0)

    def _onTODOWindowResized(self, size):
        w, h = size
        self.adjustSize()

    def _onShowTODOButtonToggled(self, state):
        if state is True:
            self.todo_list_panel_placeholder.setFixedHeight(12)
            self.todo_list_panel.adjustSize()
        else:
            self.todo_list_panel_placeholder.setFixedHeight(0)
            self.todo_list_panel.resize(self.todo_list_panel.width(), 0)

    def _onAddTODOButtonToggled(self, state):
        # 如果打开添加待办面板，则关闭设置面板
        if state is True:
            # 如果打开添加待办面板，则关闭设置面板
            self.header_panel.settings_button.setChecked(False)
            self.settings_panel_placeholder.setFixedHeight(0)
            self.settings_panel.resize(self.settings_panel.width(), 0)
        
        # 原有的显示/隐藏添加待办面板的代码
        if state is True:
            self.add_todo_panel_placeholder.setFixedHeight(12)
            self.add_todo_panel.adjustSize()
        else:
            self.add_todo_panel_placeholder.setFixedHeight(0)
            self.add_todo_panel.resize(self.add_todo_panel.width(), 0)

    def _onSettingsButtonToggled(self, state):
        # 如果打开设置面板，则关闭添加待办面板
        if state is True:
            self.header_panel.add_todo_button.setChecked(False)
            self.add_todo_panel_placeholder.setFixedHeight(0)
            self.add_todo_panel.resize(self.add_todo_panel.width(), 0)

        # 原有的显示/隐藏设置面板的代码
        if state is True:
            self.settings_panel_placeholder.setFixedHeight(12)
            self.settings_panel.adjustSize()
        else:
            self.settings_panel_placeholder.setFixedHeight(0)
            self.settings_panel.resize(self.settings_panel.width(), 0)

    def _onTODOAmountChanged(self, amount):
        if amount == 0:
            self.header_panel.unfold_button.attachment().setText("没有待办")
        else:
            self.header_panel.unfold_button.attachment().setText(f"{amount}个待办事项")
        self.header_panel.unfold_button.adjustSize()

    def _onAddTODOConfirmButtonClicked(self):
        text = self.add_todo_panel.text_edit.toPlainText()
        self.add_todo_panel.text_edit.setText("")
        self.header_panel.add_todo_button.setChecked(False)

        while text[-1:] == "\n":
            text = text[:-1]

        if text == "":
            return

        self.todo_list_panel.addTODO(text)

    def _onAddTODOCancelButtonClicked(self):
        self.add_todo_panel.text_edit.setText("")
        self.header_panel.add_todo_button.setChecked(False)

    def moveTo(self, x, y):
        self.move_animation.setTarget([x, y])
        self.move_animation.try_to_start()

    def moveEvent(self, a0):
        super().moveEvent(a0)
        x, y = a0.pos().x(), a0.pos().y()
        self.move_animation.setCurrent([x, y])

    def _onMoveAnimationTicked(self, pos):
        self.move(int(pos[0]), int(pos[1]))
        if SiGlobal.todo_list.position_locked is False:
            self.fixed_position = self.pos()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.anchor = event.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not (event.buttons() & Qt.LeftButton):
            return

        new_pos = event.pos() - self.anchor + self.frameGeometry().topLeft()
        x, y = new_pos.x(), new_pos.y()

        self.moveTo(x, y)

    def mouseReleaseEvent(self, a0):
        if SiGlobal.todo_list.position_locked is True:
            self.moveTo(self.fixed_position.x(), self.fixed_position.y())

    def _saveTodos(self):
        """保存待办事项到文件"""
        try:
            print("\n=== 开始保存待办事项 ===")
            # 获取当前待办，并写入 todos.ini
            todos = []
            widgets = self.todo_list_panel.body().widgets_top
            print(f"找到的部件数量: {len(widgets)}")
            
            for index, widget in enumerate(widgets):
                if hasattr(widget, 'text_label'):
                    text = widget.text_label.text()
                    done = widget.check_box.isChecked()
                    todos.append({"text": text, "done": done})
                    print(f"添加待办事项: {text}")
                else:
                    print(f"警告：部件没有 text_label 属性: {type(widget)}")
            
            print(f"\n待保存的待办事项: {todos}")
            print(f"待办事项数量: {len(todos)}")
            
            # 确保路径是绝对路径
            import os
            todos_file = os.path.abspath("./todos.ini")
            print(f"待办文件路径: {todos_file}")
            
            # 更新并保存
            SiGlobal.todo_list.todos_parser.todos = todos
            print(f"Parser中的待办事项: {SiGlobal.todo_list.todos_parser.todos}")
            print(f"Parser中待办事项数量: {len(SiGlobal.todo_list.todos_parser.todos)}")
            
            SiGlobal.todo_list.todos_parser.write()
            
            # 验证文件是否写入
            try:
                with open(todos_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    print(f"\n文件内容:\n{content}")
                    print(f"文件大小: {len(content)} 字节")
            except Exception as e:
                print(f"读取文件失败: {str(e)}")

            print("=== 保存完成 ===\n")
            return True
        except Exception as e:
            import traceback
            print(f"保存待办事项时出错:")
            print(traceback.format_exc())
            return False

    def closeEvent(self, a0):
        """处理窗口关闭事件"""
        try:
            print("正在处理关闭事件...")
            
            # 保存待办事项
            if self._saveTodos():
                print("待办事项保存成功")
            else:
                print("警告：待办事项保存失败")
            
            # 保存窗口位置
            try:
                SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION_X", self.fixed_position.x())
                SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION_Y", self.fixed_position.y())
                SiGlobal.todo_list.settings_parser.write()
                print("窗口位置保存成功")
            except Exception as e:
                print(f"保存窗口位置失败: {str(e)}")

            # 关闭工具提示窗口
            if "TOOL_TIP" in SiGlobal.siui.windows:
                SiGlobal.siui.windows["TOOL_TIP"].close()
            
            # 调用父类的 closeEvent
            super().closeEvent(a0)
            print("窗口已关闭")
            
        except Exception as e:
            import traceback
            print(f"关闭事件处理出错:")
            print(traceback.format_exc())
        finally:
            # 确保程序退出
            QCoreApplication.quit()
