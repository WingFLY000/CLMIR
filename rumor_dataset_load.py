from lxml import etree
from selenium import webdriver
import requests
import time
import re
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
## 把驱动放在当前的文件夹中
bro =  webdriver.Edge(executable_path='./msedgedriver.exe')##打开浏览器后手动登陆weibo
# WebDriverWait(bro, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "m_table_tit")))

# os.mkdir('rumorJson')

for j in range(206,216):##选择要爬取的页面编号
    url = 'https://service.account.weibo.com/?type=5&status=4&page=' + str(j) ##页面编号组合成完整的url
    fp = open('./rumorJson/'+str(j)+'.json','w',encoding='utf-8')                  ##打开新建一个json来存储信息
    bro.get(url=url)                                                               ##抓取第一层页面
    page_text = bro.page_source
    tree = etree.HTML(page_text)
    trlist = tree.xpath('//div[@id="pl_service_showcomplaint"]//tr')[1:]           ##获取一页20条目的列表
    for i in range(20):                                                            ##从条目中获取谣言信息：一部分信息直接从第一层获取，像正文之类的要
        title = (trlist[i].xpath('.//div[@class="m_table_tit"]/a/text()')[0])#title
        rumorCode = (trlist[i].xpath('.//div[@class="m_table_tit"]/a/@href')[0].split('=')[-1])#rumorcode
        informerName = (trlist[i].xpath('./td[3]/a/text()')[0])#informerName
        informerUrl = (trlist[i].xpath('./td[3]/a/@href')[0])#informerUrl
        rumormongerName = (trlist[i].xpath('./td[4]/a/text()')[0])#rumorerName
        rumormongerUrl = (trlist[i].xpath('./td[4]/a/@href')[0])#rumorerUrl
        bro.get(url='https://service.account.weibo.com/show?rid='+trlist[i].xpath('.//div[@class="m_table_tit"]/a/@href')[0].split('=')[-1])##通过rumorCode组成第二层点进去爬取
        subBroResTree = etree.HTML(bro.page_source)
        #rumorContext
        if subBroResTree.xpath('//*[@id="pl_service_common"]/div[4]/div[2]/div/div/div/div/p/a/text()')==['原文']:                          ##若有原文,则点进原文链接进行爬取
            bro.get(subBroResTree.xpath('//*[@id="pl_service_common"]/div[4]/div[2]/div/div/div/div/p/a/@href')[0])
            time.sleep(1)##需要等待页面加载完成！！
            subSubBroResTree = etree.HTML(bro.page_source)
            rumorText = (subSubBroResTree.xpath('//div[@class = "detail_wbtext_4CRf9"]//text()'))
            #print("需要第三层")
        elif subBroResTree.xpath('//*[@id="pl_service_common"]/div[4]/div[2]/div/div/div/div/div/div/a[2]/text()') == ['查看全文'] or subBroResTree.xpath('//*[@id="pl_service_common"]/div[4]/div[2]/div/div/div/div/div/div/a[3]/text()')==['查看全文']:
            rumorText = (subBroResTree.xpath('//div[@class="feed bg_orange2 clearfix"]/div/input/@value'))                                  ##若表示不全,则有一个查看全文的标签
            #print("要查看全文")
        else:
            rumorText = (subBroResTree.xpath('//div[@class="feed bg_orange2 clearfix"]/div/text()'))                                        ##直接表示
            #print("不用查看全文")
        result = (subBroResTree.xpath('//div[@class="middle middle_long"]/p/text()'))#rumorExplain
        visitTimes = (trlist[i].xpath('./td[5]/text()')[0])#rumorerVisit
        publishTime = (trlist[i].xpath('./td[6]/text()')[0])#rumorSubmitTime


        rumorTextStr = ''                                                                                                                   ##对谣言正文进行数据初步清洗
        rumorTextStr = rumorTextStr.join(rumorText)
        rumorTextStr = rumorTextStr.replace(u'\u200b',u'')


        resultStr = ''
        resultStr = resultStr.join(result)
        resultStr = resultStr.replace(u'\u200b',u'')                                                                                        ##对谣言解释进行数据初步清洗
        jsonList = {'rumorCode':rumorCode,                                                                                                  ##每一个谣言组成一个json文件
                    'title':title,
                    'informerName':informerName,
                    'informerUrl':informerUrl,
                    'rumormongerName':rumormongerName,
                    'rumormongerUrl':rumormongerUrl,
                    'rumorText':rumorTextStr,
                    'visitTimes':visitTimes,
                    'result':resultStr,
                    'publishTime':publishTime}
        jjson = json.dumps(jsonList,ensure_ascii=False)

        fp.write(jjson)                                                                                                                     ##把json写入文件内
        fp.write('\n')
    fp.close()