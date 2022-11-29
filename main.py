import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

import astparser
import symbol_tree
import syntax

class MyWidget(QtWidgets.QWidget):
    def __init__(self, root):
        super().__init__()

        self.root = Path(root)

        # list views
        self.file_lst_w = QtWidgets.QListWidget()
        self.file_lst_w.currentItemChanged.connect(self.file_changed)

        self.class_lst_w = QtWidgets.QListWidget()
        self.class_lst_w.currentItemChanged.connect(self.class_changed)

        self.func_lst_w = QtWidgets.QListWidget()
        self.func_lst_w.currentItemChanged.connect(self.func_changed)

        self.set_list_view(self.file_lst_w, astparser.get_file_list(self.root))

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.file_lst_w)
        self.hbox.addWidget(self.class_lst_w)
        self.hbox.addWidget(self.func_lst_w)

        # search bar and code viewer
        # self.code_text = QtWidgets.QTextEdit('')
        self.code_text = QtWidgets.QTextEdit('')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.hbox, 4)
        self.layout.addWidget(QtWidgets.QLineEdit(placeholderText = 'Search Term'), 2)
        self.layout.addWidget(self.code_text, 6)

        # self.highlight = syntax.PythonHighlighter(self.code_text)

    def set_list_view(self, lst_view: QListWidget, lst_item):
        lst_view.clear()
        i = QtWidgets.QListWidgetItem('.', lst_view)
        for item in lst_item:
            i = QtWidgets.QListWidgetItem(str(item), lst_view)
        return lst_view

    def update(self, data):
        if 'class_lst' in data:
            self.set_list_view(self.class_lst_w, data['class_lst'])

        if 'func_lst' in data:
            self.set_list_view(self.func_lst_w, data['func_lst'])

        if 'code' in data:
            self.code_text.setHtml(highlight(data['code'], PythonLexer(), 
                                             HtmlFormatter(noclasses=True)))
            # self.code_text.setMarkdown('```\n'+data['code']+'\n```')

    def file_changed(self, cur: QListWidgetItem, prev):
        data = symbol_tree.set_active_file(cur.text())
        self.update(data)

    def class_changed(self, cur: QListWidgetItem, prev):
        data = symbol_tree.set_active_class(self.class_lst_w.currentRow())
        self.update(data)

    def func_changed(self, cur: QListWidgetItem, prev):
        data = symbol_tree.set_active_func(self.func_lst_w.currentRow())
        self.update(data)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    fnt = app.font()
    fnt.setPointSize(16)
    app.setFont(fnt)

    widget = MyWidget(sys.argv[1])
    widget.resize(800, 600)
    widget.showMaximized()

    sys.exit(app.exec())        
