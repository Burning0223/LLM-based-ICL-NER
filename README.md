# **LLM-based** 上下文学习的实体识别（ICL-NER）任务

## 项目简介

通过调用大语言模型（如 **GPT-4、Qwen2.5、DeepSeek** 等）的 API，在**BC5CDR** 数据集上实现基于上下文学习（In-Context Learning, ICL）的命名实体识别（NER）任务。

## 项目结构

``` 
├── Argument         # 参数配置文件
│   ├── arg_1.json
│   ├── arg_2.json
│   └── arg_3.json
├── utils.py          # 功能类
├── data_process.py    # 读取数据、建立prompt
├── api.py     # api调用
├── main.py     # 训练器以及程序入口
├── requirements.txt   # 环境依赖
└── README.md          # 项目说明
```

## 数据格式

```
8701013|t|Famotidine-associated delirium. A series of six cases.
8701013|a|Famotidine is a histamine H2-receptor antagonist used in inpatient settings for prevention of stress ulcers and is showing increasing popularity because of its low cost. Although all of the currently available H2-receptor antagonists have shown the propensity to cause delirium, only two previously reported cases have been associated with famotidine. The authors report on six cases of famotidine-associated delirium in hospitalized patients who cleared completely upon removal of famotidine. The pharmacokinetics of famotidine are reviewed, with no change in its metabolism in the elderly population seen. The implications of using famotidine in elderly persons are discussed.
8701013	0	10	Famotidine	Chemical	D015738
8701013	22	30	delirium	Disease	D003693
8701013	55	65	Famotidine	Chemical	D015738
8701013	156	162	ulcers	Disease	D014456
8701013	324	332	delirium	Disease	D003693
8701013	395	405	famotidine	Chemical	D015738
8701013	442	452	famotidine	Chemical	D015738
8701013	464	472	delirium	Disease	D003693
8701013	537	547	famotidine	Chemical	D015738
8701013	573	583	famotidine	Chemical	D015738
8701013	689	699	famotidine	Chemical	D015738
8701013	CID	D015738	D003693
```

## 环境依赖

``` 
pip install -r requirements.txt
```

## 模型参数设置

``` 
{
    "prompt":"You are a biomedical named entity recognition model.Given a biomedical text, identify all Chemical and Disease entities.Return the result strictly in JSON format with the following structure:{\"text\": \"input text\",\"entities\": [{\"entity\": \"entity name\", \"type\": \"Chemical or Disease\"}]}If there are no entities, return an empty \"entities\" list.",
    "examples":[],
    "data_path":"data/CDR_TestSet.PubTator.txt",
    "labels_path":"data/labels.json",
    "temperature":1
}
```

## 输出示例

```
{
  "text": "Aspirin is used to treat headache.",
  "entities": [
    {
    "entity": "Aspirin", 
    "type": "Chemical"
    },
    {
    "entity": "headache", 
    "type": "Disease"
    }
  ]
}
```

## 实验结果

### gpt-5.6-luna

#### 0-shot:

运行命令：

``` 
python main.py Argument/args_1.json gpt-5.6-luna
```

``` 
Entity    Precision      Recall         F1-Score       Support
Chemical  0.80           0.30           0.44           5385
Disease   0.72           0.36           0.49           4424
micro avg 0.76           0.33           0.46           9809
```

#### 1-shot:

运行命令：

```
python main.py Argument/args_2.json gpt-5.6-luna
```

```
Entity    Precision      Recall         F1-Score       Support   
Chemical  0.83           0.84           0.84           5385      
Disease   0.76           0.72           0.74           4424      
micro avg 0.80           0.79           0.79           9809  
```

#### 3-shot:

运行命令：

```
python main.py Argument/args_3.json gpt-5.6-luna
```

```
Entity    Precision      Recall         F1-Score       Support   
Chemical  0.85           0.84           0.84           5385
Disease   0.73           0.76           0.75           4424
micro avg 0.79           0.80           0.80           9809
```



### deepseek-flash

#### 0-shot:

运行命令：

``` 
python main.py Argument/args_1.json deepseek-flash
```

``` 
Entity    Precision      Recall         F1-Score       Support
Chemical  0.71           0.29           0.42           5385
Disease   0.67           0.41           0.51           4424
micro avg 0.69           0.35           0.46           9809
```

#### 1-shot:

运行命令：

``` 
python main.py Argument/args_2.json deepseek-flash
```

``` 
Entity    Precision      Recall         F1-Score       Support
Chemical  0.83           0.92           0.87           5385
Disease   0.78           0.82           0.80           4424
micro avg 0.80           0.87           0.84           9809
```

