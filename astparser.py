import ast
from pathlib import Path
import json
from typing import List

def get_file_list(root = Path('.')) -> List[Path]:
    files = sorted(root.glob('**/*.py'))
    print(files)
    return files 

def get_docstring(elem):
    try:
        return ast.get_docstring(elem) 
    except:
        return ''

def traverse_tree(tree):
    if type(tree) == ast.ClassDef:
        out = {'type': 'class', 'name': tree.name, 'lineno': tree.lineno, 
               'end_lineno': tree.end_lineno}
    elif type(tree) == ast.FunctionDef:
        out = {'type': 'function', 'name': tree.name, 'lineno': tree.lineno, 
               'end_lineno': tree.end_lineno}
    else:
        out = {'type': str(type('tree'))}
    
    out['doc'] = get_docstring(tree)
    
    try:
        child = [traverse_tree(x) for x in tree.body]
    except Exception as e:
        child = []
#         print('child except', e)
    out['children'] = child
    return out

def get_module_ast(module_path: Path):
    '''
    get module ast for given python file
    '''
    raw_tree = module_path.read_text()
    tree = ast.parse(raw_tree)
    out = traverse_tree(tree)
    out['type'] = 'module'
    out['name'] = str(module_path)
    out['doc'] = ''
    return out

def filter_nodes(root, type_str):
    '''
    find nodes with type `type_str`
    '''
    try:
        out = [x for x in root['children'] if x['type'] == type_str ]
        for c in root['children']:
            out += filter_nodes(c, type_str)
        return out
    except:
        return []
