import numpy as np
from py2neo import Graph, NodeMatcher, RelationshipMatcher
from configparser import ConfigParser
import os
import json

currdir = os.path.split(os.path.abspath(__file__))[0]

class NeoUtil():

    def __init__(self):
        cfg = ConfigParser()
        cfg.read('%s/../config/neo4j.ini' % currdir)
        uri = cfg.get('db', 'uri')
        username = cfg.get('db', 'username')
        password = cfg.get('db', 'password')
        self.graph = Graph(uri=uri, auth=(username, password))
        self.matcher = NodeMatcher(self.graph)
        self.relation_matcher = RelationshipMatcher(self.graph)

    def write_triples_to_json(self):
        triples, entities, relations, triple_idc = self.get_all_triple_ids()

        with open('%s/../data/triples.json' % currdir, 'w') as f:
            f.write(json.dumps(triples))
        with open('%s/../data/entities.json' % currdir, 'w') as f:
            f.write(json.dumps(entities))
        with open('%s/../data/relations.json' % currdir, 'w') as f:
            f.write(json.dumps(relations))
        with open('%s/../data/triple_idc.json' % currdir, 'w') as f:
            f.write(json.dumps(triple_idc))

    # match (node)-[]->(rnode) return (rnode)
    def get_related_to_nodes(self, start_node):
        relations = self.relation_matcher.match([start_node])
        end_nodes = []
        for relation in relations:
            end_nodes.append(relation.nodes[1])
        return end_nodes

    # match (node)<-[]-(rnode) return (rnode)
    def get_related_from_nodes(self, end_node):
        relations = self.relation_matcher.match([None, end_node])
        start_nodes = []
        for relation in relations:
            start_nodes.append(relation.nodes[0])
        return start_nodes

    # match (node)-[]-(rnoode) return (rnode)
    def get_related_nodes(self, node):
        nodes = self.get_related_to_nodes(node)
        nodes.extend(self.get_related_from_nodes(node))
        return nodes
    '''
    node1_re -> [1, 2, 3]
    node2_re -> [2, 3, 4]
    return:
        list1 = [1, 1, 1, 0]
        list2 = [0, 1, 1, 1]
        id_set = (1, 2, 3, 4)
    '''
    def get_related_list(self, node1, node2):
        node1_re = self.get_related_nodes(node1)
        node2_re = self.get_related_nodes(node2)
        id_set = set()
        # id_set.add(node1.identity)
        # id_set.add(node2.identity)
        node1_id_obj = {}
        node2_id_obj = {}
        for node in node1_re:
            id_set.add(node.identity)
            node1_id_obj[node.identity] = 1
        for node in node2_re:
            id_set.add(node.identity)
            node2_id_obj[node.identity] = 1
        list1 = []
        list2 = []
        for id in id_set:
            list1.append(int(id in node1_id_obj))
            list2.append(int(id in node2_id_obj))
        return [list1, list2, id_set]

    def calc_dist(self, node1, node2):
        [list1, list2, ids] = self.get_related_list(node1, node2)
        return np.linalg.norm(np.array(list1) - np.array(list2))

    '''
    获取所有的triple， entity_id, relation_name    
    '''
    def get_all_triples(self):
        entity_id_set = set()
        relation_name_set = set()
        triple_list = []
        relations = self.relation_matcher.match()
        for relation in relations:
            start_node_id = relation.start_node.identity
            end_node_id = relation.end_node.identity
            relation_name = type(relation).__name__
            start_label = str(relation.start_node.labels).split(':')[1]
            end_label = str(relation.end_node.labels).split(':')[1]
            relation_name = '%s-%s-%s' % (start_label, relation_name, end_label)
            entity_id_set.add(start_node_id)
            entity_id_set.add(end_node_id)
            relation_name_set.add(relation_name)
            triple_list.append([start_node_id, relation_name, end_node_id])
        return triple_list, list(entity_id_set), list(relation_name_set)

    def get_all_triple_ids(self):
        triple_list, entity_list, relatioin_list = self.get_all_triples()
        entity_id_obj = {}
        relation_id_obj = {}
        triple_id_list = []
        triple_idc_obj = {}
        for idx in range(len(entity_list)):
            entity_id_obj[entity_list[idx]] = idx
        for idx in range(len(relatioin_list)):
            relation_id_obj[relatioin_list[idx]] = idx
        for [head, relation, tail] in triple_list:
            triple_id_list.append([entity_id_obj[head], relation_id_obj[relation], entity_id_obj[tail]])
            triple_idc_obj['%dc%dc%d' % (entity_id_obj[head], relation_id_obj[relation], entity_id_obj[tail])] = 1
        return triple_id_list, entity_id_obj, relation_id_obj, triple_idc_obj

if __name__ == '__main__':
    u = NeoUtil()
    # u.write_triples_to_json()

    u.write_triples_to_json()
    # cur = u.graph.run('match (n)-[m]-() return m')
    # if cur.forward():
    #     r = cur.current['m']
    #     print(dir(r))
    #     print(r.start_node)
    #     # print(r.relationships.labels)
    #     print(r.start_node.labels)


