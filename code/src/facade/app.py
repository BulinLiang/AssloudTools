from PyQt5.QtWidgets import QMainWindow
import ui.app as UiApp

class AppFacade:

    NAME = 'AppFacade'

    def __init__(self):
        # 实例化窗体
        self.window = QMainWindow()
        # 实例化界面
        self.ui = UiApp.Ui_MainWindow()
        # 装载界面到窗体
        self.ui.setupUi(self.window)


