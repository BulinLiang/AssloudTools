# -*- coding: utf-8 -*-



import PyMVCS
import root
from facade.launcher import LauncherFacade
from facade.app import AppFacade

import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    # 实例化应用
    app = QApplication(sys.argv)

    # 创建启动UI
    launcherFacade = LauncherFacade()
    PyMVCS.UIFacade.Register(LauncherFacade.NAME, launcherFacade)

    # 创建应用UI
    appFacade = AppFacade()
    PyMVCS.UIFacade.Register(AppFacade.NAME, appFacade)

    # 初始化MVCS框架
    logger = PyMVCS.Logger()
    config = PyMVCS.Config()
    framework = PyMVCS.Framework(config, logger)
    # 初始化MVCS框架
    framework.Initialize()

    # 注册部件，将部件加入到部件中心
    root.Register(framework)

    # 装载部件，调用所有部件的setup方法
    framework.Setup()

    # 进入事件循环
    result = app.exec_()

    # 拆除部件，调用所有部件的dismantle方法
    framework.Dismantle()

    # 注销部件，将部件从部件中心移除
    root.Cancel(framework)
    
    # 销毁MVCS框架
    framework.Release()

    # 退出程序返回状态码
    sys.exit(result)
