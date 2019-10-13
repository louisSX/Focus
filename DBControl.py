import time
from MySqlTools import MySqlTools

class DBControl():

    # 获取行业表中的各行业地址
    def getHY_URLS(self):
        # 获取数据库中各行业地址
        mst = MySqlTools()
        sql = 'select * from hy_url'
        data = mst.db_query(sql)
        mst.db_close()
        return data

    # 更新行业表中的爬虫时间
    def updateHY_URL(self,hy_url):
        today = time.strftime("%Y%m%d")
        sql = 'UPDATE hy_url SET pc_time = %s where hy_url = %s'
        args = (today,hy_url)
        mst = MySqlTools()
        result = mst.db_update(sql,args)
        mst.db_close()
        return result

    # 删除昨日爬虫数据
    def deleteGW_XinXi(self,hy_url):
        sql = "delete from gw_xinxi where hy_url = '" + hy_url + "'"
        mst = MySqlTools()
        mst.db_delete(sql)
        mst.db_close()

    # 先判断是否存在链接，如果存在则更新，如果不存在则新增
    # 引用此方法时，参数args为Tuple对象
    def updateGW_XinXi(self,args):
        update_sql = 'update gw_xinxi set gw_danwei = %s,gw_mingcheng = %s,gw_miaoshu = %s,gw_xinchou = %s,gw_dizhi = %s,gw_biaoqian = %s,hy_type = %s,pc_time = %s where gw_url = %s'
        insert_sql = 'INSERT INTO gw_xinxi(gw_danwei, gw_mingcheng, gw_miaoshu,gw_xinchou,gw_dizhi,gw_biaoqian,hy_type,pc_time,gw_url) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        mst = MySqlTools()
        data = mst.db_query("select * from gw_xinxi where gw_url='" + args[8] + "'")
        if len(data) == 0:
            result = mst.db_insert(insert_sql,args)
            print('新增')
        else:
            result = mst.db_update(update_sql, args)
            print('替换')
        mst.db_close()
        return result

    # 判断指定行业是否可以更新
    def insertAvailable(self,hy_url):
        today = time.strftime("%Y%m%d")
        sql = "select * from hy_url where hy_url = '" + hy_url + "'"
        mst = MySqlTools()
        data = mst.db_query(sql)
        updatetime = data[0][1]
        mst.db_close()
        if today == updatetime:
            return False
        else:
            return True