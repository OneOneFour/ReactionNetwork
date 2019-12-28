from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from .EquationDialog import EquationEditWidget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Mathematical Biology")

        self.centralWidget = QWidget()
        self.layout = QVBoxLayout()

        self.layout.addWidget(EquationEditWidget())

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.layout.addWidget(self.canvas)
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        new_variable = QAction(QIcon("./backend/calculator--plus.png"),"New Variable", self)
        toolbar.addAction(new_variable)
        remove_variable = QAction(QIcon("./backend/calculator--minus.png"),"Remove Variable", self)
        toolbar.addAction(remove_variable)