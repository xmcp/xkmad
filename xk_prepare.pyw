#coding=utf-8
from tkinter import *
from tkinter.ttk import *
from libprepare import CmsSession
import threading
import dill

tk=Tk()
tk.title('xkmad prepare')
tk.resizable(False,False)

selects={}
unvar=StringVar()
pwvar=StringVar()
basevar=StringVar(value='http://123.127.180.224')
titlevar=StringVar(value='请登录')
logvar=StringVar(value='xkmad by @xmcp')

def log(x):
    logvar.set(x)
    tk.update_idletasks()

def login():
    title=sess.login(basevar.get(),unvar.get(),pwvar.get())
    loginbtn.state(['disabled'])
    titlevar.set(title)
    threading.Thread(target=loadcls).start()

def loadcls():
    for url,csrf_token,clses in sess.details():
        week=url.partition('weekId=')[2]
        week,_,period=week.partition('&periodId=')
        week=int(week)
        period=int(period.partition('&')[0])

        wrapper=Frame(book)
        book.add(wrapper,text='星期%d 时段%d'%(week,period))
        selects[url]=[csrf_token,IntVar(value=-1)]
        cursel=selects[url][1]

        cvs=Canvas(wrapper)
        f=Frame(cvs)
        scroll=Scrollbar(wrapper,orient=VERTICAL,command=cvs.yview)
        cvs['yscrollcommand']=scroll.set

        def config(_):
            cvs.configure(scrollregion=cvs.bbox('all'),width=700,height=400)

        cvs.grid(row=0,column=0,sticky='nswe')
        scroll.grid(row=0,column=1,sticky='ns')
        cvs.create_window((0,0),window=f,anchor='nw')
        wrapper.bind('<Configure>',config)

        for ind,(clsid,clstitle,clsteacher) in enumerate(clses):
            Radiobutton(f,text='ID = %d'%clsid,variable=cursel,value=clsid).grid(row=ind,column=0)
            Label(f,text=clstitle).grid(row=ind,column=1,sticky='we')
            Label(f,text=clsteacher).grid(row=ind,column=2)

    savebtn.state(['!disabled'])

def save():
    with open('save.bin','wb') as f:
        f.write(dill.dumps({
            'session': sess.s,
            'base': basevar.get(),
            'selects': {k:[v[0],v[1].get()] for k,v in selects.items()}
        }))
    logvar.set('配置保存成功')

upf=Frame(tk)
upf.grid(row=0,column=0,sticky='we',pady=2,padx=2)

Label(upf,text=' 用户名 ').grid(row=0,column=0)
Entry(upf,textvariable=unvar).grid(row=0,column=1)
Label(upf,text=' 密码 ').grid(row=0,column=2)
Entry(upf,textvariable=pwvar,show='*').grid(row=0,column=3)
Label(upf,text=' 网址 ').grid(row=0,column=4)
Entry(upf,textvariable=basevar).grid(row=0,column=5)
loginbtn=Button(upf,text='登录',command=login)
loginbtn.grid(row=0,column=6)

Label(tk,textvariable=titlevar,font='黑体 -18').grid(row=1,column=0,padx=5)

book=Notebook(tk)
book.grid(row=2,column=0,sticky='nswe')

downf=Frame(tk)
downf.grid(row=3,column=0,sticky='we',pady=2,padx=2)

savebtn=Button(downf,text='保存',command=save)
savebtn.state(['disabled'])
savebtn.grid(row=0,column=0)
Label(downf,textvariable=logvar).grid(row=0,column=1)

sess=CmsSession(log)
mainloop()
