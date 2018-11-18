import json
import random
import tensorflow as tf
import math
import time
import os
from configparser import ConfigParser
from utils.logger import logger
import numpy as np

currdir = os.path.split(os.path.abspath(__file__))[0]
cfg = ConfigParser()
cfg.read('%s/config/transe.ini' % currdir)
os.environ["CUDA_VISIBLE_DEVICES"] = str(cfg.get('transe', 'gpu'))

class TransE_tf():

    def __init__(self, config, next_batch):
        self.entity_size = config['entity_size']
        self.relation_size = config['relation_size']
        self.dim = config['dim']
        self.batch_size = config['batch_size']
        self.learning_rate = config['learning_rate']
        self.margin = config['margin']
        self.max_epoch = config['max_epoch']
        self.threshold = config['threshold']
        self.snapshot_step = config['snapshot_step']
        self.decay_steps = config['decay_steps']
        self.decay_rate = config['decay_rate']
        self.next_batch = next_batch
        logger.info('init transe, config: %s' % json.dumps(config))

    def train(self):
        with tf.name_scope("embedding"):
            entity_embedding_table = tf.Variable(
                tf.truncated_normal([self.entity_size, self.dim], stddev=6.0 / math.sqrt(self.dim)))
            # entity_embedding_table = entity_embedding_table / tf.norm(entity_embedding_table, axis=1, keepdims=True)
            relation_embedding_table = tf.Variable(
                tf.truncated_normal([self.relation_size, self.dim], stddev=6.0 / math.sqrt(self.dim)))
            # relation_embedding_table = relation_embedding_table / tf.norm(relation_embedding_table, axis=1, keepdims=True)

            triples = tf.placeholder(tf.int32, shape=[self.batch_size, 3], name="triples")
            corrupted_triples = tf.placeholder(tf.int32, shape=[self.batch_size, 3], name="corrupted_triples")

        with tf.name_scope("lookup"):
            head_embedding = tf.nn.embedding_lookup(entity_embedding_table, triples[:, 0])
            tail_embedding = tf.nn.embedding_lookup(entity_embedding_table, triples[:, 2])
            relation_embedding = tf.nn.embedding_lookup(relation_embedding_table, triples[:, 1])
            corrupted_head_embedding = tf.nn.embedding_lookup(entity_embedding_table, corrupted_triples[:, 0])
            corrupted_tail_embedding = tf.nn.embedding_lookup(entity_embedding_table, corrupted_triples[:, 2])

        with tf.name_scope("loss"):
            loss = self.calc_loss(head_embedding, relation_embedding, tail_embedding, corrupted_head_embedding, corrupted_tail_embedding)
            global_step = tf.placeholder(dtype=tf.int32)
            learning_rate = tf.train.exponential_decay(self.learning_rate, global_step, self.decay_steps, self.decay_rate, staircase=True)
            # optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(loss)
            optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

            new_entity_embedding_table = entity_embedding_table / tf.norm(entity_embedding_table, axis=1, keepdims=True)
            update_entity_embedding_table = tf.assign(entity_embedding_table, new_entity_embedding_table)
            new_relation_embedding_table = relation_embedding_table / tf.norm(relation_embedding_table, axis=1, keepdims=True)
            update_relation_embedding_table = tf.assign(relation_embedding_table, new_relation_embedding_table)

            tf.summary.scalar(name=loss.op.name, tensor=loss)
            merge = tf.summary.merge_all()

        init = tf.global_variables_initializer()
        with tf.Session(config=tf.ConfigProto(log_device_placement=False)) as sess:
            sess.run(init)
            summary_writer = tf.summary.FileWriter(logdir="./transE_all_sumary_normal/", graph=sess.graph)
            sess.run(update_relation_embedding_table)
            for step in range(self.max_epoch):
                triple_ids, corrupted_triple_ids = self.next_batch(self.batch_size)
                sess.run(update_entity_embedding_table)
                r, _, summary = sess.run([loss, optimizer, merge], feed_dict={triples: triple_ids, corrupted_triples: corrupted_triple_ids, global_step: step})
                if step % 50 == 0:
                    summary_writer.add_summary(summary, step)
                if step % 1000 == 0:
                    print('step %d, loss = %s, %s' % (step, r, time.asctime()))
                    logger.info('step %d, loss = %s' % (step, r))
                if step % self.snapshot_step == 0:
                    self.snapshot(step, entity_embedding_table, relation_embedding_table)
                if (r < self.threshold and r != 0):
                    print('step %d, loss = %s' % (step, r))
                    logger.info('step %d, loss = %s' % (step, r))
                    self.snapshot(step, entity_embedding_table, relation_embedding_table)
                    break

    def snapshot(self, step, entity_embedding_table, relation_embedding_table):
        np.savetxt('%s/snapshot/entity_embedding_table_%s.txt' % (currdir, str(step)), entity_embedding_table.eval())
        np.savetxt('%s/snapshot/relation_embedding_table_%s.txt' % (currdir, str(step)), relation_embedding_table.eval())

    def calc_loss(self, h, l, t, h_c, t_c):
        return tf.reduce_sum(
            tf.nn.relu(self.margin + self.L2_norm(h, l, t) - self.L2_norm(h_c, l, t_c))
        )

    def L2_norm(self, h, l, t):
        return tf.norm(h+l-t, axis=1)

