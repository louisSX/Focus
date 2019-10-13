import requests
from bs4 import BeautifulSoup
from DBControl import DBControl
from MySqlTools import MySqlTools

# url = "https://xj.58.com/zplvyoujiudian/"
# r = requests.get(url)
# html = r.text
# bs = BeautifulSoup(html, "lxml")
# # print(bs)
# temp = bs.find(name='i',attrs={'class': 'total_page'})
# num = int(temp.get_text())
# print(num)
# print(type(num))

# url ="https://short.58.com/zd_p/e2981abd-2a7d-464a-8f34-311385838e4d/?target=qc-16-xgk_hwnlagvcjvujmo_89370104133628q-feykn&end=end&psid=118647408205886167832676059&entinfo=36217570522893_m&ytdzwdetaildj=0&finalCp=finalCp=000001280000000000050000000000000000_118647408205886167832676059&tjfrom=pc_list_left_tt__118647408205886167832676059__81441651814006784__mqtt"
# r = requests.get(url)
# html = r.text
# bs = BeautifulSoup(html,'lxml')
# print(bs.title.string[0:6])

# mst = MySqlTools()
# data = mst.db_query("select * from gw_xinxi where gw_url='" + "123" + "'")
# print(type(data))
# print(len(data))

str = 'https://xj.58.com/zplvyoujiudian/38837363343394x.shtml?psid=127421137205900574918387453&entinfo=38837363343394_j&ytdzwdetaildj=0&finalCp=finalCp=000001250000000000080000000000000000_127421137205900574918387453&tjfrom=pc_list_left_jp__127421137205900574918387453__81902678745776128__jp'
pos = 'xasdsadas' in str
print(pos)
print(str[0:54])