#coding=utf-8
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from libprepare import CmsSession
import pickle

tk=Tk()
tk.title('xkmad prepare')
tk.rowconfigure(2,weight=1)
tk.columnconfigure(0,weight=1)
tk.geometry('800x500')

selects={}
unvar=StringVar()
pwvar=StringVar()
basevar=StringVar(value='http://58.119.34.118/xuanke')
titlevar=StringVar(value='请登录')
logvar=StringVar(value='xkmad by @xmcp')

def log(x):
    logvar.set(x)
    tk.update_idletasks()

def login():
    savebtn.state(['disabled'])
    selects.clear()
    val=basevar.get()
    if '://' not in val:
        val='http://'+val
    if val[-1]=='/':
        val=val[:-1]
    basevar.set(val)
    tk.update_idletasks()

    try:
        title=sess.login(val,unvar.get(),pwvar.get())
    except Exception as e:
        return messagebox.showerror('登录失败','%s\n\n%s'%(type(e),e))
    titlevar.set(title)
    unentry.state(['disabled'])
    pwentry.state(['disabled'])
    baseentry.state(['disabled'])

    try:
        loadcls()
    except Exception as e:
        return messagebox.showerror('加载失败', '%s\n\n%s' % (type(e), e))
    #loginbtn.state(['disabled'])
    savebtn.state(['!disabled'])

def loadcls():
    for ch in book.children.values():
        book.forget(ch)
    book.children={}
    for url,csrf_token,clses in sess.details():
        week=url.partition('weekId=')[2]
        week,_,period=week.partition('&periodId=')
        week=int(week)
        period=int(period.partition('&')[0])

        wrapper=Frame(book)
        wrapper.rowconfigure(0,weight=1)
        wrapper.columnconfigure(0,weight=1)
        book.add(wrapper,text='星期%d 时段%d'%(week,period))
        selects[url]=[csrf_token,IntVar(value=-666)]
        cursel=selects[url][1]

        cvs=Canvas(wrapper)
        f=Frame(cvs)
        f.columnconfigure(1,weight=1)
        scroll=Scrollbar(wrapper,orient=VERTICAL,command=cvs.yview)
        cvs['yscrollcommand']=scroll.set

        def config(_):
            cvs.configure(scrollregion=cvs.bbox('all'))

        cvs.grid(row=0,column=0,sticky='nswe')
        scroll.grid(row=0,column=1,sticky='ns')
        cvs.create_window((0,0),window=f,anchor='nw')
        wrapper.bind('<Configure>',config)

        Radiobutton(f,text='不进行更改',variable=cursel,value=-666).grid(row=0,column=0,columnspan=3,sticky='we',pady=2)
        for ind,(clsid,clstitle,clsteacher) in enumerate(clses):
            Radiobutton(f,text='[ID = %s]'%(clsid if clsid!=-666 else '已选'),variable=cursel,value=clsid)\
                .grid(row=ind+1,column=0,sticky='we')
            Label(f,text=clstitle).grid(row=ind+1,column=1,sticky='we',padx=10)
            Label(f,text=clsteacher).grid(row=ind+1,column=2)

def save():
    with open('save.bin','wb') as f:
        f.write(pickle.dumps({
            'session': sess.s.cookies._cookies,
            'selects': {k:[v[0],v[1].get()] for k,v in selects.items()}
        }))
    logvar.set('配置保存成功')
    messagebox.showinfo('保存成功','在选课开始后，运行 xk_run 来开始抢课。')

upf=Frame(tk)
upf.grid(row=0,column=0,sticky='we',pady=2,padx=2)
upf.columnconfigure(6,weight=1)

Label(upf,text=' 用户名 ').grid(row=0,column=0)
unentry=Entry(upf,textvariable=unvar)
unentry.grid(row=0,column=1)

Label(upf,text=' 密码 ').grid(row=0,column=2)
pwentry=Entry(upf,textvariable=pwvar,show='*')
pwentry.grid(row=0,column=3)

Label(upf,text=' 网址 ').grid(row=0,column=4)
baseentry=Entry(upf,textvariable=basevar)
baseentry.grid(row=0,column=5)

Label(upf,text=' ').grid(row=0,column=6,sticky='we')
loginbtn=Button(upf,text='登录',command=login)
loginbtn.grid(row=0,column=7)

Label(tk,textvariable=titlevar,font='黑体 -18').grid(row=1,column=0,padx=5)

book=Notebook(tk)
book.grid(row=2,column=0,sticky='nswe')

downf=Frame(tk)
downf.grid(row=3,column=0,sticky='we',pady=2,padx=2)
downf.columnconfigure(1,weight=1)

savebtn=Button(downf,text='保存',command=save)
savebtn.state(['disabled'])
savebtn.grid(row=0,column=0)
Label(downf,textvariable=logvar).grid(row=0,column=1,padx=5,sticky='we')

sess=CmsSession(log)
mainloop()
