import json
import requests
import xlrd

def post_data(name, id_no, tel):
    base_url = 'https://lflk.clear-sz.com/submit'
    headers = {'Content-type': 'application/json'}
    input_para = {
        'name': name,
        'idCardNo': id_no,
        'telephone': tel,
        'county': '随县',
        'street': '柳林镇',
        'healthStatus': '1'
    }
    resp = requests.post(
        url=base_url,
        data=json.dumps(input_para),
        headers=headers)
    # data = json.loads(resp)
    # print(resp.status_code)
    return resp.status_code

# read excel data
# xlrd.Book.encoding = "utf-8"
wb = xlrd.open_workbook('/Users/muzhi/Downloads/suizhou/suizhou.xlsx')
sheet = wb.sheet_by_name('去掉外地生活人员筛选表')
dat = []
for a in range(sheet.nrows):
    item = []
    cells = sheet.row_values(a)
    item.append(cells[1])
    item.append(cells[2])
    item.append(str(cells[6]).split('.')[0])
    dat.append(item)
print(len(dat))
print(dat[4])

empty = []
fail = []
succ = []
# compose data
for d in dat[4:]:
    if not d[0] or not d[1] or not d[2]:
        print('some empty value ...')
        empty.append(d)
    else:
        status = post_data(d[0], d[1], d[2])
        if status != 200:
            print('post fail ...')
            fail.append(d)
        else:
            succ.append(d)

with open('/Users/muzhi/Downloads/suizhou/empty.txt', 'w') as f:
    f.writelines(empty)
with open('/Users/muzhi/Downloads/suizhou/fail.txt', 'w') as f:
    f.writelines(fail)

print('empty len:', len(empty))
print('fail len:', len(fail))
print('succ len:', len(succ))
