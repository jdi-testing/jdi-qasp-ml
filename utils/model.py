import torch

class JDIModel(torch.nn.Module):
    def __init__(self):
        super(JDIModel, self).__init__()
        
        self.input_layer = torch.nn.Linear(in_features=IN_FEATURES, out_features=64, bias=False)
        self.batchNorm1 = torch.nn.LayerNorm(normalized_shape=[self.input_layer.out_features])
        self.leaky_relu1 = torch.nn.LeakyReLU(inplace=True)
        self.hidden1 = torch.nn.Linear(in_features=self.input_layer.out_features, out_features=32, bias=False)
        self.batchNorm2 = torch.nn.LayerNorm(normalized_shape=[self.hidden1.out_features])
        self.leaky_relu2 = torch.nn.LeakyReLU(inplace=True)
        self.hidden2 = torch.nn.Linear(in_features=self.hidden1.out_features, out_features=OUT_FEATURES, bias=True)
        
    def forward(self, x):
        x = self.input_layer(x)
        x = self.batchNorm1(x)
        x = self.leaky_relu1(x)
        x = self.hidden1(x)
        x = self.batchNorm2(x)
        x = self.leaky_relu2(x)
        x = self.hidden2(x) # logits

        return x
        
