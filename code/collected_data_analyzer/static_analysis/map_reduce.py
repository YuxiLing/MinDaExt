import pandas as pd


def read_source_csv():
    api_f1 = 'vm_result/chrome_api_final_a-c.csv'
    api_f2 = 'vm_result/chrome_api_final_d-g.csv'
    api_f3 = 'vm_result/chrome_api_final_h-p.csv'

    api_pd1 = pd.read_csv(api_f1)
    api_pd2 = pd.read_csv(api_f2)
    api_pd3 = pd.read_csv(api_f3)

    api_pd = (api_pd1.append(api_pd2)).append(api_pd3)

    tag_f1 = 'vm_result/input_tag_a-c.csv'
    tag_f2 = 'vm_result/input_tag_d-g.csv'
    tag_f3 = 'vm_result/input_tag_h-p.csv'

    tag_pd1 = pd.read_csv(tag_f1)
    tag_pd2 = pd.read_csv(tag_f2)
    tag_pd3 = pd.read_csv(tag_f3)
    tag_pd = (tag_pd1.append(tag_pd2)).append(tag_pd3)

    traffic_f1 = 'vm_result/traffic_a-c_request_part.csv'
    traffic_f2 = 'vm_result/traffic_a-c_request_part2.csv'
    traffic_f3 = 'vm_result/traffic_d-g_request_part1.csv'
    traffic_f4 = 'vm_result/traffic_d-g_request_part2.csv'
    traffic_f5 = 'vm_result/h-p_request_part1.csv'
    traffic_f6 = 'vm_result/h-p_request_part2.csv'
    traffic_f7 = 'vm_result/h-p_request_part3.csv'

    traffic_pd1 = pd.read_csv(traffic_f1)
    traffic_pd2 = pd.read_csv(traffic_f2)
    traffic_pd3 = pd.read_csv(traffic_f3)
    traffic_pd4 = pd.read_csv(traffic_f4)
    traffic_pd5 = pd.read_csv(traffic_f5)
    traffic_pd6 = pd.read_csv(traffic_f6)
    traffic_pd7 = pd.read_csv(traffic_f7)

    t1 = traffic_pd1.append(traffic_pd2)
    t2 = traffic_pd3.append(traffic_pd4)
    t3 = traffic_pd5.append(traffic_pd6)
    t4 = t3.append(traffic_pd7)
    tmp1=t1.append(t2)
    tmp2=t3.append(t4)
    traffic_pd = tmp1.append(tmp2)

    return api_pd, tag_pd, traffic_pd


data_types = ['UPI', 'HI', 'FPI', 'AI', 'PCI',
              'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']


def union(api_pd, tag_pd, traffic_pd):
    data_types = ['UPI', 'HI', 'FPI', 'AI', 'PCI',
                  'LI', 'WHI', 'UAI', 'WCI', 'DI', 'PS', 'FS']
    for d_t in data_types:
        api_pd[d_t] = 0

    tag_pd = tag_pd.reset_index()
    traffic_pd = traffic_pd.reset_index()
    for index, row in tag_pd.iterrows():
        ext_name = row['ext'].split('_')[0]

        for dt in data_types:
            if row[dt] != 0:
                api_pd.loc[api_pd['ext'] == ext_name, dt] = row[dt]

    for index, row in traffic_pd.iterrows():
        ext_name = row['ext']

        for dt in data_types:
            if row[dt] != 0:
                api_pd.loc[api_pd['ext'] == ext_name, dt] += row[dt]

    return api_pd


def reducer(api_pd):
    ext_count = dict()
    # initialize
    for dt in data_types:
        ext_count[dt] = 0

    api_pd = api_pd.reset_index()

    for index, row in api_pd.iterrows():
        for dt in data_types:
            if row[dt] != 0:
                ext_count[dt] += 1
    return ext_count


def format_print(ext_count):
    for ext in ext_count:
        print(ext, ext_count[ext])


'''

UPI 2607
HI 136
FPI 96
AI 2913
PCI 476
LI 105
WHI 0
UAI 0
WCI 0
DI 10266
PS 161
FS 93

'''

if __name__ == '__main__':
    api_pd, tag_pd, traffic_pd = read_source_csv()

    union_pd = union(api_pd, tag_pd, traffic_pd)

    ext_count = reducer(union_pd)
    print(union_pd.head())
    union_pd.to_csv('./chrome_union.csv', index=False)
    format_print(ext_count)
