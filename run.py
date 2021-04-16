from typing import Text
import requests
import json


def main():

    url = 'https://rate.tmall.com/list_detail_rate.htm'
    params = {
        'itemId': '640860381255',
        'spuId': '2011017284',
        'sellerId': '1714128138',
        'order': '3',
        'currentPage': '1',
        'append': '0',
        'content': '1',
        'picture': '1',
        'needFold': '0',
        '_ksTS': ' 1618554248318_4050',
        'callback': '_'
    }
    headers = {
        'referer': 'https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w15914064-15567552165.71.69ff5f3bbwxFUa&id=640860381255&scene=taobao_shop',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'cookie': 'cna=0s9PGJSH9BACAWonKueiRWp6; lid=iamroot2333; enc=P70ZfjiDN%2Fs6aOWdphJ12Wl5hZdMZMiMl07bkDA1iY%2FYS9Rcl7hrtsR3H%2BJ6aWsxbaRPXJlnk7wr5Fo%2BrTHnhw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; xlly_s=1; t=5fe0153a2ab93059bcaa2884a22c9acd; tracknick=iamroot2333; lgc=iamroot2333; _tb_token_=3339be33933b6; cookie2=1c8c6892e03d22b2e4cee21c8b8e69f2; _m_h5_tk=8a2b9829561136635a6e4706d4e92adc_1618562112092; _m_h5_tk_enc=0b6d332f4edb65fbdf6fac3d40f22230; dnk=iamroot2333; _l_g_=Ug%3D%3D; unb=2993042747; cookie1=BqPn64USqnye3K%2BwBF0q5tY7RZlGonyiMizxRgblsCY%3D; login=true; cookie17=UUGrdT7QI%2FAe4w%3D%3D; _nk_=iamroot2333; sg=37d; x5sec=7b22726174656d616e616765723b32223a223837663434643536316464396361383137636462613066343132666431316462434a6e6d35494d4745504f5339384f4e352b664351426f4d4d6a6b354d7a41304d6a63304e7a73784b41497737626e2f3350372f2f2f2f2f41513d3d227d; uc1=cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0&cookie14=Uoe1iuWXIj6sOA%3D%3D&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=V32FPkk%2FgPzW&existShop=false; uc3=vt3=F8dCuwpnkAB3jRLml4Q%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=CseRbvwCy9L3Hsk%3D&id2=UUGrdT7QI%2FAe4w%3D%3D; uc4=nk4=0%40CMaQROfkMbKllrxDikwgF8MbF%2FpXQA%3D%3D&id4=0%40U2OcRZ7Rg7TlQd3Cyey1uWAu%2FTta; sgcookie=E100Jm6CKmL1K3T9qTzxUF1W54M4yv9CkLhxDM%2B09%2BOaP1HdpWzmZ%2Fspr6lfJhsm0rvcyu2jGmcrqhQ9kGsB81yV3w%3D%3D; csg=b99b07df; tfstk=cJodB92oLCAnUP2t32LGFnDDSxadZBd819Nl2pLjfn-Mc0jRianmDqmvR81LXdC..; isg=BOrqUfBbftyk_s2daN-vTCLOO1CMW261QLRzOnSiSD1Cp4hhX--qxLaRN9O7V-ZN; l=eBT3V124O0LJ3V8jBO5Zourza77OUIdbzsPzaNbMiInca6LlMKwW4NCQ5Wgpydtjgt5b3e-zd4S4yREMPoUU-E_ceTwhKXIpBMvM8e1..'
    }
    r = requests.get(url, params, headers=headers)
    r.encoding = 'utf-8'
    print(r.status_code)
    data = json.loads(r.text[4:len(r.text)-1])
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data.get('rateDetail').get('rateList'), ensure_ascii=False, indent=4))
        f.flush()


if __name__ == '__main__':
    main()
