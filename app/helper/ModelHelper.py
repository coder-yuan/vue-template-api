#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  
# @Author   :  jackeroo
# @Time     :  2019/11/20 上午9:58
# @File     :  ModelHelper.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
from sqlalchemy.orm import class_mapper


def model_to_dict(obj, handle_relationship_flag=False, visited_children=None, back_relationships=None):
    """
    将Sqlalchemy对象处理成字典，便于Json序列化
    :param obj: Model对象
    :param visited_children:
    :param back_relationships:       
    :param handle_relationship_flag: 是否处理relationship
    :return:
    """
    if visited_children is None:
        visited_children = set()
    if back_relationships is None:
        back_relationships = set()

    # 字典化一般Column对象
    serialized_data = {c.key: getattr(obj, c.key) for c in obj.__table__.columns}

    # relationship Model对象的处理，根据handle_relationship_flag控制
    # 默认不处理
    if handle_relationship_flag:
        relationships = class_mapper(obj.__class__).relationships
        visitable_relationships = [(name, rel) for name, rel in relationships.items() if name not in back_relationships]
        for name, relation in visitable_relationships:
            if relation.backref:
                back_relationships.add(relation.backref)
            relationship_children = getattr(obj, name)
            if relationship_children is not None:
                if relation.uselist:
                    children = []
                    for child in [c for c in relationship_children if c not in visited_children]:
                        visited_children.add(child)
                        children.append(
                            model_to_dict(child, handle_relationship_flag, visited_children, back_relationships))
                    serialized_data[name] = children
                else:
                    serialized_data[name] = model_to_dict(relationship_children, handle_relationship_flag,
                                                          visited_children, back_relationships)
    return serialized_data


def pagination_to_dict(pagination_obj, handle_relationship_flag=False, visited_children=None, back_relationships=None):
    """
    将Sqlalchemy分页展示数据转化为字典，以便序列化
    """

    pagination_dict = {}

    if pagination_obj is not None:
        pagination_dict = {
            'page': pagination_obj.page,
            'pages': pagination_obj.pages,
            'items': [model_to_dict(item, handle_relationship_flag, visited_children, back_relationships) for item in
                      pagination_obj.items],
            'pageSize': pagination_obj.per_page,
            'total': pagination_obj.total
        }

    return pagination_dict
