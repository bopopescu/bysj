# 爬取西刺上高匿ip代理
import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="bid_spider", charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    # 爬取西刺的免费ip并且加入数据库
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
    }
    for i in range(1, 5):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()
            ip = all_texts[0]
            port = all_texts[1]
            # proxy_type = all_texts[5]
            insert_sql = """
              insert into proxy_ip(ip, port, speed,proxy_type) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE speed=VALUES (speed),
              port=VALUES (port)
            """
            cursor.execute(insert_sql,(ip,port,speed,"HTTP"))
            conn.commit()


# 从数据库中取得一个有效的ip
class GetIP(object):
    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = "delete from proxy_ip where ip='{0}'".format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url  = "https://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalide ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalide ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据表中随机获取一个可用的ip
        random_sql = """
        SELECT ip,port FROM proxy_ip ORDER BY rand() LIMIT 1
        """
        cursor.execute(random_sql)
        conn.commit()
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == "__main__":
    crawl_ips()
    get_ip = GetIP()
    get_ip.get_random_ip()