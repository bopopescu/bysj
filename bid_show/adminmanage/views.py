from django.shortcuts import render
from elasticsearch import Elasticsearch
# Create your views here.
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import redis
from .models import BidTable, ProvinceTable, IndustryTable,AuthUser
STORE_PIC_PATH = "E:/pywork/bysj/bid_show/static/pic"
client = Elasticsearch(hosts=["127.0.0.1"])
redis_cli = redis.StrictRedis("localhost")

# 词云显示
def getWordCloud():
    response = BidTable.objects.values_list("title")
    words = "".join(word[0] for word in response)
    text = " ".join(jieba.cut(words, cut_all=True))
    wc = WordCloud(background_color='white',  # 设置背景颜色
                   font_path='simsun.ttc', #必须指明中文字体位置
                   # mask=backgroud_Image,  # 设置背景图片
                   max_words=2000,  # 设置最大现实的字数
                   # stopwords=STOPWORDS,  # 设置停用词
                   # max_font_size=50,  # 设置字体最大值
                   random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                   )
    my_wordcloud = wc.generate(text)
    my_wordcloud.to_file(STORE_PIC_PATH+"/word.png")


def getIindustryTrend(request):
    # key_word = request.GET.get("q", "")
    key_words = request.GET.get('q', "")
    print(key_words)
    response = client.search(
        index="bid_spider",
        doc_type="bid_table",
        body={
            "query": {
                "multi_match": {  # multi_match查询
                    "query": key_words,  # 查询关键词
                    "fields": ["title", "content", "industry", "province"]  # 查询字段
                }
            },
            "from": 0,  # 从第几条开始获取
            "size": 9999,  # 获取多少条数据
        }
    )
    month_list = []
    y_list = []
    ycount_list = {}
    for hit in response["hits"]["hits"]:
        if hit["_source"]["publish_date"][:7] not in month_list:
            month_list.append(hit["_source"]["publish_date"][:7])
            ycount_list[hit["_source"]["publish_date"][:7]] = 1
        else:
            ycount_list[hit["_source"]["publish_date"][:7]] = ycount_list[hit["_source"]["publish_date"][:7]] + 1
    month_list.sort()
    for time in month_list:
        y_list.append(ycount_list[time])
    # 绘制折线图
    plt.xlabel(u"时间", fontproperties='SimHei')
    plt.ylabel(u"数量", fontproperties='SimHei')
    plt.title(key_words+u"变化折线图", fontproperties='SimHei')
    plt.plot(month_list, y_list)
    plt.savefig(STORE_PIC_PATH + "/trend.png")
    return HttpResponse(STORE_PIC_PATH+"/trend.png")


#管理员登录验证
@csrf_exempt
def adminlogin(request):
    errors = []
    account = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('用户名不能为空')
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors.append('密码不能为空')
        else:
            password = request.POST.get('password')

        if account is not None and account == 'admin' and password is not None:
            user = auth.authenticate(username=account, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('adminindex.html?user='+account)
                else:
                    errors.append('用户名错误')
            else:
                errors.append('用户名或密码错误')
    return render(request, 'adminmanage/adminlogin.html')


    # return render(request, "")
def adminindex(request):
    account = request.GET.get("user", "")
    provinces = ProvinceTable.objects.all()
    industry = IndustryTable.objects.all()
    user = AuthUser.objects.all()
    context = {
        "provinces": provinces,
        "industry": industry,
        "user": len(user)
    }
    getWordCloud()
    if account == "":
        return HttpResponseRedirect("/adminmanage")
    else:
        return render(request, "adminmanage/adminindex.html", context=context)