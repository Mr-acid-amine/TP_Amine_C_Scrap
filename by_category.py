from pymongo import MongoClient

client = MongoClient("mongodb+srv://mino:Minososo1234@cluster.fkflmzu.mongodb.net/")
db = client["bdd_scrap"] 
article_collection = db["scraped_articles"]  
critere = input("Enter the category : ").strip().lower()

resultats_filtrés = article_collection.find({
    "$or": [
        {"category": critere},   
        {"tags": critere}        
    ]
})

for art in resultats_filtrés:
    print("📝 Titre :", art["title"])
    print("📅 Publié le :", art["date"])
    print("👨‍💻 Auteur :", art["author"])
    print("🔗 Lien :", art["url"])
    print("💬 Résumé :", art["summary"])
    print("-" * 50)
