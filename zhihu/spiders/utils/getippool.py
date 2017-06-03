# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector
import MySQLdb

conn= MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='articlespider',
    charset='utf8',
    use_unicode=True)
cursor = conn.cursor()



def get_crawl_ips():
    #爬取西刺代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }

    # 遍历2000页的数据
    for i in range(2000):
        response = requests.get('http://www.xicidaili.com/nn/{0}'.format(i), headers=headers)
        # 获取selector用来解析网页内容
        selector = Selector(text=response.text)

        all_trs = selector.css('#ip_list tr')

        ip_list = []
        # all_trs[1:]去除表头
        for tr in all_trs[1:]:
            speed = tr.css('.bar::attr(title)').extract()[0]
            if speed:
                speed = float(speed.split('秒')[0])

            all_text = tr.css('td::text').extract()

            ip = all_text[0]
            port = all_text[1]
            proxy_type = all_text[5]

            ip_list.append((ip, port, proxy_type, speed))

            # print(ip_list)
            for ip_info in ip_list:
                insert_sql = "insert into proxy_ip(ip, port, speed, proxy_type) values(%s,%s,%s,%s)"
                cursor.execute(insert_sql, (ip_info[0], ip_info[1], ip_info[3], ip_info[2]))
                conn.commit()


class GetIp(object):

    def delete_ip(self,ip):
        # 从数据库中删除无效的ip
        delete_sql = """delete from proxy_ip where ip='{0}'""".format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True


    def check_ip_use(self, ip, port):
        print('check_ip_use...........')
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip,port)
        try:
            proxy_dict = {
                'http': proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
            return True
        except Exception as e:
            print('invalid ip and port')
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print('useful ip')
                return True
            else:
                print('invalid ip and port')
                self.delete_ip(ip)
                return False


    def getRandomIp(self):
        # 从数据库中随机获取一个ip
        random_sql = "select ip,port from proxy_ip order by rand() limit 1"

        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            check_result = self.check_ip_use(ip, port)
            print("check_result is :"+str(check_result))
            if check_result:
                return 'http://{0}:{1}'.format(ip,port)
            else:
                return self.getRandomIp()

# get_crawl_ips()

getip = GetIp()
print(getip.getRandomIp())
# print(getip.delete_ip('175.155.24.17'))

