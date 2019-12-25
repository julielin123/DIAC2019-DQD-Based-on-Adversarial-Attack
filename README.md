# DQD-Based-on-Adversarial-Attack
5st place solution for competition [基于Adversarial Attack的问题等价性判别比赛](https://www.biendata.com/competition/2019diac/)

## 赛题简介
>虽然近年来智能对话系统取得了长足的进展，但是针对专业性较强的问答系统（如法律、政务等），如何准确的判别用户的输入是否为给定问题的语义等价问法仍然是智能问答系统的关键。举例而言，“市政府管辖哪些部门？”和“哪些部门受到市政府的管辖？”可以认为是语义上等价的问题，而“市政府管辖哪些部门？”和“市长管辖哪些部门？”则为不等价的问题。针对问题等价性判别而言，除去系统的准确性外，系统的鲁棒性也是很重要、但常常被忽略的一点需求。举例而言，虽然深度神经网络模型在给定的训练集和测试集上常常可以达到满意的准确度，但是对测试集合的稍微改变（Adversarial Attack）就可能导致整体准确度的大幅度下降。

## 赛题分析
       数据处理：和评论区的想法一样，采用下列规则得到训练数据
       A: qi is from <EquivalentSentence>, qj is from <EquivalentSentence>, label 1
       B: qi is from <EquivalentSentence>, qj is from <NotEquivalentSentence> label 0
       
       数据增强：每一个句子，随机替换同义词和形近字得到两个生成句，用上面的规则，得到增强的数据。
       下面是一个例子:
       原句：民事诉讼什么情况下不能立案
       替换同义词：官事诉讼什么情况下不能立案
       替换形近字：民事诉沦什么情况下不能立案
       
       训练模型：bert+fgm (roberta)

## B榜成绩
训练折数：2（因为没有时间，只训练了2折）  

成绩：5	yansixiliang      0.79442	     1  

## 开发环境

### python3.7 

pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com  boto3==1.9.229 regex==2019.8.19
pip install torch==1.3.1+cu92 torchvision==0.4.2+cu92 -f https://download.pytorch.org/whl/torch_stable.html

### pyltp
安装pyltp  
>pip install pyltp  

下载模型：[ltp_data_v3.4.0 ](https://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569#list/path=%2F&parentPath=%2F)


## 运行
### 数据处理
       
       在dataset下
       安装pyltp后，把pyltp-master的内容拷贝至pyltp-master下
       下载ltp_data_v3.4.0,拷贝至pyltp-master下
       将形近字表存放在pyltp-master/ltp_data_v3.4.0下（已放置）
       
       创建data_gitignore,用于放置训练数据
       用train_origin_data.py生成train_origin.csv,存于data_gitignore
       用train_augment_data.py生成train_augment.csv,存于data_gitignore
       将train_origin.csv，train_augment.csv相连得到train_final.csv
       用Kfold_dataset.py划分数据，得到5份划分数据，存在data_gitignore\data_StratifiedKFold_42下
       
### 模型训练
       
       运行'model/model.sh'，训练模型
       运行'model/generate_submission.py'生成提交文件


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

### 数据处理

'dataset/train_origin_data.py'生成原始句子对  
'dataset/train_augment_data.py'生成对抗句子对  
'dataset/Kfold_dataset.py'生成交叉验证数据集  

### 训练模型

'src/FGM.py' FGM模型class  
'src/pytorch_transformers/modeling_bert.py' 在bert中使用fgm，增加扰动  
'src/run_bert_base_fgm.py' 模型训练  

## 参考
错别字生成参考[SimilarCharacter](https://github.com/contr4l/SimilarCharacter)

生成原始句子对参考[训练集构造](https://www.biendata.com/forum/view_post_category/718/)




