'''
Node and Tree data structure implementation for storing AST information
'''
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Node:
    name : str
    classes : List['Node']  
    functions : List['Node']
    parent : Optional['Node'] = None
    type :str = 'node'
    start_line_no : int = 0
    end_line_no : int = -1
    doc : str = ''

    def __hash__(self):
        t = (self.type, self.name)
        return hash(t)

    def __repr__(self):
        return f'''
        name: {self.name}
        parent: {self.parent.name if self.parent else ''}
        classes: {self.classes}
        functions: {self.functions}
        '''

    def get_classes_recursive(self):
        cls = self.classes

        for c in self.classes:
            cls += c.get_classes_recursive()

        for c in self.functions:
            cls += c.get_classes_recursive()

        return cls

    def get_functions_recursive(self):
        funcs = self.functions

        for c in self.classes:
            funcs += c.get_functions_recursive()

        for c in self.functions:
            funcs += c.get_functions_recursive()

        return funcs

class ModuleNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'module'
        self.code_lines = []

class ClassNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'class'

class FunctionNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'function'

