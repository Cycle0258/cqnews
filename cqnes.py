import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import sys
import urllib3
import time

# 屏蔽 LibreSSL 警告，保持终端整洁
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.cbg.cn"
LIST_URL_TEMPLATE = "https://www.cbg.cn/list/4928/{page}.html" 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def parse_date(date_str):
    """提取 '2026-04-24 20:01' 中的日期部分"""
    date_str = date_str.strip()
    return date_str.split(" ")[0] if " " in date_str else date_str

def get_news_list_by_date(target_date_str, limit_pages=150):
    """
    深度暴力检索模式：不找齐不罢休
    """
    news_items = []
    page = 1
    
    print(f"--- 开启深度检索：目标日期 {target_date_str} ---")

    while page <= limit_pages:
        url = LIST_URL_TEMPLATE.format(page=page)
        # 使用 \r 实现单行刷新显示进度
        print(f"正在扫描第 {page:03d} 页...", end='\r')
        
        try:
            # verify=False 兼容你的 LibreSSL 环境
            response = requests.get(url, headers=HEADERS, verify=False, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            items_in_page = soup.select('ul.news-list li')
            if not items_in_page:
                print(f"\n[提示] 第 {page} 页无内容，可能已达到网站末尾。")
                break
            
            found_in_this_page = False
            for li in items_in_page:
                time_span = li.select_one('span.time')
                if not time_span: continue
                
                current_item_date = parse_date(time_span.text.strip())
                
                if current_item_date == target_date_str:
                    a_tag = li.find('a')
                    news_items.append({
                        'title': a_tag.get('title'),
                        'url': a_tag.get('href')
                    })
                    found_in_this_page = True
            
            # 改进的停止判断：
            # 如果我们已经在之前的页面找到了新闻，但这一页一个都没找到，
            # 且这一页的第一条新闻日期已经比目标日期“老”了，才说明真的抓完了。
            if len(news_items) > 0 and not found_in_this_page:
                first_item_date = parse_date(items_in_page[0].select_one('span.time').text.strip())
                if first_item_date < target_date_str:
                    print(f"\n[OK] 目标日期内容抓取完毕。")
                    break
            
            page += 1
        except Exception as e:
            print(f"\n[错误] 扫描第 {page} 页时发生异常: {e}")
            break
            
    print(f"\n扫描结束。共计在 {page} 页中找到 {len(news_items)} 条新闻。")
    return news_items

def get_article_content(url):
    """进入详情页提取正文"""
    try:
        res = requests.get(url, headers=HEADERS, verify=False, timeout=20)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        content_div = soup.select_one('.article-content') or \
                      soup.select_one('.content') or \
                      soup.select_one('#content')
                      
        if content_div:
            # 剔除干扰元素
            for s in content_div(['script', 'style', 'video', 'iframe', 'canvas']):
                s.decompose()
            return content_div.get_text(separator='\n', strip=True)
    except:
        return "正文提取失败。"
    return "未找到正文内容。"

def run_task(input_date=None):
    if input_date:
        try:
            clean_date = input_date.replace('-', '').replace('/', '')
            dt = datetime.strptime(clean_date, "%Y%m%d")
            target_date_str = dt.strftime("%Y-%m-%d")
        except:
            print("日期格式错误，请使用 20260406 这种格式")
            return
    else:
        target_date_str = datetime.now().strftime("%Y-%m-%d")

    items = get_news_list_by_date(target_date_str)
    
    if not items:
        print(f"❌ 未能找到 {target_date_str} 的任何新闻，请尝试调大 limit_pages 或确认该日是否有节目。")
        return

    # 创建保存目录（建议改为你的 Obsidian 实际路径）
    save_dir = "Chongqing_News_History"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, f"{target_date_str}_新闻汇总.md")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# 重庆新闻联播文字稿 ({target_date_str})\n\n---\n\n")
        for idx, item in enumerate(items, 1):
            print(f"正在抓取详情 ({idx}/{len(items)}): {item['title']}")
            body = get_article_content(item['url'])
            f.write(f"## {item['title']}\n")
            f.write(f"- 原文: {item['url']}\n\n")
            f.write(f"{body}\n\n---\n\n")

    print(f"\n🎉 抓取成功！文件已保存至: {file_path}")

if __name__ == "__main__":
    user_param = sys.argv[1] if len(sys.argv) > 1 else None
    run_task(user_param)