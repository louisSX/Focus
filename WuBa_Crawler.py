import requests
from bs4 import BeautifulSoup
from DBControl import DBControl
import time

class WuBa_Crawler():

    def __init__(self):
        dbc = DBControl()
        self.HYUrls = dbc.getHY_URLS()
        self.currentPage = ''
        self.currentHy_Type = ''

    def start(self):
        dbc = DBControl()
        # 遍历HYUrks，获得每个行业的地址
        for i in self.HYUrls:
            # 获取当前爬取的行业
            self.currentHy_Type = i[2]
            # 根据每个行业的地址生成每一页地址
            urls = self.__crawler_url_pages__(i[0])
            # 判断网页是否被拒绝
            if urls == False:
                return False
            # 根据具体的地址进行遍历，获取岗位信息
            for j in urls:
                self.currentPage = j
                result = self.__crawler_gw_url__(j)
                if result == False:
                    return False
            # 这里是更新行业表中的爬虫时间到最新时间
            dbc.updateHY_URL(i[0])

    # 根据行业URL，获取所有该行业岗位信息页数地址,返回一个地址集的list
    def __crawler_url_pages__(self,url):
        # 以下代码获取该行业网页总页数
        r = requests.get(url)
        html = r.text
        bs = BeautifulSoup(html,'lxml')
        state = self.__pageAvailable__(bs,url)
        if state == False:
            return False
        temp = bs.find(name='i',attrs={'class':'total_page'})
        num_str = temp.get_text()
        num = int(num_str)
        # 以下为每一页生成地址，合并成list，最后返回list
        index = 2
        urls = [url]
        for i in range(num - 1):
            urls.append(url + 'pn' + str(index))
            index = index + 1
        return urls

    # 根据行业URL，爬虫行业岗位列表中的岗位地址及岗位信息
    def __crawler_gw_url__(self,url):
        hy_url = url
        dbc = DBControl()
        # 以下操作开始爬虫并更新进数据库
        r = requests.get(hy_url)
        html = r.text
        bs = BeautifulSoup(html, "lxml")
        # 检查网页是否可以爬虫
        state = self.__pageAvailable__(bs,hy_url)
        if state == False:
            return False
        for i in bs.find_all(attrs={'class': 'job_name clearfix'}):
            gw_url = str(i.a['href'])
            if 'legoclick' in gw_url:
                continue
            if 'short' in gw_url:
                continue
            pos = gw_url.index('?')
            gw_url = gw_url[0:pos]
            # 根据给定的岗位信息地址，爬取岗位各项信息并存储到数据库中
            result = self.__crawler_gw_xinxi__(gw_url)
            if result == False:
                return False

    # 根据给定的岗位信息地址，爬取岗位各项信息并存储到数据库中
    def __crawler_gw_xinxi__(self,url):
        r = requests.get(url)
        html = r.text
        bs = BeautifulSoup(html, "lxml")
        # 检查是否被拒绝
        result = self.__pageAvailable__(bs,url)
        if result == False:
            return False
        # 获取岗位所属单位名称
        temp = bs.find(name='div',attrs={'class': 'baseInfo_link'})
        gw_danwei = temp.get_text()
        # 获取岗位名称
        temp = bs.find(name='span', attrs={'class': 'pos_title'})
        gw_mingcheng = temp.string
        # 获取岗位职责及要求
        temp = bs.find(name='div',attrs={'class': 'des'})
        gw_miaoshu = temp.get_text()
        # 获取岗位薪酬
        temp = bs.find(name='span',attrs={'class': 'pos_salary'})
        gw_xinchou = temp.get_text()
        # 获取岗位单位工作地址
        temp = bs.find(name='div',attrs={'class': 'pos-area'})
        temp = temp.find(name='span',attrs={'class':''})
        gw_dizhi = temp.string
        # 获取岗位标签
        temp = bs.find(name='div', attrs={'class': 'pos_welfare'})
        if temp == None:
            gw_biaoqian = ''
        else:
            gw_biaoqian = temp.get_text("|", strip=True)

        print("/n正在爬取岗位列表页：" + self.currentPage)
        print("/n正在爬取岗位详情页：" + url)
        args = (gw_danwei,gw_mingcheng,gw_miaoshu,gw_xinchou,gw_dizhi,gw_biaoqian,self.currentHy_Type,time.strftime("%Y%m%d"),url)
        dbc = DBControl()
        # 更新或新增岗位各项信息到数据库
        r = dbc.updateGW_XinXi(args)
        if r == 1:
            print('/n岗位详情保存成功！')
        else:
            print('/n岗位详情保存失败！')
        print('---------------------------------')

    # 判断网站是否拒绝爬虫
    def __pageAvailable__(self,bs,url):
        if bs.title.string[0:6] == '请输入验证码':
            print('访问频繁错误:' + url)
            return False
        else:
            return True