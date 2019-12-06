import numpy as np
import pandas as pd
import networkx as nx

from random import randint

class PrepareGraph:
   def __init__(self, **kwargs):
      self.load_adjacency_matrix(kwargs['file'])
      self.train_test_split(kwargs['test_size'])
      self.normalize_adjacency_matrix()
      self.x_features = np.identity(self.adjacency.shape[0])
      
   def normalize_adjacency_matrix(self):
      G = nx.from_numpy_matrix(self.train_adj)
      self.normalized = nx.normalized_laplacian_matrix(G)
      self.normalized = self.normalized.toarray()
      
      pass
      
   def train_test_split(self, test_size):
      
      self.train_edges = list()
      self.test_edges = list()
      self.false_edges = list()
      
      self.train_adj = self.adjacency.copy()
      
      num_test_edges = round(len(self.edges) * test_size)
      
      # Create false edges
      while len(self.false_edges) < num_test_edges:
         row = randint(0, self.train_adj.shape[0])
         col = randint(0, self.train_adj.shape[0])
         
         if row != col:
            if tuple([row, col]) not in self.edges:
               if tuple([col, row]) not in self.edges:
                  if tuple([row, col]) not in self.false_edges:
                     if tuple([col, row]) not in self.false_edges:
                        self.false_edges.append(tuple([row, col]))
      
      # Create test edges
      idx_test = list()
      while len(idx_test) < num_test_edges:
         idx = randint(0, len(self.edges)-1)
         if idx not in idx_test:
            idx_test.append(idx)

      for idx in idx_test:
         self.test_edges.append(self.edges[idx])
         self.train_adj[self.edges[idx][0], self.edges[idx][1]] = 0
         self.train_adj[self.edges[idx][1], self.edges[idx][0]] = 0
      
      # Train edges
      for i in range(self.train_adj.shape[0]):
         for j in range(self.train_adj.shape[1]):
            if self.train_adj[i][j] == 1:
               self.train_edges.append(tuple([i,j]))
               
      pass
      
   def load_adjacency_matrix(self, file):
      
      self.id_to_node = {}
      self.node_to_id = {}
      
      # Load csv file
      self.edges = pd.read_csv(file, header=None)
      self.edges = self.edges.values
      self.edges = [tuple(edge) for edge in self.edges]
      
      G = nx.Graph()
      G.add_edges_from(self.edges)
      
      i=0
      for node in G.nodes():
         self.id_to_node[i] = node
         self.node_to_id[node] = i
         i+=1
      
      # Build adjacency matrix
      self.adjacency = np.zeros((len(G.nodes()), len(G.nodes())), dtype=int)
      for edge in self.edges:
         self.adjacency[edge[0], edge[1]] = 1
         self.adjacency[edge[1], edge[0]] = 1
      
      self.adjacency = self.adjacency + np.identity(len(G.nodes()))

      pass
