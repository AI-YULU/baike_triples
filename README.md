# baike_triples
爬取百度百科词条，抽取三元组，构建知识图谱

1.首先运行spider/spider_main迭代地抓取原始词条的网页,爬取的html文件放到spider/webpages文件夹里面

2.运行ie/extract-table.py进行网页的解析，并将每个词条的信息存入txt文件，放到info-table文件夹里面

3.运行kg/build-triple-from-triple.py生成三元组文件triples.txt,放到kg/triple.txt里面

4.运行insert_to_neo4j.py将三元组存入neo4j数据库
