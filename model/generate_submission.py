import pandas as pd
import numpy as np


df = pd.read_csv('./1120_roberta_wwm_large_150_last2embedding_cls/1120_roberta_wwm_large_150_last2embedding_cls_0/sub.csv')
df = df[['qid']]
df['0'] = 0
df['1'] = 0

k = 5
for i in [0,3]:
    temp=pd.read_csv('./1120_roberta_wwm_large_150_last2embedding_cls/1120_roberta_wwm_large_150_last2embedding_cls_{}/sub.csv'.format(i))
    df['0']+=temp['label_0']/k
    df['1']+=temp['label_1']/k
print(df['0'].mean())

df['label']=np.argmax(df[['0','1']].values,-1)
submit_fname = './1120_roberta_wwm_large_150_last2embedding_cls/1120_roberta_wwm_large_150_last2embedding_cls_sub_01234.csv'
df[['qid','label']].to_csv(submit_fname,\
                           index=False,header=False,sep='\t')
print(submit_fname)