import argparse
from concurrent.futures import ThreadPoolExecutor
from data_process import read_bc5cdr,build_prompt,save_json
from utils import Argument,get_Labels,Metric
from api import APIClient
parser = argparse.ArgumentParser(description='args path')
parser.add_argument('args')
parser.add_argument('api_name')
args = parser.parse_args()
class Eval():
    def __init__(self,dataset,api,args,metric,api_name):
        self.dataset=dataset
        self.api=api
        self.args=args
        self.metric=metric
        self.api_name=api_name
    def predict(self,example):     
        try:
            prompt=build_prompt(self.args.prompt,example["text"],examples=self.args.examples)
            response=self.api.generate(prompt)
            pred_entities=self.metric.parse_json(response)
            return {
                "text":example["text"],
                "entities":[
                    {"entity":p["entity"].lower(),"type":p["type"]}
                    for p in pred_entities
                ]
            }
        except Exception as e:
            print(f"请求失败：{e}")

        return None
    def eval(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            results=list(executor.map(self.predict,self.dataset))
        failed_results=[]
        for i,(pred,true) in enumerate(zip(results,self.dataset)):
            if pred is None:
                failed_results.append({
                    "index": i,
                    "text": true["text"]
                })
                continue
            self.metric.update(pred["entities"],true["entities"])
        save_json(failed_results,f"output/{self.api_name}_failed.json")
        self.metric.report()
        print(f"请求总数：{len(self.dataset)}")
        print(f"失败数量：{len(failed_results)}")

def main(arg_path,api_name):
    args=Argument(arg_path)
    dataset=read_bc5cdr(args.data_path)
    api=APIClient(api_name=api_name,temperature=args.temperature)
    labels=get_Labels(args.labels_path)
    metric=Metric(labels.labels)
    eval=Eval(dataset,api,args,metric,api_name)
    eval.eval()

if __name__=="__main__":
    main(args.args,args.api_name)

