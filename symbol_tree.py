from pathlib import Path

import astparser

STATE = {}

def nodelist_to_lst(node_list):
    return [x['name'] for x in node_list]

def set_active_file(file_path: str):
    '''
    Set active file and return changed UI state
    '''
    if file_path == '.':
        return {}
    else:
        STATE['module'] = file_path
        STATE['ast'] = astparser.get_module_ast(Path(file_path))
        STATE['class_lst'] = astparser.filter_nodes(STATE['ast'], 'class')
        STATE['func_lst'] = astparser.filter_nodes(STATE['ast'], 'function')
        STATE['code_lines'] = Path(file_path).read_text().split('\n')

        code = '\n'.join(STATE['code_lines'])

        return {'class_lst': nodelist_to_lst(STATE['class_lst']), 
                'func_lst': nodelist_to_lst(STATE['func_lst']),
                'code': code}

def set_active_class(cls_idx: int):
    '''
    set active class and return changed UI state
    '''
    if cls_idx == 0:
        STATE['func_lst'] = astparser.filter_nodes(STATE['ast'], 'function')
        code = '\n'.join(STATE['code_lines'])
    else:
        cls_idx -= 1
        active_class = STATE['class_lst'][cls_idx]
        STATE['func_lst'] = astparser.filter_nodes(active_class, 'function')

        start = active_class['lineno'] - 1
        end = active_class['end_lineno'] + 1
        code = '\n'.join(STATE['code_lines'][start : end])
    return {'func_lst': nodelist_to_lst(STATE['func_lst']), 'code': code}

def set_active_func(func_idx: int):
    '''
    set active function and return changed UI state
    '''
    if func_idx == 0:
        code = '\n'.join(STATE['code_lines'])
    else:
        func_idx -= 1
        active_func = STATE['func_lst'][func_idx]

        start = active_func['lineno'] - 1
        end = active_func['end_lineno'] + 1
        code = '\n'.join(STATE['code_lines'][start : end])
    return {'code': code}

