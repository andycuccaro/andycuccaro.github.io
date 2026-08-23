"""
Utilidades compartidas para generar feeds RSS.
Usado por generate_feed.py (feed general) y generate_tags.py (feeds por etiqueta).
"""
from email.utils import format_datetime, formatdate
from xml.sax.saxutils import escape

SITE_URL = "https://andycuccaro.info"
SITE_TITLE = "Andy Cuccaro"


def build_rss(items, feed_title, feed_description, feed_self_url):
    """
    items: lista de dicts con 'title', 'type', 'url', 'date' (datetime)
    Devuelve el XML del feed como string.
    """
    rss_items = ""
    for item in items:
        pub_date = format_datetime(item["date"])
        rss_items += f"""  <item>
    <title>{escape(item['title'])}</title>
    <link>{item['url']}</link>
    <guid>{item['url']}</guid>
    <pubDate>{pub_date}</pubDate>
    <description>{escape(item.get('type', ''))}</description>
  </item>
"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{escape(feed_title)}</title>
  <link>{SITE_URL}/</link>
  <description>{escape(feed_description)}</description>
  <language>en</language>
  <atom:link href="{feed_self_url}" rel="self" type="application/rss+xml" />
  <lastBuildDate>{formatdate(usegmt=True)}</lastBuildDate>
{rss_items}</channel>
</rss>
"""
