#coding=utf-8
import pickle
import requests
import traceback
import os

print('=== 加载选课配置')
if os.environ.get('XMCP_ENV')!='XMCP':
    input('您不能运行该测试版！ ')
    raise SystemExit()
with open('save.bin','rb') as f:
    conf=pickle.load(f)

s=requests.Session()
s.cookies=requests.cookies.RequestsCookieJar()
s.cookies._cookies=conf['session']
TIMEOUT=15

for uri,(csrf_token,choice) in conf['selects'].items():
    print('=== %s'%uri)
    if choice==-666:
        print(' -> 不更改')
        continue
    else:
        print(' -> 选择 %d'%choice)
        while True:
            try:
                res=s.post(uri,data=dict(
                    __RequestVerificationToken=csrf_token,
                    rdoId=choice
                ),timeout=TIMEOUT)
                res.raise_for_status()
                if res.json()['Status']!=1:
                    raise RuntimeError(res.json()['Message'])
            except Exception:
                traceback.print_exc()
                print(' !! 正在重试')
            else:
                print(' ^^ 选课成功')
                break
                
print('=== 完成')
input('按回车键退出 ')