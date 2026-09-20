import os
import json_repair
from json_repair import load
class Argument:
    def __init__(self,arg_path):
        self.arg_dict=self.load_arg(arg_path)
        for k,v in self.arg_dict.items():
            setattr(self,k,v)

    def load_arg(self,arg_path):
        if not os.path.exists(arg_path):
            raise FileExistsError(f"配置文件{arg_path}不存在")
        else:
            return load(open(arg_path, "rb"))

class get_Labels:
    def __init__(self,labels_path):
        self.labels=self.load_labels(labels_path)
    def load_labels(self,labels_path):
        if not os.path.exists(labels_path):
            raise FileExistsError(f"labels文件{labels_path}不存在")
        else:
            return load(open(labels_path, "rb"))
class Metric:
    def __init__(self,labels):
        self.tp=0
        self.pred_sum=0
        self.true_sum=0
        self.entities_tp={}
        self.entities_pred_num={}
        self.entities_true_num={}
        self.types=labels

    def parse_json(self,response):
        try:
            entities=json_repair.loads(response)
            if isinstance(entities,dict):
                entities=entities.get("entities",[])
            if not isinstance(entities,list):
                return []
            return entities
        except (TypeError, ValueError):
            return []
    def update(self,pred_entities,true_entities):
        self.pred_sum+=len(pred_entities)
        self.true_sum+=len(true_entities)
        for pred in pred_entities:
            entity_type=pred["type"]
            self.entities_pred_num[entity_type]=self.entities_pred_num.get(entity_type,0)+1
        for true in true_entities:
            entity_type=true["type"]
            self.entities_true_num[entity_type]=self.entities_true_num.get(entity_type,0)+1
        true_copy=true_entities.copy()
        for pred in pred_entities:
            for i,true in enumerate(true_copy):
                if (pred["entity"]==true["entity"]
                    and pred["type"]==true["type"]):
                    self.tp+=1
                    self.entities_tp[pred["type"]]=self.entities_tp.get(pred["type"],0)+1
                    true_copy.pop(i)
                    break
        

    def compute(self,tp,pred,true):
        eps=1e-8
        precision=tp/(pred+eps)
        recall=tp/(true+eps)
        f1=2*precision*recall/(precision+recall+eps)

        return precision,recall,f1
    def report(self):
        print(f"{'Entity':<10}{'Precision':<15}{'Recall':<15}{'F1-Score':<15}{'Support':<10}")
        for type in self.types:
            precision,recall,f1=self.compute(self.entities_tp.get(type,0),self.entities_pred_num.get(type,0),self.entities_true_num.get(type,0))
            print(f"{type:<10}{precision:<15.2f}{recall:<15.2f}{f1:<15.2f}{self.entities_true_num.get(type,0):<10}")
        micro_avg_p,micro_avg_r,micro_avg_f=self.compute(self.tp,self.pred_sum,self.true_sum)
        print(f"{'micro avg':<10}{micro_avg_p:<15.2f}{micro_avg_r:<15.2f}{micro_avg_f:<15.2f}{self.true_sum:<10}")
