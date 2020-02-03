# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object, UserTypeError

class Inspect(Object) :

    def __init__(self, raw_data) :
        Object.__init__(self)
        self._registerProperty(['raw_data', 'field_path_list'])
        if not isinstance(raw_data, (List, Dict)) :
            raise UserTypeError(raw_data)
        self._raw_data = raw_data
        self._field_path_list = List()
        self._field_path_list = self._inspect(self._raw_data).field_path_list

    # 返回拉平后的字段tuple的列表，统计字段类型和可能的取值，数组长度，存在性检验
    def _inspect(self, data) :
        def prepend_path_list(field, path_list) :
            return List(tuple(List(list(path)).prepended(field)) for path in path_list)

        result = Dict(
            field_path_list = List()
        )
        if isinstance(data, Dict) :
            for key, value in data.items() :
                if isinstance(value, (List, Dict)) :
                    res = self._inspect(value)
                    result.field_path_list.extend(prepend_path_list(key, res.field_path_list))
                else :
                    result.field_path_list.append(tuple([key]))
        elif isinstance(data, List) :
            for index, item in data.enum() :
                if isinstance(item, (List, Dict)) :
                    res = self._inspect(item)
                    result.field_path_list.extend(prepend_path_list('#', res.field_path_list))
                else :
                    result.field_path_list.append(tuple(['#']))
        result.field_path_list.unique().sort()
        return result





# DataStructure Module
#   def inspect()
#   def compatibleTo
#   def validate
#   def difference/delta


# # move
# def inspect(data, max_depth = 10, depth = 0) :
# https://docs.python.org/3/library/reprlib.html
#     # print(str(data)[:120])
#     if depth > max_depth :
#         if data is None : return None 
#         elif isinstance(data, (str, int, float, bool, tuple, set)) : return data
#         elif isinstance(data, list) : return '[ {} items folded ]'.format(len(data))
#         elif isinstance(data, dict) : return '{{ {} keys folded }}'.format(len(data))
#         else : raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])
#     if data is None : return None
#     elif isinstance(data, (str, int, float, bool, tuple, set)) : return data
#     elif isinstance(data, list) :
#         if len(data) == 0 : return data
#         elif len(data) == 1 : return List([ inspect(data[0], max_depth, depth + 1) ])
#         elif len(data) == 2 : return List([ inspect(data[0], max_depth, depth + 1), inspect(data[1], max_depth, depth + 1) ])
        
#         # len >= 3
#         result_0 = inspect(data[0], max_depth, depth + 1)
#         _ = '------------------------------'
#         if isinstance(result_0, dict) :
#             for index, datum_i in enumerate(data) :
#                 if not isinstance(datum_i, dict) : raise Exception('列表中元素类型不一致({})'.format(datum_i))
#                 for key, value in datum_i.items() :
#                     if key not in result_0 :
#                         result_0[key] = inspect(value, max_depth, depth + 1) # 【补充】第0个元素中不存在的字段
#                         continue
#                     if data[0].get(key) is not None and isinstance(data[0][key], list) : continue # 列表类【原生】字段不扩充POSSIBLE VALUES
#                     if data[0].get(key) is not None and isinstance(data[0][key], dict) : continue # 字典类【原生】字段不扩充POSSIBLE VALUES
#                     if data[0].get(key) is None and isinstance(result_0[key], list)
#                         and not (isinstance(result_0[key][0], str) and 'POSSIBLE VALUES' in result_0[key][0]) : continue # 列表类【补充】字段不扩充POSSIBLE VALUES
#                     if data[0].get(key) is None and isinstance(result_0[key], dict) : continue # 字典类【补充】字段不扩充POSSIBLE VALUES
#                     # 此时待补充的是非列表字典类字段
#                     if isinstance(value, list) or isinstance(value, dict) : raise Exception('列表中元素类型不一致({})'.format(value))
#                     # 此时value一定为非列表字典类数据
#                     if not isinstance(result_0[key], list) : # 暂未扩充过，现进行首次扩充POSSIBLE VALUES
#                         result_0[key] = [
#                             _ + 'POSSIBLE VALUES' + _, 
#                             result_0[key]
#                         ]
#                         if inspect(value, max_depth, depth + 1) != result_0[key][1] :
#                             result_0[key].append(inspect(value, max_depth, depth + 1))
#                     else : # 非首次扩充POSSIBLE VALUES
#                         if len(result_0[key]) < 5 :
#                             if inspect(value, max_depth, depth + 1) not in result_0[key] :
#                                 result_0[key].append(inspect(value, max_depth, depth + 1)) # 扩充
#                         if index == len(data) - 1 :
#                             result_0[key].append('{} TOTAL {} SIMILAR ITEMS {}'.format(_, len(data), _))
#             return [ result_0, '{} TOTAL {} SIMILAR DICTS {}'.format(_, len(data), _) ]
#         else : # 非字典类数据，含列表
#             return [ inspect(data[0], max_depth, depth + 1), inspect(data[1], max_depth, depth + 1), '{} TOTAL {} SIMILAR LISTS {}'.formart(_, len(data), _) ]
#     elif isinstance(data, dict) : return { key : inspect(value, max_depth, depth + 1) for key, value in data.items() }
#     else : raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])


