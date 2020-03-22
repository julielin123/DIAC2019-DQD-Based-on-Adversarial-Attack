# DIAC2019-DQD-Based-on-Adversarial-Attack
5st place solution for competition [Duplication Question Detection based on Adversarial Attack](https://www.biendata.com/competition/2019diac/)

## Introduction
>Although the QA system has made great progress in recent years, how to accurately determine whether the user's input is a semantic equivalent of a given question is still the key of a QA system (such as law, government affairs, etc.). For example, "What departments does the municipal government govern?" and "Which departments are under the jurisdiction of the municipal government?" can be considered as semantically equivalent issues, while "what departments does the municipal government govern?" and "Which departments do the mayor govern?" is different questions. For Duplication Question Detection, in addition to the accuracy of the system, the robustness of the system is also important, but it is often neglected. For example, although a deep neural network model can often achieve satisfactory accuracy on a given train set and test set, a slight change to the test set (Adversarial Attack) may cause a large decrease in overall accuracy.


## Analysis
       Data Processing：Use the rule below to train.
       A: qi is from <EquivalentSentence>, qj is from <EquivalentSentence>, label 1
       B: qi is from <EquivalentSentence>, qj is from <NotEquivalentSentence> label 0
       
       Data Augmentation ：For each sentence, replace it with synonym or character with similar form randomly to get two new sentences.
       For example:
       original sentence：民事诉讼什么情况下不能立案
       replaced with synonym：官事诉讼什么情况下不能立案
       replaced with characters with similar form：民事诉沦什么情况下不能立案
       
       Model：bert+fgm (roberta)

## Performance on B Leaderboard
fold：2
performance: 5st	yansixiliang      0.79442	     1  

## Environment

### python3.7 

pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com  boto3==1.9.229 regex==2019.8.19
pip install torch==1.3.1+cu92 torchvision==0.4.2+cu92 -f https://download.pytorch.org/whl/torch_stable.html

### pyltp
install pyltp  
>pip install pyltp  

download model：[ltp_data_v3.4.0 ](https://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569#list/path=%2F&parentPath=%2F)


## RUN
### Data Processing
       
       in dataset
       install pyltp, then copy pyltp-master to pyltp-master
       dowload ltp_data_v3.4.0, then copy it to pyltp-master
       put table character with similar form to pyltp-master/ltp_data_v3.4.0
       
       create data_gitignore to keep data
       USE train_origin_data.py TO GET train_origin.csv, KEEP IT IN data_gitignore
       USE train_augment_data.py TO GET train_augment.csv, KEEP IT IN data_gitignore
       Merge train_origin.csv, train_augment.csv TO GET train_final.csv
       USE Kfold_dataset.py TO GET 5 fold data, KEEP IT IN data_gitignore\data_StratifiedKFold_42
       
### Model Trainning
       
       RUN 'model/model.sh' TO train model.
       RUN 'model/generate_submission.py' TO get submit file.


## Project File Structure
.  
├─ 1120_roberta_wwm_large_150_last2embedding_cls  
├─ README.md  
├─ dataset  
│    ├─ Kfold_dataset.py  
│    ├─ data_gitignore  
│    │    ├─ data_StratifiedKFold_42  
│    │    ├─ train_augment.csv  
│    │    ├─ train_final.csv  
│    │    └─ train_origin.csv  
│    ├─ data_origin  
│    │    ├─ baifendian_data.zip  
│    │    ├─ dev_set.csv  
│    │    ├─ sample_submission.csv  
│    │    ├─ test_set.csv  
│    │    └─ train_set.xml  
│    ├─ pyltp-master  
│    │    ├─ ..  
│    │    ├─ ltp_data_v3.4.0  
│    │    │    ├─newShape(table of character with similar form)  
│    │    └─ src  
│    ├─ train_augment_data.py  
│    └─ train_origin_data.py  
└─ model  
       ├─ generate_submission.py  
       └─ model.sh  

### Data Processing

'dataset/train_origin_data.py' to get original sentence pair 
'dataset/train_augment_data.py' to get adversarial sentence pair 
'dataset/Kfold_dataset.py' to get cross-validation data set

### Model Training

'src/FGM.py' FGM model Class  
'src/pytorch_transformers/modeling_bert.py' use fgm in bert to add adversarial  
'src/run_bert_base_fgm.py' model train 

## Future Work
* add fold
* merge with other models
* use synonym extracting algorithm to get synonyms in Law Field

## References
How to generate wrong word? (https://github.com/contr4l/SimilarCharacter)

How to generate orginal sentence pair? (https://www.biendata.com/forum/view_post_category/718/)

Some briliant ideas (https://github.com/WenRichard/DIAC2019-Adversarial-Attack-Share)




