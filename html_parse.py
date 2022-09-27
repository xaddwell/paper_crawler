# file_name:html_parse.py
# 解析方法一
from bs4 import BeautifulSoup
import urllib3
import json
from get_html import get_html
from Paper_class import security_Paper
from utils import validateTitle,save_to_file
import pandas as pd
import warnings
import requests
import io
import os

warnings.filterwarnings('ignore')
root_dir = os.getcwd()

def list2csv(columns = ["paper_title","author","paper_link","pdf_link","slides_link","abstract"],list = None,name=None):
    pd_DataFrame = pd.DataFrame(columns=columns, data=list)
    pd_DataFrame.to_csv(root_dir+name+".csv",encoding='utf-8')


def download_content(url):
    """
    第一个函数，用来下载网页，返回网页内容
    参数 url 代表所要下载的网页网址。
    整体代码和之前类似
    """
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    response_data = response.data
    html_content = response_data.decode()
    return html_content

# 输入参数为要分析的 html 文件名，返回值为对应的 BeautifulSoup 对象
def create_doc_from_html(html_content):
    doc = BeautifulSoup(html_content)
    return doc

def create_doc_from_filename(filename):
    with open(root_dir + "/"+ filename, "r", encoding='utf-8') as f:
        html_content = f.read()
        doc = BeautifulSoup(html_content)
    return doc

def security_list_parse(doc,tag="h2",class_="node-title"):
    link_list = doc.body.find_all(tag,class_=class_)
    link_paper = []
    for link in link_list:
        temp = link.find_all("a")
        if len(temp)!=0:
            link_paper.append((paper_dict["security"]+temp[0]['href'],temp[0].text))

    return link_paper

def security_single_parse(link):
    temp_content = create_doc_from_html(download_content(link))
    temp_content = create_doc_from_html(str(temp_content.find_all("section", id="content")))
    title = temp_content.find_all("h1", id="page-title")
    author = temp_content.find_all("div", class_="field-name-field-paper-people-text")
    abstract = temp_content.find_all("div", class_="field-name-field-paper-description")
    pdf_link = temp_content.find_all("div", class_="field-name-field-presentation-pdf")
    slide_link = temp_content.find_all("div", class_="field-name-field-paper-slides-file")

    return security_Paper(paper_title=title,abstract=abstract,pdf_link=pdf_link,author=author,slides_link=slide_link,paper_link=link)


def download_pdf(save_path,pdf_name,pdf_url):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    response = requests.get(pdf_url, headers=send_headers)
    bytes_io = io.BytesIO(response.content)
    os.chdir(save_path)
    if not os.path.exists("%s.PDF" % pdf_name):
        with open("%s.PDF" % pdf_name, mode='wb') as f:
            f.write(bytes_io.getvalue())
    else:
        print("已存在")
    os.chdir(root_dir)
    print('%s.PDF,下载成功！' % (pdf_name))

def new_file(root_dir,name):
    os.chdir(root_dir)
    if not os.path.exists(name):
        os.mkdir(name)
    os.chdir(name)
    path = os.getcwd()
    os.chdir(root_dir)
    return path


# security的历年论文https://www.usenix.org/conferences/byname/108

paper_dict = {"security":"https://www.usenix.org/"}
conference_url = {"security22_fall":"https://www.usenix.org/conference/usenixsecurity22/fall-accepted-papers",
                  "security22_summer":"https://www.usenix.org/conference/usenixsecurity22/summer-accepted-papers",
                  "security21_fall":"https://www.usenix.org/conference/usenixsecurity21/fall-accepted-papers",
                  "security21_summer":"https://www.usenix.org/conference/usenixsecurity21/summer-accepted-papers",
                  "security20_fall":"https://www.usenix.org/conference/usenixsecurity20/fall-accepted-papers",
                  "security20_summer":"https://www.usenix.org/conference/usenixsecurity20/summer-accepted-papers",
                  "security20_spring":"https://www.usenix.org/conference/usenixsecurity20/spring-accepted-papers",
                  "security19_fall":"https://www.usenix.org/conference/usenixsecurity19/fall-accepted-papers",
                  }

if __name__ == '__main__':
    use_history = True
    name = "security21"
    pdf_save_path = new_file(root_dir=root_dir+"/pdf_info",name=name)
    url = conference_url[name]

    if not use_history:
        get_html(name=name, url=url)
        result = download_content(url)
        save_to_file(root_dir + "/history_file/" + name + ".html", result)
        doc = create_doc_from_html(result)
    else:
        doc = create_doc_from_filename("history_file/"+name+".html")

    link_paper = security_list_parse(doc)
    paper_info_list = []
    pdf_link_list = []
    for link, paper_name in link_paper:
        print(paper_name)
        paper = security_single_parse(link)
        if paper.paper_title !="":
            paper_info_list.append([paper.paper_title,paper.author,
                                    paper.paper_link,paper.pdf_link,
                                    paper.slides_link,paper.abstract])
            if paper.pdf_link != None:
                download_pdf(pdf_save_path, validateTitle(paper.paper_title), paper.pdf_link)

    # list2csv(list=paper_info_list,name="/paper_info/"+name)
    # for title, link in pdf_link_list:
    #     download_pdf(pdf_save_path,title,link)

