import pandas as pd
import numpy as np
import networkx as nx
import os

class Topology:
  def __init__(self, file, type="csv",headers=None):
    if type == "csv":
      self.read_cvs(file)
    elif type == "xlsx":
      self.read_excel(file)
    self.graph = nx.Graph()
    self.V = len(self.data)
    self.graph.add_nodes_from(range(0, self.V))
    for i in range(0, self.V):
      for j in range(0, self.V):
          if self.data[i][j] == 1:
              self.graph.add_edge(i, j)

    self.E = self.graph.number_of_edges()
    self.D = nx.floyd_warshall_numpy(self.graph)

  def read_cvs(self, file):
    self.data = pd.read_csv(file, header=None).values

  def read_excel(self, file):
    self.data = pd.read_excel(file, header=None).values

  def degree(self):
    return [len(self.graph.edges([i])) for i in self.graph.nodes]

  def accessIndex(self):
    return [np.sum(i) for i in self.D]

  def keniganNumber(self):
    return [np.max(i) for i in self.D]

  def balewashIndex(self):
    ai = self.accessIndex()

    S = np.sum(ai)
    return [S/Si for Si in ai]
  def bichemanIndex(self):
    S = self.accessIndex()
    return [(self.V - 1)/Si for Si in S]

  def topologyMark(self):
    baleshIndex = self.balewashIndex()
    central_elem = np.max(baleshIndex)
    central_elem_col = np.where(baleshIndex == central_elem)[0][0]
    ai = self.accessIndex()
    central_elem = ai[central_elem_col]
    return [Si/central_elem for Si in ai]

  def alphaIndex(self):
    res = (self.E-self.V) / (2 * self.V-5)
    return res

  def betaIndex(self):
    res = self.E/self.V
    return res

  def fitaIndex(self):
    res = (self.E/(3*(self.V-2)))
    return res
  def centralElem(self):
    S = self.accessIndex()
    elem = np.min(S)
    index = S.index(elem)
    return index

  def make_report(self):
    report = {
      'accessIndex': self.accessIndex(),
      'nodesDegree': self.degree(),
      'keniganNumber': self.keniganNumber(),
      'balewashIndex': self.balewashIndex(),
      'bichemanIndex': self.bichemanIndex(),
      'alphaIndex': self.alphaIndex(),
      'betaIndex': self.betaIndex(),
      'fitaIndex': self.fitaIndex(),
      'centralElem': self.centralElem(),
      'nodes': [i for i in self.graph.nodes],
      'adj_matrix': self.data,
      'distance_matrix': self.D.tolist(),
    }
    return report

