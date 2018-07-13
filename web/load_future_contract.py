import requests
import re

url = "http://finance.sina.com.cn/iframe/futures_info_cff.js"

if __name__ == '__main__':
    r = requests.get(url)
    model = 'new Array\\("(.+)","(.+)"\\);'
    model = re.compile(model)

    all_text = r.text

    all_list = all_text.split('\r\n')

    all_contract = set()
    for line in all_list:
        m = model.search(line)
        print(line)

        if m:
            print(m.group(2))
            all_contract.add(m.group(2))

    with open('future_contract.txt','w') as f:
        for i in all_contract:
            f.write(str(i)+'\n')
            

    

    
