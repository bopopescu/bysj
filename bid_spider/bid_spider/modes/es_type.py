# 自定义es的模型，类似于django的models
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text,  Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl import connections
connections.create_connection(hosts=["localhost"])


class CustomerAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return []
    pass


ik_analyzer = CustomerAnalyzer("ik_max_word", filter=["lowercase"])


class BidType(DocType):
    suggestion = Completion(analyzer=ik_analyzer)
    industry = Text()
    title = Text(analyzer="ik_max_word")
    fund = Text()
    url = Keyword()
    region = Text()
    publish_date = Date()
    content = Text(analyzer="ik_max_word")
    bid_id = Text()
    dead_date = Date()

    class Meta:
        index = "bid_spider"
        doc_type = "bid_table"


if __name__ == "__main__":
     BidType.init()
