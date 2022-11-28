import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from pathlib import Path

import astparser

def get_class_list_w():
    lst = ['QTClass', 'GTKClass', 'Terminal']
    w = QtWidgets.QListWidget()
    for f in lst:
        i = QtWidgets.QListWidgetItem(f, w)

    return w

def get_func_list_w():
    lst = ['__init__', 'func1', 'func2']
    w = QtWidgets.QListWidget()
    for f in lst:
        i = QtWidgets.QListWidgetItem(f, w)

    return w

def get_code(file_path: Path):
    with open(file_path) as f:
        return f.read()

class MyWidget(QtWidgets.QWidget):
    def set_list_view(self, lst_view: QListWidget, lst_item):
        lst_view.clear()
        i = QtWidgets.QListWidgetItem('.', lst_view)
        for item in lst_item:
            i = QtWidgets.QListWidgetItem(str(item), lst_view)
        return lst_view

    def __init__(self, root):
        super().__init__()

        self.root = Path(root)

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

        self.code_text = QtWidgets.QTextEdit('')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.hbox, 4)
        self.layout.addWidget(QtWidgets.QLineEdit(placeholderText = 'Search Term'), 2)
        self.layout.addWidget(self.code_text, 6)

    def update_class_lst(self):
        class_lst = [x['name'] for x in self.class_lst]
        self.set_list_view(self.class_lst_w, class_lst)

    def update_func_lst(self):
        func_lst = [x['name'] for x in self.func_lst]
        self.set_list_view(self.func_lst_w, func_lst)

    def update_code(self):
        code = get_code(self.file_lst_w.currentItem().text())
        self.code_lines = code.split('\n')
        self.code_text.setMarkdown('```'+code+'```')

    def file_changed(self, cur: QListWidgetItem, prev):
        if self.file_lst_w.currentRow() != 0:
            self.ast = astparser.get_module_ast(Path(cur.text()))
            self.class_lst = astparser.filter_nodes(self.ast, 'class')
            self.func_lst = astparser.filter_nodes(self.ast, 'function')

            self.update_class_lst()
            self.update_func_lst()
            self.update_code()

    def class_changed(self, cur: QListWidgetItem, prev):
        pass

    def func_changed(self, cur: QListWidgetItem, prev):
        cur_idx = self.func_lst_w.currentRow()
        # print(self.func_lst, ))
        if cur_idx == 0:
            return 
        else:
            cur_idx -= 1
            func = self.func_lst[cur_idx]
            print(func)
            print(self.code_lines)
            start = func['lineno']
            end = func['end_lineno'] + 1
            code = '\n'.join(self.code_lines[start - 1 : end])
            print('*'*80)
            print(code)
            print('*'*80)
            print('```\n '+code+'\n ```')
            self.code_text.setMarkdown('```\n '+code+'\n ```')
            print(self.code_text.toMarkdown())

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
