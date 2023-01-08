'''
Main library
'''
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

import astparser
import node_tree as nt

STATE = {}

class Message(Enum):
    FILE_SELECTED = 1
    CLASS_SELECTED = 2
    FUNCTION_SELECTED = 3

@dataclass
class Model:
    root: Path
    ast: nt.Node | None
    
    file_list: List[Path]
    selected_file_idx: int
    
    class_list: List[nt.Node]
    selected_class_idx: int
    
    function_list: List[nt.Node]
    selected_function_idx: int

    code: str

def init(root: Path | str) -> Model:
    root = Path(root)
    files = sorted(root.glob('**/*.py'))
    
    model = Model(root, None, files, -1, [], -1, [], -1, '')
    return model

def update(model: Model, message: Tuple) -> Model:
    msg, idx = message
    match msg:
        case Message.FILE_SELECTED:
            return get_file_details(model, idx)
        case Message.CLASS_SELECTED:
            return get_class_details(model, idx)
        case Message.FUNCTION_SELECTED:
            return get_function_details(model, idx)

def get_file_details(model: Model, idx: int) -> Model:
    model.selected_function_idx = -1
    model.selected_class_idx = -1
    if idx == 0:
        model.selected_file_idx = 0
        return model
    else:
        model.selected_file_idx = idx
        idx -= 1
        file_path = model.file_list[idx]
        root = astparser.get_module_node(file_path)
        model.ast = root
        model.class_list = root.get_classes_recursive()
        model.function_list = root.get_functions_recursive()
        model.code = '\n'.join(root.code_lines)
        return model

def get_class_details(model: Model, idx: int) -> Model:
    model.selected_function_idx = -1
    if idx == 0:
        model.selected_class_idx = 0
    else:
        model.selected_class_idx = idx
        idx -= 1
        cls = model.class_list[idx]
        print('current class', cls, cls.start_line_no, cls.end_line_no)
        model.function_list = cls.get_functions_recursive()
        model.code = '\n'.join(
                model.ast.code_lines[
                    cls.start_line_no - 2 : cls.end_line_no + 1
                    ]
                )
    return model

def get_function_details(model : Model, idx: int) -> Model:
    if idx == 0:
        model.selected_function_idx = 0
    else:
        model.selected_function_idx = idx
        idx -= 1
        func = model.function_list[idx]
        print('current function', func, func.start_line_no, func.end_line_no)
        model.code = '\n'.join(
                model.ast.code_lines[
                    func.start_line_no - 2 : func.end_line_no + 1
                    ]
                )

    return model
