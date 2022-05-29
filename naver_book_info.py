#-*- encoding: utf8 -*-

import os, json, urllib.parse, requests, re
import urllib.request

import xmltodict


client_id = "#" # 네이버 애플리케이션 등록시 발급 받은 값 입력
client_secret = "#" # 네이버 애플리케이션 등록시 발급 받은 값 입력


# makexml
xml = '''<?xml version="1.0"?>
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Title>{title}</Title>
  <Series>{title}</Series>
  <Summary>{desc}</Summary>
  <Writer>{author}</Writer>
  <Publisher>{publisher}</Publisher>
  <Genre></Genre>
  <Tags></Tags>
  <LanguageISO>ko</LanguageISO>
  <Notes>완결</Notes>
  <CoverArtist></CoverArtist>
  <Penciller></Penciller>
  <Inker></Inker>
  <Colorist></Colorist>
  <Letterer></Letterer>
  <CoverArtist></CoverArtist>
  <Editor></Editor>
  <Characters></Characters>
  <Year>{year}</Year>
  <Month>{month}</Month>
  <Day>{day}</Day>
</ComicInfo>'''

def change_info(str):
    return str.replace('<', '"').replace('>', '"').replace('&', '&amp;').strip()



print("\n============================================================================\n")



targetpath = os.getcwd()
get_folder = targetpath.split("\\")[-1]
search_title = re.sub("\[(.*?)\]", '', get_folder).strip()

get_author = re.search(r"\[(.+)\](.+)", get_folder)
if get_author:
    search_author = get_author.group(1)
    param_author = "&d_auth="+urllib.parse.quote(str(search_author))
else:
    search_author = ""
    param_author = ""


url = "https://openapi.naver.com/v1/search/book_adv.xml?display=100&sort=count&d_titl="+urllib.parse.quote(str(search_title))+param_author


request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()
data = response.read()
data = json.loads(json.dumps(xmltodict.parse(data)))


if(rescode==200):
    if data['rss']['channel']['total'] != '0':
        try:
            item = data['rss']['channel']['item'][0]
        except:
            item = data['rss']['channel']['item']

        entity = {}

        if item['title'] is not None:
            tmp_title = item['title'].replace('<b>', '').replace('</b>', '')
            entity['title'] = re.sub("\(.*?\)", '', tmp_title).strip()
        else:
            entity['title'] = search_title

        entity['publisher'] = item['publisher']
        entity['code'] = 'BN' + item['link'].split('bid=')[1]
        entity['pubdate'] = item['pubdate']

        try:
            entity['author'] = item['author'].replace('<b>', '').replace('</b>', '')
        except:
            entity['author'] = search_author

        entity['description'] = ''
        try:
            if item['description'] is not None:
                entity['description'] = item['description'].replace('<b>', '').replace('</b>', '')
        except:
            pass


        set_xml = xml.format(
            title = change_info(entity['title']),
            desc = change_info(entity['description']),
            author = change_info(entity['author']),
            publisher = change_info(entity['publisher']),
            year = entity['pubdate'][0:4],
            month = entity['pubdate'][4:6] if len(entity['pubdate']) > 4 else '01',
            day = entity['pubdate'][6:8] if len(entity['pubdate']) > 6 else '01',
        )

        f = open(os.path.join(targetpath, 'info.xml'), 'w', encoding='UTF-8')
        f.write(set_xml)
        f.close()


        print("title => "+entity['title']+"\n")
        print("author => "+entity['author']+"\n")
        print("code => "+entity['code']+"\n")
        print("pubdate => "+entity['pubdate']+"\n")
        print("publisher => "+entity['publisher']+"\n")
        print("description => "+entity['description'])



    else:
        print("실패")

else:
    print("Error Code:" + rescode)


print("\n============================================================================\n")

                    



