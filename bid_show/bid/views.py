from django.shortcuts import render
from django.http import HttpResponse
from .models import BidTable, IndustryTable, ProvinceTable, BidType, AuthUser
import json
import re
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
from datetime import datetime
import redis
client = Elasticsearch(hosts=["127.0.0.1"])
redis_cli = redis.StrictRedis("localhost")
STORE_PIC_PATH = "E:/pywork/bysj/bid_show/static/pic"


# 获取查询结果
def get_query_list(key_words, page):
    provinces = ProvinceTable.objects.all()
    industrylist = IndustryTable.objects.all()
    redis_cli.zincrby("search_keyword_set", key_words)
    topn_words = redis_cli.zrevrangebyscore("search_keyword_set", "+inf", "-inf", start=0, num=10)
    start_time = datetime.now()
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
            "from": (page-1)*10,  # 从第几条开始获取
            "size": 10,  # 获取多少条数据
            "highlight": {  # 查询关键词高亮处理
                "pre_tags": ['<em class="keyword">'],  # 高亮开始标签
                "post_tags": ['</em>'],  # 高亮结束标签
                "fields": {  # 高亮设置
                    'title': {},  # 高亮字段
                    'content': {}  # 高亮字段
                }
            }
        }
    )
    end_time = datetime.now()
    last_seconds = (end_time-start_time).total_seconds()
    total_nums = response["hits"]['total']
    if (page%10) > 0:
        page_nums = int(total_nums/10)+1
    else:
        page_nums = int(total_nums/10)
    hits_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        if "highlight" in hit and "title" in hit["highlight"]:
            hit_dict["title"] = "".join(hit["highlight"]["title"])
        else:
            hit_dict["title"] = "".join(hit["_source"]["title"])
        hit_dict['titleurl'] = "".join(hit["_source"]["title"])
        if "highlight" in hit and "content" in hit["highlight"]:
            hit_dict["content"] = "".join(hit["highlight"]["content"])[:200]
        else:
            hit_dict["content"] = hit["_source"]["content"][:200]
        if re.match("(.*)<e", hit_dict["content"]):
            hit_dict["content"] = re.match("(.*)<e", hit_dict["content"]).group(1)
        hit_dict["publish_date"] = hit["_source"]["publish_date"][:10]
        hit_dict["industry"] = hit["_source"]["industry"]
        hit_dict["fund"] = hit["_source"]["fund"]
        hit_dict["region"] = hit["_source"]["region"]
        hit_dict["url"] = hit["_source"]["url"]
        hit_dict["dead_date"] = hit["_source"]["dead_date"][:10]
        if hit_dict["dead_date"] == "2100-01-01":
            hit_dict["dead_date"] = "未知"
        hit_dict["score"] = hit["_score"]
        hits_list.append(hit_dict)
    all_hits = sorted(hits_list, key=lambda hits_list_dict: hits_list_dict["publish_date"],reverse=True)
    context = {
        "all_hits": all_hits,
        "key_word": key_words,
        'industrylist': industrylist,
        'provinces': provinces,
        'total_nums': total_nums,
        'last_seconds': last_seconds,
        'page_nums': page_nums,
        'page': page,
        'topn_words': topn_words
    }
    return context, response["hits"]["hits"]


def drawpicture(request):
    key_words = request.GET.get('q', "")
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
    plt.savefig(STORE_PIC_PATH+"/a.jpg")
    plt.show()
    # 绘制柱状图
    plt.xlabel(u"时间", fontproperties='SimHei')
    plt.ylabel(u"数量", fontproperties='SimHei')
    plt.title(key_words+u"数量统计柱状图", fontproperties='SimHei')
    plt.bar(month_list, y_list, facecolor='blue', edgecolor='white')
    for x, y in zip(month_list, y_list):
        plt.text(x, y, y, ha='center', va='bottom')
    plt.savefig(STORE_PIC_PATH + "/b.jpg")
    plt.show()
    return HttpResponse("/a.jpg")


@csrf_exempt
def index(request):
    if request.method == "POST":
        proitem = request.POST.get("province", "")
        inditem = request.POST.get("industry", "")
        starttime = request.POST.get("starttime", datetime.now())
        endtime = request.POST.get("endtime", datetime.now)
        if proitem == "所有省份":
            proitem = ""
        if inditem == "所有行业":
            inditem = ""
        key_words =proitem+inditem+request.POST.get("search", "")
        page = 1
        context, datacontext = get_query_list(key_words, page)
        context['starttime'] = starttime
        context['endtime'] = endtime
        # drawpicture(datacontext)
        return render(request, "bid/index.html", context=context)
    else:
        # account = request.GET.get("account", "")
        industry = request.GET.get("industry", "")
        page = request.GET.get("p", "1")
        key_words = request.GET.get("q", "1")
        if key_words == "1":
            key_words = industry
        try:
            page = int(page)
        except:
            page = 1
        # if account == "":
        #     return HttpResponseRedirect("/")
        # else:
        context, datacontext = get_query_list(key_words, page)
        # drawpicture(datacontext)
        return render(request, "bid/index.html", context=context)


# 这里实现的是搜索提示补全功能
def suggest(request):
    key_words = request.GET.get('q', "")
    re_datas = []
    if key_words:
        s = BidType.search()
        s = s.suggest(
            'my_suggest',
            key_words,
            completion={
                "field": "suggestion",
                "fuzzy": {
                    "fuzziness": 2
                },
                "size": 10
            })
        suggestions = s.execute()
        for match in suggestions.suggest.my_suggest[0].options:
            source = match._source
            re_datas.append(source['title'])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")
    # return render(request, "bid/index.html")

# @csrf_exempt
# def test(request):
#     if request.method == "POST":
#         proitem = request.POST.get("province", "")
#         inditem = request.POST.get("industry", "")
#         if proitem == "省份":
#             proitem = ""
#         if inditem == "行业":
#             inditem = ""
#         key_words = request.POST.get("search", "")+proitem+inditem
#         page = request.GET.get("p", "1")
#         try:
#             page = int(page)
#         except:
#             page = 1
#         context, datacontext = get_query_list(key_words, page)
#         drawpicture(datacontext)
#         # return render(request, "bid/index.html", context=context)
#         return render(request, "bid/test.html", context=context)
#     else:
#         page = int(request.GET.get('p', 1))
#         context, datacontext = get_query_list("江苏", page)
#         drawpicture(datacontext)
#         # return render(request, "bid/index.html", context=context)
#         return render(request, "bid/test.html", context=context)
#         # return HttpResponse(json.dumps(context), content_type="application/json")
