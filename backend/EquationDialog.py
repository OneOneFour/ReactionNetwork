from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QWidget, QLabel, QSpinBox, QHBoxLayout

symbols = ["X", "Y"]


# class EquationDialog(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(EquationDialog, self).__init__(*args, **kwargs)
#         self.setWindowTitle("Add Equation")
#
#         QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
#         self.layout = QVBoxLayout()
#
#         self.buttonBox = QDialogButtonBox(QBtn)
#
#         self.layout.addWidget(self.buttonBox)
#         self.setLayout(self.layout)
class EqnLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(EqnLabel, self).__init__(*args, **kwargs)
        font = self.font()
        font.setPointSize(20)
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)


class EquationEditWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(EquationEditWidget, self).__init__(*args, **kwargs)
        self.layout = QHBoxLayout()

        for i, symbol in enumerate(symbols):
            self.layout.addWidget(SymbolWidget(symbol))
            if i != len(symbols) - 1:
                self.layout.addWidget(EqnLabel("+"))

        self.arrow_widget = QWidget()
        self.arrow_layout = QVBoxLayout()
        self.arrow_layout.addWidget(EqnLabel("A"))
        self.arrow_layout.addWidget(EqnLabel( u"\u2192"))
        self.arrow_widget.setLayout(self.arrow_layout)
        self.layout.addWidget(self.arrow_widget)

        for i, symbol in enumerate(symbols):
            self.layout.addWidget(SymbolWidget(symbol))
            if i != len(symbols) - 1:
                self.layout.addWidget(EqnLabel("+"))

        self.setLayout(self.layout)
        self.setMaximumHeight(100)


class SymbolWidget(QWidget):
    def __init__(self, symbol, *args, **kwargs):
        super(SymbolWidget, self).__init__(*args, **kwargs)
        self.layout = QHBoxLayout()
        self.symbol = symbol
        self.dropDown = QSpinBox()
        self.dropDown.setRange(0, 10)
        self.dropDown.valueChanged.connect(self.set_symbol_var)
        self.layout.addWidget(self.dropDown)
        self.layout.addWidget(QLabel(symbol))
        self.setLayout(self.layout)

    def set_symbol_var(self, v):
        print(f"Set {self.symbol} value to {v}")