def run(triples, entities, relations, triple_idc):
    def next_batch(batch_size):
        batch_size = min(len(triples), batch_size)
        triple_ids = random.sample(triples, batch_size)
        corrupted_triple_ids = []
        if random.randint(0, 1) == 0:
            for triple_id in triple_ids:
                ctriple = [random.randint(0, len(entities) - 1), triple_id[1], triple_id[2]]
                while '%dc%dc%d' % (ctriple[0], ctriple[1], ctriple[2]) in triple_idc:
                    ctriple = [random.randint(0, len(entities) - 1), triple_id[1], triple_id[2]]
                corrupted_triple_ids.append(ctriple)
        else:
            for triple_id in triple_ids:
                ctriple = [triple_id[0], triple_id[1], random.randint(0, len(entities) - 1)]
                while '%dc%dc%d' % (ctriple[0], ctriple[1], ctriple[2]) in triple_idc:
                    ctriple = [random.randint(0, len(entities) - 1), triple_id[1], triple_id[2]]
                corrupted_triple_ids.append(ctriple)
        return triple_ids, corrupted_triple_ids

    config = {
        'dim': int(cfg.get('transe', 'dim')),
        'batch_size': int(cfg.get('transe', 'batch_size')),
        'learning_rate': float(cfg.get('transe', 'learning_rate')),
        'margin': float(cfg.get('transe', 'margin')),
        'max_epoch': int(cfg.get('transe', 'max_epoch')),
        'threshold': float(cfg.get('transe', 'threshold')),
        'snapshot_step': int(cfg.get('transe', 'snapshot_step')),
        'decay_steps': int(cfg.get('transe', 'decay_steps')),
        'decay_rate': float(cfg.get('transe', 'decay_rate')),
        'entity_size': len(entities),
        'relation_size': len(relations)
    }
    transE_tf = TransE_tf(config, next_batch)
    transE_tf.train()


def get_triples_from_json():
    with open('%s/data/triples.json' % currdir, 'r') as f:
        triples = json.load(f)
    with open('%s/data/entities.json' % currdir, 'r') as f:
        entities = json.load(f)
    with open('%s/data/relations.json' % currdir, 'r') as f:
        relations = json.load(f)
    with open('%s/data/triple_idc.json' % currdir, 'r') as f:
        triple_idc = json.load(f)
    return triples, entities, relations, triple_idc


if __name__ == '__main__':
    triples, entities, relations, triple_idc = get_triples_from_json()
    run(triples, entities, relations, triple_idc)