import pandas as pd
import os
import random
import numpy as np
from sklearn.model_selection import StratifiedKFold
train_fname = 'data_gitignore/train_final.csv'
test_fname = 'data_origin/dev_set.csv'
train_df=pd.read_csv(train_fname)
test_df=pd.read_csv(test_fname, sep='\t')
test_df['label'] = 0
test_df.head()
X = np.array(train_df.index)
y = train_df.loc[:,'label'].values
def generate_data(random_state = 42, is_pse_label=False):
    """生成交叉验证数据集
    """
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    i = 0
    for train_index, dev_index in skf.split(X, y):
        print(i, "TRAIN:", train_index, "TEST:", dev_index)
        DATA_DIR = "./data_gitignore/data_StratifiedKFold_{}/data_final_{}/".format(random_state,i)
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        tmp_train_df = train_df.iloc[train_index]
        
        tmp_dev_df = train_df.iloc[dev_index]
        
        test_df['label'] = 0
        test_df.to_csv(DATA_DIR+"test.csv", index=False)
#         if is_pse_label:
#             pse_dir = "./data/data_pse_10fold/data_pse_24_{}/".format(i)
#             pse_df = pd.read_csv(pse_dir+'train.csv')
#             tmp_train_df = pd.concat([tmp_train_df, pse_df],ignore_index=True,sort=False)
            
        tmp_train_df.to_csv(DATA_DIR + "train.csv", index=False)
        tmp_dev_df.to_csv(DATA_DIR+"dev.csv", index=False)
        print(tmp_train_df.shape, tmp_dev_df.shape)
        i+=1
generate_data(random_state=42, is_pse_label=False)