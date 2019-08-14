from pymongo import MongoClient
import pdb
Client = MongoClient('mongodb://root_esoda:root_esoda@127.0.0.1') 
col = Client.hcihub.esoda_hci_papers
paper_num = 0
acm_num = 0
ref_num = 0
with open('pairs.txt', 'w') as f:
    for item in col.find():
        paper_num += 1
        if 'acmdl_id' not in item:
            continue
        if not len(item['acmdl_id'].strip()):
            continue
        line = item['title']+'|||'+item['acmdl_id'].strip()
        if 'references' in item:
            for ref in item['references']:
                if len(ref['id'].strip()):
                    line += ' ' + ref['id'].strip()
                    ref_num += 1
        f.write(line+'\n')
        acm_num += 1
print(paper_num, acm_num, ref_num)

