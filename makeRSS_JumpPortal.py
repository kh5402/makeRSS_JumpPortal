import requests
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def main():
    base_url = "https://portal.jamp.jiji.com/portal/search?freeWord=AI"
    output_file = "makeRSS_JumpPortal.xml"
    events = []

    # 既存のXMLファイルがあれば読み込む
    if os.path.exists(output_file):
        tree = ET.parse(output_file)
        root = tree.getroot()
    else:
        # 新しくXMLを作成
        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")
        ET.SubElement(channel, "title").text = "JAMPポータルからの情報"
        ET.SubElement(channel, "description").text = "JAMPポータルからの情報を提供します。"
        ET.SubElement(channel, "link").text = "https://example.com"
        
    channel = root.find("channel")

    # HTMLの取得と解析
    response = requests.get(base_url)
    html_content = response.text

    article_pattern = re.compile(r'<li class="item">\s*<a href="([^"]+)">\s*([^<]+)<span class="date">([^<]+)<\/span>\s*<\/a>\s*<\/li>')

    for match in article_pattern.findall(html_content):
        link = "https://portal.jamp.jiji.com" + match[0]
        title = match[1]
        date = match[2]
        
        # 重複を避けるためにURLでチェック
        if not any(item.find("link").text == link for item in channel.findall("item")):
            new_item = ET.SubElement(channel, "item")
            ET.SubElement(new_item, "title").text = title
            ET.SubElement(new_item, "link").text = link
            ET.SubElement(new_item, "pubDate").text = date

    # XMLを出力
    xml_str = ET.tostring(root)
    xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
    with open(output_file, "w") as f:
        f.write(xml_pretty_str)

if __name__ == "__main__":
    main()
