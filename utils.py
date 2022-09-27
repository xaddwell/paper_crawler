import re

def validateTitle(title):
    # 创建合法文件名
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def save_to_file(filename, content):
    fo = open(filename, "w", encoding="utf-8")
    fo.write(content)
    fo.close()