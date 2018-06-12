import pdfkit


# 将html保存成pdf,目前还没做完呐
def html_to_pdf(html_url, filename):
    pdfkit.from_url(html_url, filename+".pdf")