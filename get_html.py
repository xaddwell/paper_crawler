import urllib3

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


def save_to_file(filename, content):
    fo = open(filename, "w", encoding="utf-8")
    fo.write(content)
    fo.close()


def get_html(name,url):
    result = download_content(url)
    save_to_file("history_file/"+name+".html", result)


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
    for k,v in conference_url.items():
        get_html(name=k,url=v)
