# 测试re
import re

content = "江苏省-苏州市"
# print(content)
match_obj = "(.*省)"
ans = re.match(match_obj, content, re.DOTALL)
# print(content)
bid_id = " "
if ans:
    # print("1")
    bid_id = str(ans.group(2))
# print(bid_id)
print(bid_id)
