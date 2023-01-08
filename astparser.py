import ast
from pathlib import Path
import json
from typing import List

import node_tree as nt

def get_file_list(root = Path('.')) -> List[Path]:
    files = sorted(root.glob('**/*.py'))
    print(files)
    return files 

def get_docstring(elem) -> str:
    try:
        return ast.get_docstring(elem) 
    except:
        return ''

def traverse_tree(tree) -> nt.Node:
    if type(tree) == ast.ClassDef:
        # out = {'type': 'class', 'name': tree.name, 'lineno': tree.lineno, 
        #        'end_lineno': tree.end_lineno}
        out = nt.ClassNode(tree.name, [], [], start_line_no = tree.lineno, 
                           end_line_no = tree.end_lineno)
    elif type(tree) == ast.FunctionDef:
        # out = {'type': 'function', 'name': tree.name, 'lineno': tree.lineno, 
        #        'end_lineno': tree.end_lineno}
        out = nt.FunctionNode(tree.name, [], [], start_line_no = tree.lineno, 
                           end_line_no = tree.end_lineno)
    else:
        # out = {'type': str(type('tree'))}
        out = nt.Node(str(type(tree)), [], [])
    
    # out['doc'] = get_docstring(tree)
    out.doc = get_docstring(tree)
    
    try:
        child = [traverse_tree(x) for x in tree.body]
    except Exception as e:
        child = []
#         print('child except', e)
    for c in child:
        if type(c) == nt.ClassNode:
            out.classes.append(c)
        elif type(c) == nt.FunctionNode:
            out.functions.append(c)
        c.parent = out
    
    return out

def get_module_node(module_path: Path) -> nt.ModuleNode:
    '''
    get module ast for given python file
    '''
    raw_tree = module_path.read_text()
    tree = ast.parse(raw_tree)
    out = traverse_tree(tree)
    mod = nt.ModuleNode(str(module_path), out.classes, out.functions, doc = out.doc)
    mod.code_lines = raw_tree.split('\n')
    # out['type'] = 'module'
    # out['name'] = str(module_path)
    # out['doc'] = ''
    return mod

def filter_nodes(root: nt.Node, type_str: str) -> List[nt.Node]:
    '''
    find nodes with type `type_str`
    '''
    # try:
    #     out = [x for x in root['children'] if x['type'] == type_str ]
    #     for c in root['children']:
    #         out += filter_nodes(c, type_str)
    #     return out
    # except:
    #     return []
    if type_str == 'class':
        return root.get_classes_recursive()
    elif type_str == 'function':
        return root.get_functions_recursive()
    else:
        return []
