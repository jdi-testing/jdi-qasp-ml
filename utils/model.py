import torch
from .config import logger


class JDIModel(torch.nn.Module):
    def __init__(self, in_features, out_features):
        super(JDIModel, self).__init__()
        logger.info(
            f'IN_FEATURES: {in_features}, OUT_FEATURES: {out_features}')

        self.input_layer = torch.nn.Linear(in_features=in_features, out_features=128, bias=False)
        self.batchNorm1 = torch.nn.LayerNorm(normalized_shape=[self.input_layer.out_features])
        self.leaky_relu1 = torch.nn.LeakyReLU(0.1, inplace=True)
        self.hidden1 = torch.nn.Linear(in_features=self.input_layer.out_features, out_features=32, bias=False)
        self.batchNorm2 = torch.nn.LayerNorm(normalized_shape=[self.hidden1.out_features])
        self.leaky_relu2 = torch.nn.LeakyReLU(0.1, inplace=True)
        self.hidden2 = torch.nn.Linear(in_features=self.hidden1.out_features, out_features=out_features, bias=True)

    def forward(self, x):
        x = self.input_layer(x)
        x = self.batchNorm1(x)
        x = self.leaky_relu1(x)
        x = self.hidden1(x)
        x = self.batchNorm2(x)
        x = self.leaky_relu2(x)
        x = self.hidden2(x)  # logits

        return x
