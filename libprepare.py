#coding=utf-8
import requests
import pyquery

class CmsSession:
    def __init__(self,logger):
        self.s=requests.Session()
        self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2853.0 Safari/537.36'})
        self.l=logger
        self.base=None
        self.elid=None

    def login(self,base,un,pw):
        self.base = base

        self.l('正在加载登录页……')
        res=self.s.get(base + '/')
        res.raise_for_status()

        pq=pyquery.PyQuery(res.text)
        csrf_token=pq('form[action=\\/] input[name=__RequestVerificationToken]').val()

        self.l('正在登录……')
        res=self.s.post(base+'/', data=dict(
            __RequestVerificationToken=csrf_token,
            SchoolName='深圳龙创软件',
            UserCode=un,
            Password=pw,
            CheckCode='lcsb',
            CheckCodeRefer='lcsb',
            Remember='false',
        ))
        res.raise_for_status()
        assert res.json()['Status'] == 1, '登录失败'

        self.l('加载当前选课……')
        res=self.s.get(base+'/Elective/ElectiveInput/List')
        res.raise_for_status()

        pq=pyquery.PyQuery(res.text)
        cur_ele=pq('.panel-body h3.text-center')
        self.elid = int(cur_ele.find('a.btn').attr('href').partition('?electiveId=')[2])

        return cur_ele.contents()[0].strip()

    def details(self):
        self.l('加载时段列表……')

        res=self.s.get(self.base+'/Elective/ElectiveInputBySchedule/List', params=dict(electiveId=self.elid))
        res.raise_for_status()
        pq=pyquery.PyQuery(res.text)

        periods=pq('a[href^=\\/Elective\\/ElectiveOrg\\/Select]')
        for ind,period in enumerate(periods):
            self.l('加载选课详情 (%d/%d)……'%(ind+1,len(periods)))
            uri=period.attrib['href']

            res=self.s.get(self.base+uri)
            res.raise_for_status()

            pq=pyquery.PyQuery(res.text)
            csrf_token=pq('form input[name=__RequestVerificationToken]').val()
            res=[]
            for cls in pq('tr[class]'):
                columns=pq(cls).find('td')

                clsid=int(columns.find('input[name=rdoId]').val() or -666)
                clstitle=columns[2].text.strip()
                clsteacher=columns[4].text.strip()

                res.append([clsid,clstitle,clsteacher])

            yield uri,csrf_token,res
        self.l('完成')



