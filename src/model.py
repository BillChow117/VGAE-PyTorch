import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np
from torch.autograd import Variable

device = 'cuda' if torch.cuda.is_available() else 'cpu'

class VGAE(nn.Module):
   def __init__(self, **kwargs):
      super(VGAE, self).__init__()
      
      self.num_neurons = kwargs['num_neurons']
      self.num_features = kwargs['num_features']
      self.embedding_size = kwargs['embedding_size']

      self.w_0 = torch.nn.Parameter(torch.randn(self.num_features, self.num_neurons, requires_grad=True))
      self.b_0 = torch.nn.Parameter(torch.randn(self.num_neurons, requires_grad=True))
      
      self.w_1_mu = torch.nn.Parameter(torch.randn(self.num_neurons, self.embedding_size, requires_grad=True))
      self.b_1_mu = torch.nn.Parameter(torch.randn(self.embedding_size, requires_grad=True))

      self.w_1_sigma = torch.nn.Parameter(torch.randn(self.num_neurons, self.embedding_size, requires_grad=True))
      self.b_1_sigma = torch.nn.Parameter(torch.randn(self.embedding_size, requires_grad=True))
      
      torch.nn.init.normal_(self.w_0)
      torch.nn.init.normal_(self.w_1_mu)
      torch.nn.init.normal_(self.w_1_sigma)
      
      
   def encode(self, adjacency, norm_adj, x_features):
      
      hidden_0 = torch.relu(torch.add(torch.matmul(torch.matmul(norm_adj, x_features), self.w_0), self.b_0))
      
      self.GCN_mu = torch.add(torch.matmul(torch.matmul(norm_adj, hidden_0), self.w_1_mu), self.b_1_mu)
      self.GCN_sigma = torch.exp(torch.add(torch.matmul(torch.matmul(norm_adj, hidden_0), self.w_1_sigma), self.b_1_sigma))

      z = self.GCN_mu + ( torch.randn(adjacency.size(0), self.embedding_size) * self.GCN_sigma )
      
      return z
   
   @staticmethod
   def decode(z):
      x_reconstructed = torch.sigmoid(torch.matmul(z, z.t()))
      return x_reconstructed


      
   def forward(self, adjacency, norm_adj, x_features):
      z = self.encode(adjacency, norm_adj, x_features)
      x_reconstructed = VGAE.decode(z)
      
      return x_reconstructed
      
           
      