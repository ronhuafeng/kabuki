import kabuki
from kabuki.hierarchical import Knode
import numpy as np
import pymc as pm

def load_models():
    """
    This function returns a list of models that are going to be tested
    """
    import hddm
    n = 400
    dtype = [('response', np.int), ('rt', np.float), ('subj_idx', np.int32), ('cond1', 'S20'), ('cond2', 'S20')]
    data = np.empty(n, dtype=dtype)
    data['rt'] = np.random.rand(n) + 0.5;
    data['response'] = np.random.randint(2, size=n)
    data['cond1'] = np.array(['A','B'])[np.random.randint(2, size=n)]
    data['cond2'] = np.array(['A','B'])[np.random.randint(2, size=n)]
    data['subj_idx'] = np.zeros(n)

    models = []
    #model 1
    m = hddm.HDDM(data, depends_on = {'v':'cond1'})
    models.append(m)

    #model 2
    m = hddm.HDDM(data, depends_on = {'v':['cond1', 'cond2'], 'a':'cond1'}, include =['z','sv'])
    models.append(m)

    data['subj_idx'] = np.random.randint(5, size=n)
    #model 3
    m = hddm.HDDM(data, depends_on = {'v':'cond1'})
    models.append(m)

    m = hddm.HDDM(data, depends_on = {'v':['cond1', 'cond2'], 'a':'cond1'}, include=['sv'], group_only_nodes=['sv'])
    models.append(m)

    return models

def sample_from_models(models, n_iter = 200):
    """sample from all models"""
    for i, model in enumerate(models):
        print "sample model", i
        model.sample(n_iter)
