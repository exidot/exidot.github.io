
import os

from bs4 import BeautifulSoup


base_path = r'D:/资料/书籍/gg/道具篇V1.0/'
hhc_path = r'D:\资料\书籍\gg\道具篇V1.0\小黄书-道具篇V1.0.hhc'
doc_path = r'D:\资料\书籍\gg\道具篇V1.0\DNF教程目录'


hhc_fp = open(hhc_path, 'r')
hhc_data = hhc_fp.read()
hhc_fp.close()

hhc_bs = BeautifulSoup(hhc_data, 'html.parser')
hhc_list = hhc_bs.select('body param[name=Local]')

def parse_index(f: str):
    p = os.path.dirname(f)
    n = os.path.basename(f)
    return {
        'menu': p,
        'name': n.replace('.htm', ''),
        'path': f
    }

def search_files(path):
    files = []
    sub_paths = [os.path.join(path, f) for f in os.listdir(path)]
    for sub_path in sub_paths:
        if os.path.isfile(sub_path):
            p = os.path.abspath(sub_path)
            p = p.replace('\\', '/')
            p = p.replace(base_path, '')
            files.append(p)
        elif os.path.isdir(sub_path):
            files.extend(search_files(sub_path))
    return files

def handle(indexs):
    data = []
    data_i = []
    for index in indexs:
        menu = index['menu']
        if menu not in data_i:
            data.append({
                'menu': menu,
                'item': []
            })
            data_i.append(menu)
        i = data_i.index(menu)
        data[i]['item'].append(index)
    return data

def write_file(data, fn):
    index_fp = open(fn, 'w', encoding='utf-8')
    index_fp.write('<!DOCTYPE HTML>\n<html>\n<body>\n')
    for index in data:
        index_fp.write('  <div>{}</div>\n'.format(index['menu']))
        index_fp.write('  <ul>\n')
        for item in index['item']:
            index_fp.write('    <li>\n')
            index_fp.write('      <a href="{}">{}</a>\n'.format(item['path'], item['name']))
            index_fp.write('    </li>\n')
        index_fp.write('  </ul>\n')
    index_fp.write('</html>\n</body>\n')

    index_fp.close()

# 通过chm目录解析的索引
indexs = []
for v in hhc_list:
    indexs.append(v.attrs.get('value'))
index_items = [parse_index(f) for f in indexs]
index_data = handle(index_items)
write_file(index_data, 'index.html')

# 通过文档文件夹解析的索引
doc_files = search_files(doc_path)
doc_items = [parse_index(f) for f in doc_files]
doc_data = handle(doc_items)
write_file(doc_data, 'doc.html')


"""
下面是处理每个 htm 文档, 包括编码(utf-8), 显示下拉条
document.write("<style>\n");
document.write("body {overflow: hidden;}\n");
document.write("#winchm_template_container {position: absolute;overflow: auto;}\n");
document.write("</style>\n");

<div id="winchm_template_navigation">Help
<div id="winchm_template_navigation"><a href="index.html">Help</a>

"""

fs = [
    r'D:\资料\书籍\gg\道具篇V1.0\DNF教程目录',
    r'D:\资料\书籍\gg\技能篇\DNF教程目录',
    r'D:\资料\书籍\gg\台服百科全书V1.8\DNF教程目录',
    r'D:\资料\书籍\gg\装备篇\装备属性相关'
]

def find_docs(path):
    files = []
    sub_files = os.listdir(path)
    for sub_file in sub_files:
        sub_path = os.path.abspath(os.path.join(path, sub_file))
        if os.path.isdir(sub_path):
            files.extend(find_docs(sub_path))
        elif os.path.isfile(sub_path) and sub_path.endswith('.htm') and not sub_path.startswith('_new_'):
            files.append(sub_path)
    return files

doc_files = []
for f in fs:
    doc_files.extend(find_docs(f))


old_files = []
new_files = []
for f in doc_files:
    fp = open(f, 'r', encoding='utf-8')
    fdata = fp.read()
    fp.close()
    p = os.path.dirname(f)
    fn = os.path.basename(f)
    new_file = os.path.join(p, '_new_'+fn)
    fp = open(new_file, 'w', encoding='utf-8')
    fdata = fdata.replace(r' "-//W3C//DTD HTML 4.01 Transitional//EN"', '')
    fdata = fdata.replace(r'<meta name="GENERATOR" content="WinCHM">', '')
    fdata = fdata.replace(r'<meta http-equiv="Content-Type" content="text/html; charset=gb2312">', '')
    fdata = fdata.replace(r'document.write("<style>\n");', '')
    fdata = fdata.replace(r'document.write("body {overflow: hidden;}\n");', '')
    fdata = fdata.replace(r'document.write("#winchm_template_container {position: absolute;overflow: auto;}\n");', '')
    fdata = fdata.replace(r'document.write("</style>\n");', '')
    fdata = fdata.replace(r'<div id="winchm_template_navigation">Help', r'<div id="winchm_template_navigation"><a href="index.html">Help</a>')
    # fdata = fdata.replace(r'<div id="winchm_template_navigation"><a href="index.html">Help</a>', r'<div id="winchm_template_navigation"><a href="https://exidot.github.io/">Help</a>')
    fp.write(fdata)
    fp.close()
    old_files.append(f)
    new_files.append(new_file)

for f in old_files:
    os.remove(f)

for f in new_files:
    os.rename(f, os.path.join(os.path.dirname(f), os.path.basename(f).replace('_new_', '')))
