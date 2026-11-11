"""Construit mahe.json à partir des listes de séries ci-dessous."""
import json, re, unicodedata, datetime

TODAY = datetime.date.today().isoformat()

def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]

SERIES = {
    "Les émotions de Gaston": dict(
        qprefix="Gaston", qkey="Chien Chow Chine",
        authors="Aurélie Chien Chow Chine", publisher="Hachette Enfants",
        about="Gaston, la licorne à la crinière arc-en-ciel, apprend à reconnaître et à apaiser ses émotions. Chaque petit album cartonné aborde une émotion et propose un exercice simple pour retrouver le calme.",
        owned=["Je suis triste", "Je n'arrive pas à dormir", "Je suis joyeux", "Je m'ennuie", "Je suis gentil",
               "Je m'en veux", "Je suis en colère", "Je suis vexé", "Je suis différent comme tout le monde", "Je suis fier"],
        wanted=[("Je suis tout fou-fou", "9782017089629"), "Je boude", ("Je suis amoureux", "9782017064114"),
                "J'ai peur", "Je suis jaloux", ("Je me concentre", "9782017092780"), ("Je suis timide", "9782017023470"),
                ("Je suis impatient", "9782017092773"), "J'ai confiance en moi", ("J'écoute", "9782017107033")],
    ),
    "Azuro": dict(
        qprefix="", qkey="Souillé",
        authors="Olivier Souillé, Laurent Souillé, Jérémie Fleury", publisher="Auzou",
        about="Les aventures d'Azuro, un petit dragon bleu au grand cœur, et de ses amis, dans un monde de chevaliers, de fées et de créatures magiques.",
        owned=["Azuro et les dinosaures"],
        wanted=["Azuro le dragon bleu", "Azuro et l'œuf mystérieux", "Azuro à l'école des monstres",
                "Azuro et la fée des glaces", "Azuro au royaume des dragons", "Azuro et le défi du Père Noël",
                "Azuro et la dernière licorne", "Azuro et la sorcière", "Azuro et le château oublié",
                "Azuro sur la piste de Jippy", "Azuro et l'île fantastique", "Azuro, il faut sauver la Lune !",
                "Azuro et le cristal chantant", "Azuro, un cadeau magique pour maman"],
    ),
    "Bluey": dict(
        qprefix="Bluey", qkey="Hachette",
        authors="d'après la série de Joe Brumm", publisher="Hachette Jeunesse",
        about="Les albums tirés du dessin animé Bluey : la petite chienne Bluey, sa sœur Bingo et leurs parents inventent des jeux à partir du quotidien.",
        owned=[("Papa-Robot", "9782017291886"), ("Mini Bluey", "9782017291947"), ("Camping", "9782017246657"),
               ("La nuit de Noël", "9782017292159")],
        wanted=[("La plage", "9782017194095", "2023"), ("La course des bébés", "9782017291800"),
                ("Le grand bain de Noël", "9782017291855"), ("Papa met Bingo et Bluey au lit", "9782017291879", "2024"),
                ("C'est l'heure de dormir", "9782017291923", "2025"), ("Monsieur Licorne", "9782017291954", "2025"),
                ("J'aime ma famille", "9782017292012", "2025"), ("Le conte de fées", "9782017292036", "2025"),
                ("La mauvaise humeur", "9782017292104", "2025"), ("Le trajet en voiture", "9782017292050", "2025"), ("Le barbecue", "9782017292029", "2025"),
                ("Calypso - La maîtresse", "9782017292081", "2025"), ("L'école des mamans", "9782017292098", "2025"),
                ("Les reines", "9782017292173", "2025"), ("Imitation", "9782017292227", "2026"),
                ("La chambre", "9782017292234", "2026"), ("La cabane à outils", "9782017292272", "2026"),
                ("Passe le paquet", "9782017292296", "2026"), ("Le xylophone magique", "9782017376514", "2026"),
                ("Le week-end", "9782017376521", "2026"), ("Le zoo", "9782017376552", "2026"),
                ("Le scooter à mamies", "9782017376576", "2026"), ("Les trains", "9782017376569", "2026"),
                ("La soirée pyjama", "9782017376675", "2026", "Parution le 28 octobre 2026."),
                ("Le médecin", "9782017376682", "2026", "Parution le 4 novembre 2026.")],
    ),
    "Les Histoires de Flash McQueen": dict(
        qprefix="Cars Flash McQueen", qkey="Disney",
        authors="Disney Pixar", publisher="Hachette Jeunesse (Disney)",
        about="De courtes histoires inédites avec Flash McQueen et ses amis de Radiator Springs, tirées de l'univers Cars. Petits albums numérotés.",
        numbered=True,
        owned=[(7, "Esprit de compétition"), (8, "Coureurs sur glace", "9782017868026")],
        wanted=[(1, "La parade des pompiers", "9782017867890"), (2, "Une course solidaire", "9782017867906"),
                (3, "Le jukebox de Martin", "9782017867913"), (4, "La passion de la course", "9782017867920"),
                (5, "Le monstre de la forêt", "9782017867975"), (6, "Duel contre Storm", "9782017867982")],
    ),
    "La Pelleteuse": dict(
        qprefix="", qkey="Kuefler",
        authors="Joseph Kuefler", publisher="Kimane",
        about="Une petite pelleteuse au grand cœur, sur son chantier, découvre l'amitié et la douceur au fil des saisons. Albums illustrés de Joseph Kuefler.",
        owned=[("La pelleteuse et le papillon", "9782383222927"), "La pelleteuse et le caneton", "Nuit blanche pour la pelleteuse", ("La pelleteuse et la fleur", "9782383220831")],
        wanted=["La pelleteuse et le sapin de Noël"],
    ),
}

