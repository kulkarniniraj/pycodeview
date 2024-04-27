import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

import astparser
import libpycodeview as lpcv

class MyWidget(QtWidgets.QWidget):
    def __init__(self, root):
        super().__init__()

        # self.root = Path(root)

        # list views
        self.file_lst_w = QtWidgets.QListWidget()
        # self.file_lst_w.currentItemChanged.connect(self.file_changed)
        self.file_lst_w.itemClicked.connect(self.file_changed)

        self.class_lst_w = QtWidgets.QListWidget()
        # self.class_lst_w.currentItemChanged.connect(self.class_changed)
        self.class_lst_w.itemClicked.connect(self.class_changed)

        self.func_lst_w = QtWidgets.QListWidget()
        # self.func_lst_w.currentItemChanged.connect(self.func_changed)
        self.func_lst_w.itemClicked.connect(self.func_changed)


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

        self.model = lpcv.init(Path(root))
        print('initial model', self.model)
        self.update_view(self.model)

    def set_list_view(self, lst_view: QListWidget, lst_item):
        lst_view.clear()
        i = QtWidgets.QListWidgetItem('.', lst_view)
        for item in lst_item:
            i = QtWidgets.QListWidgetItem(str(item), lst_view)
        return lst_view

    def update_view(self, model: lpcv.Model):
        self.set_list_view(self.file_lst_w, [str(x) for x in model.file_list])
        self.file_lst_w.setCurrentRow(model.selected_file_idx)

        self.set_list_view(self.class_lst_w, [x.name for x in model.class_list])
        self.class_lst_w.setCurrentRow(model.selected_class_idx)

        self.set_list_view(self.func_lst_w, [x.name for x in model.function_list])
        self.func_lst_w.setCurrentRow(model.selected_function_idx)

        self.code_text.setHtml(highlight(model.code, PythonLexer(), 
                                             HtmlFormatter(noclasses=True)))
        print()

    def file_changed(self, cur: QListWidgetItem):
        model = lpcv.update(self.model, (lpcv.Message.FILE_SELECTED, 
                                         self.file_lst_w.currentRow()) )
        self.model = model
        self.update_view(model)

    def class_changed(self, cur: QListWidgetItem):
        '''
        data = symbol_tree.set_active_class(self.class_lst_w.currentRow())
        self.update(data)
        '''
        model = lpcv.update(self.model, (lpcv.Message.CLASS_SELECTED, 
                                         self.class_lst_w.currentRow()) )
        self.model = model
        self.update_view(model)

    def func_changed(self, cur: QListWidgetItem):
        '''
        data = symbol_tree.set_active_func(self.func_lst_w.currentRow())
        self.update(data)
        '''
        model = lpcv.update(self.model, (lpcv.Message.FUNCTION_SELECTED, 
                                         self.func_lst_w.currentRow()) )
        self.model = model
        self.update_view(model)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

def print_help():
    print('''Usage: pycodeview ROOTFOLDER
Loads all python folder in ROOTFOLDER and subfolders and presents Smalltalk IDE like view
''')
if __name__ == "__main__":
    if (len(sys.argv) != 2) or (sys.argv[1] == '-h') or (sys.argv[1] == '--help'):
        print_help()
        sys.exit(0)
    app = QtWidgets.QApplication([])
    fnt = app.font()
    fnt.setPointSize(16)
    app.setFont(fnt)

    widget = MyWidget(sys.argv[1])
    widget.resize(800, 600)
    widget.showMaximized()

    sys.exit(app.exec())        