# DataStructure Module
#   def inspect()
#   def compatibleTo
#   def validate
#   def difference/delta

# print(str(data)[:120])
# if depth > max_depth :
#     if data is None : return None 
#     elif isinstance(data, (str, int, float, bool, tuple, set)) : return data
#     elif isinstance(data, list) : return '[ {} items folded ]'.format(len(data))
#     elif isinstance(data, dict) : return '{{ {} keys folded }}'.format(len(data))
#     else : raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])
# if data is None : return None
# elif isinstance(data, (str, int, float, bool, tuple, set)) : return data
# elif isinstance(data, list) :
#     if len(data) == 0 : return data
#     elif len(data) == 1 : return List([ inspect(data[0], max_depth, depth + 1) ])
#     elif len(data) == 2 : return List([ inspect(data[0], max_depth, depth + 1), inspect(data[1], max_depth, depth + 1) ])
    
#     # len >= 3
#     result_0 = inspect(data[0], max_depth, depth + 1)
#     _ = '------------------------------'
#     if isinstance(result_0, dict) :
#         for index, datum_i in enumerate(data) :
#             if not isinstance(datum_i, dict) : raise Exception('列表中元素类型不一致({})'.format(datum_i))
#             for key, value in datum_i.items() :
#                 if key not in result_0 :
#                     result_0[key] = inspect(value, max_depth, depth + 1) # 【补充】第0个元素中不存在的字段
#                     continue
#                 if data[0].get(key) is not None and isinstance(data[0][key], list) : continue # 列表类【原生】字段不扩充POSSIBLE VALUES
#                 if data[0].get(key) is not None and isinstance(data[0][key], dict) : continue # 字典类【原生】字段不扩充POSSIBLE VALUES
#                 if data[0].get(key) is None and isinstance(result_0[key], list)
#                     and not (isinstance(result_0[key][0], str) and 'POSSIBLE VALUES' in result_0[key][0]) : continue # 列表类【补充】字段不扩充POSSIBLE VALUES
#                 if data[0].get(key) is None and isinstance(result_0[key], dict) : continue # 字典类【补充】字段不扩充POSSIBLE VALUES
#                 # 此时待补充的是非列表字典类字段
#                 if isinstance(value, list) or isinstance(value, dict) : raise Exception('列表中元素类型不一致({})'.format(value))
#                 # 此时value一定为非列表字典类数据
#                 if not isinstance(result_0[key], list) : # 暂未扩充过，现进行首次扩充POSSIBLE VALUES
#                     result_0[key] = [
#                         _ + 'POSSIBLE VALUES' + _, 
#                         result_0[key]
#                     ]
#                     if inspect(value, max_depth, depth + 1) != result_0[key][1] :
#                         result_0[key].append(inspect(value, max_depth, depth + 1))
#                 else : # 非首次扩充POSSIBLE VALUES
#                     if len(result_0[key]) < 5 :
#                         if inspect(value, max_depth, depth + 1) not in result_0[key] :
#                             result_0[key].append(inspect(value, max_depth, depth + 1)) # 扩充
#                     if index == len(data) - 1 :
#                         result_0[key].append('{} TOTAL {} SIMILAR ITEMS {}'.format(_, len(data), _))
#         return [ result_0, '{} TOTAL {} SIMILAR DICTS {}'.format(_, len(data), _) ]
#     else : # 非字典类数据，含列表
#         return [ inspect(data[0], max_depth, depth + 1), inspect(data[1], max_depth, depth + 1), '{} TOTAL {} SIMILAR LISTS {}'.formart(_, len(data), _) ]
# elif isinstance(data, dict) : return { key : inspect(value, max_depth, depth + 1) for key, value in data.items() }
# else : raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])