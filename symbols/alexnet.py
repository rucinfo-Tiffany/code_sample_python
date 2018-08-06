# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Reference:

Krizhevsky, Alex, Ilya Sutskever, and Geoffrey E. Hinton. "Imagenet classification with deep convolutional neural networks." Advances in neural information processing systems. 2012.
detail structure of each layer reference: https://blog.csdn.net/Chenyukuai6625/article/details/77886795
"""
import mxnet as mx
import numpy as np
from matplotlib.pyplot import imshow
import multiprocessing
import os

mx.random.seed(42) # set seed for repeatability

def plot_mx_array(array):
    assert array.shape[2] == 3, "RGB Channel should be last"
    imshow((array.clip(0, 255)/255).asnumpy())

def create_aug_auto(image):
    # created automatically
    aug_list = mx.image.CreateAugmenter(data_shape=(3, 300, 300), rand_crop=0.5,
            rand_mirror=True, mean=True, brightness=0.125, contrast=0.125,
            saturation=0.125, pca_noise=0.05, inter_method=10)
    aug_image = image.copy()
    for aug in aug_list:
        aug_image = aug(aug_image)
    plot_mx_array(aug_image)

def create_aug_manual(image):
    # created automatically
    aug_list = [mx.image.RandomCropAug(size=(100, 100)),
                mx.image.ColorJitterAug(brightness=1)
                mx.image.HorizontalFlipAug(p=1)]
    aug_image = example_image.copy()
    for aug in aug_list:
        aug_image = aug(aug_image)
    plot_mx_array(aug_image)

def get_image_iter(batch_size):
    """
    create data iterator with NDArrayIter
    """
    mnist = mx.test_utils.get_mnist()
    train = mx.io.NDArrayIter(mnist['train_data'], mnist['train_label'], batch_size, shuffle=True)
    val = mx.io.NDArrayIter(mnist['test_data'], mnist['test_label'], batch_size)
    return (train, val)

def get_symbol(num_classes, dtype='float32', **kwargs):
    input_data = mx.sym.Variable(name="data")
    if dtype == 'float16':
        input_data = mx.sym.Cast(data=input_data, dtype=np.float16)

    # stage 1
    conv1 = mx.sym.Convolution(name='conv1', data=input_data, kernel=(11, 11), stride=(4, 4), num_filter=96)
    relu1 = mx.sym.Activation(data=conv1, act_type="relu")
    lrn1 = mx.sym.LRN(data=relu1, alpha=0.0001, beta=0.75, knorm=2, nsize=5)
    pool1 = mx.sym.Pooling(data=lrn1, pool_type="max", kernel=(3, 3), stride=(2,2))
    # data size now: 27 * 27 * 96

    # stage 2
    conv2 = mx.sym.Convolution(name='conv2',
            data=pool1, kernel=(5, 5), pad=(2, 2), num_filter=256, num_group = 2)
    relu2 = mx.sym.Activation(data=conv2, act_type="relu")
    lrn2 = mx.sym.LRN(data=relu2, alpha=0.0001, beta=0.75, knorm=2, nsize=5)
    pool2 = mx.sym.Pooling(data=lrn2, kernel=(3, 3), stride=(2, 2), pool_type="max")
    # data now: 13 * 13 * 256


    # stage 3
    conv3 = mx.sym.Convolution(name='conv3',
        data=pool2, kernel=(3, 3), pad=(1, 1), num_filter=384)
    relu3 = mx.sym.Activation(data=conv3, act_type="relu")

    # stage 4
    conv4 = mx.sym.Convolution(name='conv4',
        data=relu3, kernel=(3, 3), pad=(1, 1), num_filter=384)
    relu4 = mx.sym.Activation(data=conv4, act_type="relu")

    # stage 5
    conv5 = mx.sym.Convolution(name='conv5', data=relu4, kernel=(3, 3), pad=(1, 1), num_filter=256)
    relu5 = mx.sym.Activation(data=conv5, act_type="relu")
    pool3 = mx.sym.Pooling(data=relu5, kernel=(3, 3), stride=(2, 2), pool_type="max")
    # data now: 6 * 6 * 256

    # stage 6
    flatten = mx.sym.Flatten(data=pool3)
    fc1 = mx.sym.FullyConnected(name='fc1', data=flatten, num_hidden=4096)
    relu6 = mx.sym.Activation(data=fc1, act_type="relu")
    dropout1 = mx.sym.Dropout(data=relu6, p=0.5)

    # stage 7
    fc2 = mx.sym.FullyConnected(name='fc2', data=dropout1, num_hidden=4096)
    relu7 = mx.sym.Activation(data=fc2, act_type="relu")
    dropout2 = mx.sym.Dropout(data=relu7, p=0.5)

    # stage 8
    fc3 = mx.sym.FullyConnected(name='fc3', data=dropout2, num_hidden=num_classes)

    # output layer
    if dtype == 'float16':
        fc3 = mx.sym.Cast(data=fc3, dtype=np.float32)
    softmax = mx.sym.SoftmaxOutput(data=fc3, name='softmax')
    return softmax

if __name__ = "__main__":
    image_dir = os.path.join("data", "images")
    mx.test_utils.download('https://raw.githubusercontent.com/dmlc/web-data/master/mxnet/doc/tutorials/data_aug/inputs/0.jpg', dirname=image_dir)
    example_image = mx.image.imread(os.path.join(image_dir,"0.jpg")).astype("float32")
    plot_mx_array(example_image)
