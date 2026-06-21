import feedparser
import json
from datetime import datetime

def load_feeds():
    with open('feeds.json', 'r') as f:
        return json.load(f)['feeds']

def fetch_feed(feed):
    try:
        parsed = feedparser.parse(feed['url'])
        entries = []
        for entry in parsed.entries[:10]:
            summary = entry.get('summary', entry.get('description', ''))
            title = entry.get('title', '')
            link = entry.get('link', '')
            published = entry.get('published_parsed') or entry.get('updated_parsed')
            
            if published:
                pub_date = datetime(*published[:6]).isoformat()
            else:
                pub_date = datetime.now().isoformat()
            
            content = (title + ' ' + summary).lower()
            if any(kw.lower() in content for kw in feed.get('keywords', [])) or not feed.get('keywords'):
                entries.append({
                    'title': title,
                    'link': link,
                    'summary': summary[:300] + '...' if len(summary) > 300 else summary,
                    'published': pub_date,
                    'source': feed['name']
                })
        return entries
    except Exception as e:
        print(f"Error fetching {feed['name']}: {e}")
        return []

def main():
    feeds = load_feeds()
    all_news = []
    
    for feed in feeds:
        entries = fetch_feed(feed)
        all_news.extend(entries)
    
    all_news.sort(key=lambda x: x['published'], reverse=True)
    all_news = all_news[:50]
    
    output = {
        'last_updated': datetime.now().isoformat(),
        'news': all_news
    }
    
    with open('news_cache.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Parsed {len(all_news)} news items")

if __name__ == "__main__":
    main()
