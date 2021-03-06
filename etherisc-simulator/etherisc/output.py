# -*- coding: utf-8 -*-
# @Author: Jake Brukhman
# @Date:   2016-11-30 22:01:55
# @Last Modified by:   Jake Brukhman
# @Last Modified time: 2016-12-15 17:45:52

from scipy.stats import norm, uniform
from etherisc.variable import EtheriscEstimator
from etherisc.data import extract_flight_csv
from etherisc.simulation import EtheriscSimulator

def estimatedata(filename, datatype='flightcsv', payout=500, randomsample=0, minprob=0.001, maxprob=0.20):
  """
  Load actual data for model estimation.
  """
  data = __loaddata(filename, datatype=datatype, minprob=minprob, maxprob=maxprob)
  estimator = __estimatedata(data, payout=payout, 
    randomsample=randomsample)
  print(estimator)
  print(estimator.data)


def __estimatedata(data, payout=500, randomsample=0):
  """
  Estimate the Etherisc model from a dataframe. The data
  frame will be expected to have a column called `probs` for
  event probabilities and an index of labels.

  data          data frame with event probabilities and labels
  payout        the payout level desired
  randomsample  if this is > 0, then the estimate will randomly sample some 
                number of data points for the calculation
  """
  if randomsample > 0:
    data = data.sort('prob')
    data = data.head(randomsample)

  data['premium'] = 0.0
  data['payout'] = payout

  # get the model parameters
 
  # estimate
  estimator = EtheriscEstimator(data)
  estimator.estimate()
  return estimator


def __loaddata(filename, datatype='flightcsv', minprob=0.001, maxprob=0.20):
  """
  Load event probability data.
  """
  if datatype is 'flightcsv':
    return extract_flight_csv(filename, minprob=minprob, maxprob=maxprob)
  else:
    raise Exception('unknown datatype %s' % datatype)


def simulate(filename, datatype='flightcsv', payout=500, minprob=0.001, maxprob=0.20, auxcapital=20000):
  data = __loaddata(filename, datatype=datatype, minprob=minprob, maxprob=maxprob)
  __simulate(data, payout=payout, minprob=minprob, maxprob=maxprob, auxcapital=auxcapital)

def __simulate(data, payout=500, minprob=0.001, maxprob=0.20, auxcapital=20000):
  simulator = EtheriscSimulator(data, auxcapital=auxcapital)
  
  for _ in range(100):
    policy = simulator.underwrite(payout)
    print(policy)
    
