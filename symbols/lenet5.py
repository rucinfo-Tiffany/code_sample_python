# coding=utf-8
from __future__ import print_function
from __future__ import print_function

'''
MXNet 101 - Lenet5
'''
import os, gzip, struct
import logging
import numpy as np
import mxnet as mx
logging.basicConfig(level=logging.DEBUG)
BATCH_SIZE = 100
DATA_PATH = '/mnt/cephfs/lab/zhangyaxuan/myData'
MODEL_PATH = '/mnt/cephfs/lab/zhangyaxuan/model'
NUM_BATCH = 3

def get_mnist_iter(batch_size):
    """
    create data iterator with NDArrayIter
    """
    mnist = mx.test_utils.get_mnist()
    train = mx.io.NDArrayIter(mnist['train_data'], mnist['train_label'], batch_size, shuffle=True)
    val = mx.io.NDArrayIter(mnist['test_data'], mnist['test_label'], batch_size)
    return (train, val)


def lenet5():
    """Lenet5 model"""
    # input
    data = mx.symbol.Variable('data')
    # C1
    conv1 = mx.symbol.Convolution(data=data, kernel=(5,5), num_filter=20)
    relu1 = mx.symbol.Activation(data=conv1, act_type="relu")

    # S2: max_pooling
    pool1 = mx.symbol.Pooling(data=relu1, pool_type="max",
                              kernel=(2,2), stride=(2,2))
    # C3
    conv2 = mx.symbol.Convolution(data=pool1, kernel=(5,5), num_filter=50)
    relu2 = mx.symbol.Activation(data=conv2, act_type="relu")

    # S4: max_pooling
    pool2 = mx.symbol.Pooling(data=relu2, pool_type="max",
                              kernel=(2,2), stride=(2,2))
    # C5: flatten
    flatten = mx.symbol.Flatten(data=pool2)
    fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=500)
    relu3 = mx.symbol.Activation(data=fc1, act_type="relu")

    # F6: Full connection
    fc2 = mx.symbol.FullyConnected(data=relu3, num_hidden=10)

    # Output
    lenet = mx.symbol.SoftmaxOutput(data=fc2, name='softmax')
    return lenet

def get_confusion_metrics(label, prediction):
    labelSet = [int(x) for x in sorted(set(label))]
    num_case = len(label)
    num = len(labelSet)
    tp, tn, fp, fn = np.zeros(num), np.zeros(num), np.zeros(num), np.zeros(num)
    for idx, lb in enumerate(labelSet):
        pred = [np.where(x==max(x))[0][0] for x in prediction]
        label = label.astype(int)
        tp[idx] = sum([label[i] == lb and pred[i] == lb for i in range(num_case)])
        fp[idx] = sum([label[i] != lb and pred[i] == lb for i in range(num_case)])
        fn[idx] = sum([label[i] == lb and pred[i] != lb for i in range(num_case)])
        tn[idx] = sum([label[i] != lb and pred[i] != lb for i in range(num_case)])
    return (tp, fp, fn, tn)

def precision(label, pred):
    (tp, fp, fn, tn) = get_confusion_metrics(label, pred)
    return tp * 1.0 / (tp + fp)

def recall(label, pred):
    (tp, fp, fn, tn) = get_confusion_metrics(label, pred)
    return np.mean(tp * 1.0 / (tp + fn))

def f_score(label, pred):
    precision, recall = precision_func(label, pred), recall_func(label, pred)
    return 2 * precision * recall / (precision + recall)

if __name__ == '__main__':
    logging.info('Starting loading data...')
    # load data
    train, val = get_mnist_iter(batch_size=BATCH_SIZE)
    # ctx = mx.gpu() if mx.test_utils.list_gpus() else mx.cpu()
    ctx = mx.cpu()  # test, cpu only

    logging.info('Starting loading model...')
    # load lenet5 model
    lenet = lenet5()
    lenet_model = mx.mod.Module(symbol=lenet, context=ctx)

    # train model with validation data
    lr_factor = 0.1
    steps = [10000,15000] # in iterations
    lr_scheduler = mx.lr_scheduler.MultiFactorScheduler(step=steps, factor=lr_factor)
    optimizer_params = {'learning_rate': 0.01,
                        'wd': 0.0005,
                        'lr_scheduler': lr_scheduler,
                        'momentum': 0.9}
    save_model_prefix = os.path.join(MODEL_PATH, 'my_model')
    rank = 0 # indicate worker id, unused in single-machine training
    checkpoint = mx.callback.do_checkpoint(save_model_prefix, rank)
    logging.info('Starting training model...')
    lenet_model.fit(train,
            eval_data=val,
            optimizer='sgd',
            optimizer_params=optimizer_params,
            epoch_end_callback=[checkpoint],
            eval_metric=[
                'acc',
                mx.metric.create(recall)],
            num_epoch=5)

    # evaluation
    lenet_model.predict(val).asnumpy()
    print(lenet_model.score(val, mx.metric.create('acc')))
    print(lenet_model.score(val, mx.metric.create(recall)))
