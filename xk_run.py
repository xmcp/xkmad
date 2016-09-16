#coding=utf-8
import dill

print('=== 加载选课配置')
with open('save.bin','rb') as f:
    conf=dill.load(f)

s=conf['session']
base=conf['base']

for uri,(csrf_token,choice) in conf['selects'].items():
    print('=== 正在选择 %s'%uri)
    res=s.post(base+uri,data=dict(
        __RequestVerificationToken=csrf_token,
        rdoId=choice
    ))
    res.raise_for_status()
    if res.json()['Status']!=1:
        print('选课失败',res.json()['Message'])
        raise RuntimeError()

print('=== 完成')