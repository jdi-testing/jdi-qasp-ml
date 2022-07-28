import torch
from utils.config import logger


class JDIModel(torch.nn.Module):
    def __init__(self, in_features, out_features, n2):
        super(JDIModel, self).__init__()
        logger.info(f"IN_FEATURES: {in_features}, OUT_FEATURES: {out_features}")

        self.input_layer = torch.nn.Linear(
            in_features=in_features, out_features=128, bias=False
        )
        #self.dropout1 = torch.nn.Dropout(0.5)
        self.leaky_relu1 = torch.nn.LeakyReLU(n2, inplace=True)
        self.batchNorm1 = torch.nn.LayerNorm(
            normalized_shape=[self.input_layer.out_features]
        )
        self.hidden1 = torch.nn.Linear(
            in_features=self.input_layer.out_features, out_features=64, bias=False
        )
        #self.dropout2 = torch.nn.Dropout(0.2)
        self.leaky_relu2 = torch.nn.LeakyReLU(n2, inplace=True)
        self.hidden2 = torch.nn.Linear(
            in_features=self.hidden1.out_features, out_features=out_features, bias=False
        )
        #self.dropout3 = torch.nn.Dropout(n1)
        # self.leaky_relu3 = torch.nn.LeakyReLU(n2, inplace=True)
        # self.hidden3 = torch.nn.Linear(
        #     in_features=self.hidden1.out_features, out_features=out_features, bias=False
        # )

    def forward(self, x):
        x = self.input_layer(x)
        #x = self.dropout1(x)
        x = self.leaky_relu1(x)
        x = self.batchNorm1(x)
        x = self.hidden1(x)
        #x = self.dropout2(x)
        x = self.leaky_relu2(x)
        x = self.hidden2(x)  
        #x = self.dropout3(x)
        # x = self.leaky_relu3(x)
        # x = self.hidden3(x)  # logits

        return x


class HTML5_JDIModel(torch.nn.Module):
    def __init__(self, in_features, out_features):
        super(HTML5_JDIModel, self).__init__()
        logger.info(f"IN_FEATURES: {in_features}, OUT_FEATURES: {out_features}")

        self.input_layer = torch.nn.Linear(
            in_features=in_features, out_features=100, bias=False
        )
        self.leaky_relu1 = torch.nn.LeakyReLU(0.1, inplace=True)
        self.batchNorm1 = torch.nn.LayerNorm(
            normalized_shape=[self.input_layer.out_features]
        )
        self.hidden1 = torch.nn.Linear(
            in_features=self.input_layer.out_features, out_features=32, bias=False
        )
        self.leaky_relu2 = torch.nn.LeakyReLU(0.1, inplace=True)
        self.hidden2 = torch.nn.Linear(
            in_features=self.hidden1.out_features, out_features=out_features, bias=False
        )

    def forward(self, x):
        x = self.input_layer(x)
        x = self.leaky_relu1(x)
        x = self.batchNorm1(x)
        x = self.hidden1(x)
        x = self.leaky_relu2(x)
        x = self.hidden2(x)  # logits

        return x
