import json
def read_bc5cdr(file_path):
    documents={}
    with open(file_path,"r",encoding="utf-8") as f:
        for line in f:
            line=line.rstrip("\n")
            if not line:
                continue
            if "|t|" in line or "|a|" in line:
                id,part,content=line.split("|", 2)
                if id not in documents:
                    documents[id]={
                        "text":"",
                        "abstract":"",
                        "entities":[]
                    }
                if part=="t":
                    documents[id]["text"]=content
                elif part=="a":
                    documents[id]["abstract"]=content
                    documents[id]["text"]+=content
            else:
                parts=line.split("\t")
                if len(parts)>=6:
                    id=parts[0]
                    entity=parts[3]
                    type=parts[4]
                    if type not in ["Chemical","Disease"]:
                        continue
                    if id not in documents:
                        documents[id]={
                        "text":"",
                        "abstract":"",
                        "entities":[]
                    }
                    documents[id]["entities"].append(
                        {"entity":entity.lower(), "type":type}
                    )
                elif len(parts)==4 and parts[1]=="CID":
                    continue
    dataset=[]
    for id,document in documents.items():
        dataset.append({
            "text":document["text"],
            "entities":document["entities"]
        })
    return dataset
def save_json(data,file_path): 
    with open(file_path,"w",encoding="utf-8") as f: 
        json.dump(data,
                  f,
                  ensure_ascii=False,
                  indent=2)
def build_prompt(prompt,text,examples=None):
    if examples:
        prompt+="\nHere are some examples:\n"
        for i,example in enumerate(examples,1):
            output={
                "text":example["text"],
                "entities":[{
                    "entity":e["entity"].lower(),"type":e["type"]}
                    for e in example["entities"]]
            }

            prompt+=f"""
Example {i}:
Text: {example["text"]}
Output:
{json.dumps(output['entities'], ensure_ascii=False, indent=2)}
"""
    prompt+=f"""
Now identify the entities in the following text:
Text: {text}
Output:
"""
    return prompt

           


