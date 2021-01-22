import logging
import os
# import os.path as osp
import sys

from pathlib import Path
from qtpy import QtCore
from qtpy import QtWidgets

from labelme import __app_name__
from labelme import __version__
from labelme.widgets.app import MainWindow
from labelme.logger import logger
from labelme.utils import newIcon


RESET_CONFIG = False     # 跟注册表相关，记录窗口尺寸位置等设置，使用QSetting实现
LOGGER_LEVEL = 'INFO'    # choices=["DEBUG", "INFO", "WARNING", "FATAL", "ERROR"]


def main():
    logger.setLevel(getattr(logging, LOGGER_LEVEL))
    logger.info("{} V{}".format(__app_name__, __version__))

    translator = QtCore.QTranslator()
    translator.load(
        QtCore.QLocale.system().name(),
        Path(__file__).parent.joinpath('translate').as_posix(),
    )
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(__app_name__)
    app.setWindowIcon(newIcon("icon"))
    app.installTranslator(translator)
    win = MainWindow()

    if RESET_CONFIG:
        logger.info("Resetting Qt config: %s" % win.settings.fileName())
        win.settings.clear()
        sys.exit(0)

    win.show()
    win.raise_()
    sys.exit(app.exec_())


# this main block is required to generate executable by pyinstaller
if __name__ == "__main__":
    main()