books = []
series_meta = {}
for name, s in SERIES.items():
    series_meta[name] = {"checkedAt": TODAY, "about": s["about"]}
    for owned, items in ((True, s["owned"]), (False, s["wanted"])):
        for it in items:
            num = isbn = year = note = None
            if s.get("numbered"):
                num, title, *rest = it
                isbn = rest[0] if rest else None
            elif isinstance(it, tuple):
                title, *rest = it
                isbn = rest[0] if len(rest) > 0 else None
                year = rest[1] if len(rest) > 1 else None
                note = rest[2] if len(rest) > 2 else None
            else:
                title = it
            b = {"id": slug(name + "-" + title), "title": title, "authors": s["authors"], "publisher": s["publisher"],
                 "series": name, "seriesNumber": num, "isbn": isbn or "", "year": year or "", "synopsis": note or "",
                 "addedAt": TODAY, "gid": "", "cover": ""}
            if owned:
                b["owned"] = True
            # requête de couverture : titre + série pour les titres courts
            b["coverQuery"] = f"{s['qprefix']} {title} {s['qkey']}".strip()
            books.append(b)

# Livres hors série ajoutés à la main (dates fixes)
STANDALONE = [
 {
  "id": "chevalier-chouette",
  "title": "Chevalier Chouette",
  "authors": "Christopher Denise",
  "publisher": "L'École des loisirs (Kaléidoscope)",
  "series": "Chevalier Chouette",
  "seriesNumber": 1,
  "isbn": "9782211335713",
  "year": "2024",
  "addedAt": "2026-11-02",
  "gid": "",
  "cover": "",
  "coverQuery": "Chevalier Chouette Christopher Denise",
  "synopsis": "Une petite chouette rêve de devenir chevalier. Admise à l'école de chevalerie, elle monte la garde la nuit et doit affronter un dragon affamé, avec plus d'astuce et de gentillesse que de force.\n\nUn album sur la persévérance et la bravoure des plus petits."
 },
 {
  "id": "mon-amour-desbordes",
  "title": "Mon amour",
  "authors": "Astrid Desbordes, Pauline Martin",
  "publisher": "Albin Michel Jeunesse",
  "series": None,
  "seriesNumber": None,
  "isbn": "9782226315243",
  "year": "2015",
  "addedAt": "2026-11-02",
  "gid": "",
  "cover": "",
  "coverQuery": "Mon amour Astrid Desbordes Pauline Martin",
  "synopsis": "Archibald demande à sa maman si elle l'aimera toute la vie. Elle lui répond par une série de situations opposées, sage ou en colère, près ou loin, pour lui montrer que son amour ne change jamais.\n\nUn album très tendre sur l'amour inconditionnel."
 },
 {
  "id": "chevalier-chouette-petite-oiselle",
  "title": "Chevalier Chouette et Petite Oiselle",
  "authors": "Christopher Denise",
  "publisher": "L'École des loisirs (Kaléidoscope)",
  "series": "Chevalier Chouette",
  "seriesNumber": 2,
  "isbn": "9782378882839",
  "year": "2025",
  "addedAt": "2026-11-03",
  "gid": "",
  "cover": "",
  "coverQuery": "Chevalier Chouette et Petite Oiselle Christopher Denise",
  "synopsis": "Chevalier Chouette, capitaine de la garde de nuit, suit une routine bien réglée : il veille sur le château toute la nuit et se repose le matin. Jusqu'au jour où une petite oiselle vient bousculer ses habitudes… et lui prouver qu'on a toujours besoin d'un plus petit que soi."
 },
 {
  "id": "chevalier-chouette-prepare-noel",
  "title": "Chevalier Chouette prépare Noël",
  "authors": "Christopher Denise",
  "publisher": "Kaléidoscope",
  "series": "Chevalier Chouette",
  "seriesNumber": 3,
  "isbn": "9782378883126",
  "year": "2025",
  "addedAt": "2026-11-03",
  "gid": "",
  "cover": "",
  "coverQuery": "Chevalier Chouette prépare Noël Christopher Denise",
  "synopsis": "Chevalier Chouette et Petite Oiselle attendent Noël avec impatience. Le jeune lecteur les aide à tout préparer pour la fête."
 }
]
books += STANDALONE
series_meta["Chevalier Chouette"] = {"checkedAt": "2026-11-03", "about": "Les aventures d'une petite chouette devenue chevalier, qui veille sur le château la nuit et règle les problèmes avec astuce et gentillesse plutôt qu'avec la force. Albums de Christopher Denise, aux illustrations dorées et nocturnes."}

ISBN = json.load(open("tools/isbn.json"))
for b in books:
    if not b.get("isbn") and b["title"] in ISBN:
        b["isbn"] = ISBN[b["title"]]
json.dump({"series": series_meta, "books": books}, open("mahe.json", "w"), ensure_ascii=False, indent=1)
print(len(books), "livres,", sum(1 for b in books if not b.get("owned")), "souhaités")
