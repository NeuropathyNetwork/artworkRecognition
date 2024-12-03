from torchvision.models import efficientnet_b3, EfficientNet_B3_Weights
import glob

import os
import shutil
import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Variable
from torchvision.models import efficientnet_b3, EfficientNet_B3_Weights

# Use weights instead of pretrained model
from torchvision import transforms, utils
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import torch.optim as optim
from torch.optim import lr_scheduler
import time
import copy
# import IBN_ResNet as ibn
from torch.autograd import Variable
from torch.backends import cudnn


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.base = efficientnet_b3(pretrained=True)
        self._avg_pooling = nn.AdaptiveAvgPool2d(1)
        self._max_pooling = nn.AdaptiveMaxPool2d(1)
        num_ftrs = self.base.classifier[1].in_features
        self.reduce_layer = nn.Conv2d(num_ftrs * 2, 512, 1)  # b3 num_ftrs=1536
        self._dropout = nn.Dropout(0.3)
        self._fc = nn.Linear(512, 49)

    def forward(self, x):
        x = self.base.extract_features(x)
        x1 = self._avg_pooling(x)
        x2 = self._max_pooling(x)
        x = torch.cat([x1, x2], dim=1)
        x = self.reduce_layer(x)
        x = x.flatten(start_dim=1)
        x = self._dropout(x)
        x = self._fc(x)
        return x


def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Is CUDA available: ", torch.cuda.is_available())
    print("CUDA device count: ", torch.cuda.device_count())
    print(device)
    model = efficientnet_b3(weights=EfficientNet_B3_Weights.IMAGENET1K_V1)
    num_trs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_trs, 49)
    model = model.to(device)
    pth = 'static\\resnet.pth'
    model.load_state_dict(torch.load(pth, weights_only=True, map_location=torch.device('cpu')))
    return model
