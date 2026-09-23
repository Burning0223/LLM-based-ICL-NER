import argparse
from concurrent.futures import ThreadPoolExecutor
from json_repair import load
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
        self.out_path=f"output/{self.api_name}_output.json"
        self.failed_path=f"output/{self.api_name}_failed.json"
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
        try:
            results=load(open(self.out_path, "rb"))
            if len(results)!=len(self.dataset):
                print("已有结果数量与数据集数量不一致，重新开始。")
                results=[None]*len(self.dataset)
            else:
                 print("发现已有结果，继续执行。")
        except FileNotFoundError:
            print("没有发现已有结果，从头开始。")
            results=[None]*len(self.dataset)
        completed_count=0
        for result in results:
            if result is not None:
                completed_count+=1
        pending_idx=[
            i
            for i,result in enumerate(results)
            if result is None
        ]
        print(f"已完成的请求：{completed_count}/{len(self.dataset)}")
        print(f"未完成的请求：{len(pending_idx)}")
        if pending_idx:
            with ThreadPoolExecutor(max_workers=10) as executor:
                predictions=executor.map(self.predict,[self.dataset[i] for i in pending_idx])
            for i,pred in zip(pending_idx,predictions):
                results[i]=pred
                save_json(results,self.out_path)
        else:
            print("所有数据都已经完成，不需要重新请求。")
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
        print(f"请求成功数量：{len(self.dataset)-len(failed_results)}")
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

