import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import time

client = MongoClient("mongodb+srv://mino:Minososo1234@cluster.fkflmzu.mongodb.net/")
db = client["bdd_scrap"] 
collection = db["scraped_articles"]  
base_url = "https://www.blogdumoderateur.com/"
response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")
posts = soup.find_all("article")
print(f"🔍 Nombre d'articles trouvés : {len(posts)}")

for post in posts:
    try:

        link_tag = post.find("a", href=True)
        post_url = link_tag["href"]
        print(f"🔎 Traitement de : {post_url}")

        article_resp = requests.get(post_url)
        article_soup = BeautifulSoup(article_resp.content, "html.parser")

        title_tag = article_soup.find("h1", class_="entry-title")
        title = title_tag.get_text(strip=True) if title_tag else "Titre introuvable"

        hat_tag = article_soup.find("div", class_="article-hat")
        summary = hat_tag.get_text(strip=True) if hat_tag else "Aucun résumé"

        fig_tag = article_soup.find("figure", class_="article-hat-img")
        img_tag = fig_tag.find("img") if fig_tag else None
        thumbnail = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

        post_content = article_soup.find("div", class_="post-content")
        category = post_content["data-cat"].lower() if post_content and post_content.has_attr("data-cat") else "inconnue"

        tag_classes = post.get("class", [])
        tags = [cls.replace("tag-", "") for cls in tag_classes if cls.startswith("tag-")]

        time_tag = article_soup.find("time", class_="entry-date")
        if time_tag and time_tag.has_attr("datetime"):
            date_obj = datetime.strptime(time_tag["datetime"][:10], "%Y-%m-%d")
            post_date = date_obj.date().isoformat()
        else:
            post_date = "Date inconnue"

        author_tag = article_soup.select_one(".byline a")
        author = author_tag.get_text(strip=True) if author_tag else "Auteur inconnu"

        content_div = article_soup.find("div", class_="entry-content")
        images = {}
        if content_div:
            for idx, figure in enumerate(content_div.find_all("figure")):
                img = figure.find("img")
                if not img or not img.get("src"):
                    continue
                img_url = img["src"]
                caption = figure.find("figcaption")
                description = caption.get_text(strip=True) if caption else img.get("alt", "")
                images[f"image_{idx+1}"] = {
                    "url": img_url,
                    "description": description
                }

        scraped_at = datetime.utcnow().isoformat()

        post_data = {
            "url": post_url,
            "title": title,
            "thumbnail": thumbnail,
            "category": category,
            "tags": tags,
            "summary": summary,
            "date": post_date,
            "author": author,
            "images": images,
            "scraped_at": scraped_at
        }

        collection.insert_one(post_data)
        print(f"✅ Article inséré : {title}")
        time.sleep(1)

    except Exception as e:
        print(f"❌ Erreur pour l'article {post_url} : {e}")
