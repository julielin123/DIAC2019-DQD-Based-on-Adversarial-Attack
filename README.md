# DQD-Based-on-Adversarial-Attack
5st place solution for competition [基于Adversarial Attack的问题等价性判别比赛](https://www.biendata.com/competition/2019diac/)

## B榜得分
训练2折：0.79442

## 开发环境

### python3.7 

pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com  boto3==1.9.229 regex==2019.8.19
pip install torch==1.3.1+cu92 torchvision==0.4.2+cu92 -f https://download.pytorch.org/whl/torch_stable.html

### pyltp

pip install pyltp

模型：ltp_data_v3.4.0 

## 项目结构简介
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
│    │    │    ├─newShape(形近字表)  
│    │    └─ src  
│    ├─ train_augment_data.py  
│    └─ train_origin_data.py  
└─ model  
       ├─ generate_submission.py  
       └─ model.sh  

### 数据使用

'dataset/train_origin_data.py'生成原始句子对

'dataset/train_augment_data.py'生成对抗句子对

'dataset/Kfold_dataset.py'生成交叉验证数据集

### 模型

‘src/FGM.py’ FGM模型class

‘src/pytorch_transformers/modeling_bert.py’ 在bert中使用fgm，增加扰动

'src/run_bert_base_fgm.py' 模型训练

### 运行
      ####数据处理
       在dataset下
       创建data_gitignore,用于放置训练数据
       用train_origin_data.py生成train_origin.csv,存于data_gitignore
       用train_augment_data.py生成train_augment.csv,存于data_gitignore
       将train_origin.csv，train_augment.csv相连得到train_final.csv
       用Kfold_dataset.py划分数据，得到5份划分数据，存在data_gitignore\data_StratifiedKFold_42下
      ####模型训练
       运行'model/model.sh'，训练模型
       运行'model/generate_submission.py'生成提交文件

## 参考
错别字生成参考[SimilarCharacter](https://github.com/contr4l/SimilarCharacter)

生成原始句子对参考[训练集构造](https://www.biendata.com/forum/view_post_category/718/)



