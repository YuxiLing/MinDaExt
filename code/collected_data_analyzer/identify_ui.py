
input_file='../sitemap_crawler/tmp.txt'
input_file2='../sitemap_crawler/tmp2.txt'
path_list=[]
with open(input_file,'r') as file:
    for line in file:
        line = line.strip()
        path_list.append(line)

with open(input_file2,'r') as file:
    for line in file:
        line = line.strip()
        path_list.append(line)

ext_num={}
for path in path_list:
    id=path.split('/')[1]
    if id in ext_num.keys():
        ext_num[id]+=1
    else:
        ext_num[id]=1

count=[0,0,0,0]
for key,val in ext_num.items():
    if val==1:
        count[0]+=1
    elif val<=5:
        count[1]+=1
    elif val<=10:
        count[2]+=1
    else:
        count[3]+=1


print('unique ext with ui',len(ext_num.keys()))
print(count)
