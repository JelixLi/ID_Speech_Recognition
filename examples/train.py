import _init_path
from models.conv import GatedConv
import json


# model = GatedConv.load("pretrained/gated-conv.pth")

# model.to_train()

# model.fit("train.manifest", "train.manifest")

with open("data_aishell/labels.json") as f:
    vocabulary = json.load(f)
    vocabulary = "".join(vocabulary)
model = GatedConv(vocabulary)

model.to_train()

model.fit("/home/dolan/Desktop/masr/data_aishell/train.index",
            "/home/dolan/Desktop/masr/data_aishell/dev.index",
            "/home/dolan/Desktop/masr/data_aishell/labels.json",
            10)