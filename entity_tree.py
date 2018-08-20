# -*- coding: utf-8 -*-
from __future__ import print_function
import math, os, sys, random
import numpy as np

from treelib import Tree
from utils.file_utils import file_read_json, file_read
"""
parsing entity labels with tree model
"""
DEBUG = False

class EntityTree(object):

    def __init__(self):
        self.tree = Tree()

    def create_ent_tree(self, ent_dct, cls_name_map, parent=None, cls_data_map={}):
        '''递归，依据遍历标签间层级关系生成树'''
        tag = ent_dct['LabelName']
        name = cls_name_map.get(tag)
        data = cls_data_map.get(tag, 0)
        if not name:
            print("Error: tag %s not found in cls_name_map!" % tag)
            sys.exit(-1)

        if DEBUG:
            print("# of tree nodes: %d, tree height: %d, # of leaves: %d" % (len(self.tree),
                                                                             self.tree.depth(),
                                                                             len(self.tree.leaves())
                                                                            ))
        nd = self.tree.create_node(tag=name, parent=parent, data=data)
        if 'Subcategory' in ent_dct.keys():
            for dct in ent_dct['Subcategory']:
                self.create_ent_tree(dct, cls_name_map,
                                     parent=nd.identifier,
                                     cls_data_map=cls_data_map)




if __name__ == '__main__':
    ent_dct = file_read_json("openimage/bbox_labels_600_hierarchy.json")
    cls_name = file_read("openimage/class-descriptions-boxable.csv", end=-1, delimiter=",")
    cls_name_map = dict(cls_name)
    cls_name_map['/m/0bl9f'] = 'Entity'
    print(len(cls_name_map.items()))

    tr = EntityTree()
    tr.create_ent_tree(ent_dct, cls_name_map, parent=None, cls_data_map={})
    print("# of tree nodes: %d, tree height: %d, # of leaves: %d" % (len(tr.tree),
                                                                     tr.tree.depth(),
                                                                     len(tr.tree.leaves())
                                                                    ))

    #  统计不同层级tag的个数
    tag_ids = tr.tree.nodes.keys()
    print(len(tag_ids))
    tag_level = [tr.tree.level(idx) for idx in tag_ids]

    for level in sorted(list(set(tag_level))):
        print(level, tag_level.count(level))

    # tr.tree.show()
