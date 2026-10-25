"""Construit mahe.json à partir des listes de séries ci-dessous."""
import json, re, unicodedata, datetime

TODAY = datetime.date.today().isoformat()

def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]

SERIES = {
    "P'tit Loup": dict(
        qprefix="", qkey="Lallemand",
        authors="Orianne Lallemand, Éléonore Thuillier", publisher="Auzou",
        about="Les petites histoires du quotidien de P'tit Loup, pour les tout-petits : le pot, le dodo, les émotions, la famille, les premières fois. Albums cartonnés, collection Auzou éveil.",
        owned=["P'tit Loup aime sa mamie", "P'tit Loup ne dort pas à la maison", "P'tit Loup va sur le pot",
               "P'tit Loup et la chasse aux œufs de Pâques", "P'tit Loup et les émotions",
               "P'tit Loup aime les bébés animaux", "P'tit Loup au parc animalier", "P'tit Loup se balade en forêt"],
        wanted=["P'tit Loup rentre à l'école", "P'tit Loup aime son doudou", "P'tit Loup a peur du noir",
                "P'tit Loup prépare Noël", "P'tit Loup n'aime que les pâtes", "P'tit Loup dit toujours non",
                "P'tit Loup a un bobo", "P'tit Loup part en vacances", "P'tit Loup ne veut pas partager",
                "P'tit Loup aime sa gardienne", "P'tit Loup s'habille tout seul", "Au dodo, P'tit Loup !",
                "P'tit Loup fait une colère", "P'tit Loup part en voyage", "P'tit Loup apprend à jardiner",
                "P'tit Loup est le roi de la galette", "P'tit Loup fête son anniversaire", "P'tit Loup va chez le docteur",
                "P'tit Loup fait du ski", "P'tit Loup se lave tout seul", "P'tit Loup veut être le chef",
                "P'tit Loup ne veut pas dormir", "P'tit Loup aime sa maman", "P'tit Loup n'a plus besoin de tétine",
                "P'tit Loup va chez papi et mamie", "P'tit Loup aime son papa", "P'tit Loup aime sa maîtresse",
                "P'tit Loup ne veut pas ranger", "P'tit Loup aime le Père Noël", "P'tit Loup fait des bêtises",
                "P'tit Loup est poli", "P'tit Loup se déguise", "P'tit Loup veut devenir pompier",
                "P'tit Loup ne veut pas aller à l'école", "P'tit Loup visite Paris", "P'tit Loup fête Halloween",
                "P'tit Loup aime les livres", "P'tit Loup fait des crêpes",
                ("P'tit Loup adore les dinosaures", "9791039577403", "2026")],
    ),
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
                "Azuro sur la piste de Jippy", "Azuro et l'île fantastique", "Azuro, il faut sauver la Lune !"],
    ),
    "Bluey": dict(
        qprefix="Bluey", qkey="Hachette",
        authors="d'après la série de Joe Brumm", publisher="Hachette Jeunesse",
        about="Les albums tirés du dessin animé Bluey : la petite chienne Bluey, sa sœur Bingo et leurs parents inventent des jeux à partir du quotidien.",
        owned=[("Papa-Robot", "9782017291886"), ("Mini Bluey", "9782017291947"), ("Camping", "9782017246657"),
               ("La nuit de Noël", "9782017292159"), ("La mauvaise humeur", "9782017292104")],
        wanted=[("La plage", "9782017194095", "2023"), ("La course des bébés", "9782017291800"),
                ("Le grand bain de Noël", "9782017291855"), ("Papa met Bingo et Bluey au lit", "9782017291879", "2024"),
                ("C'est l'heure de dormir", "9782017291923", "2025"), ("Monsieur Licorne", "9782017291954", "2025"),
                ("J'aime ma famille", "9782017292012", "2025"), ("Le conte de fées", "9782017292036", "2025"),
                ("Le trajet en voiture", "9782017292050", "2025"), ("Le barbecue", "9782017292029", "2025"),
                ("Calypso - La maîtresse", "9782017292081", "2025"), ("L'école des mamans", "9782017292098", "2025"),
                ("Les reines", "9782017292173", "2025"), ("Imitation", "9782017292227", "2026"),
                ("La chambre", "9782017292234", "2026"), ("La cabane à outils", "9782017292272", "2026"),
                ("Passe le paquet", "9782017292296", "2026"), ("Le xylophone magique", "9782017376514", "2026"),
                ("Le week-end", "9782017376521", "2026"), ("Le zoo", "9782017376552", "2026"),
                ("Le scooter à mamies", "9782017376576", "2026"), ("Les trains", "9782017376569", "2026"),
                ("La soirée pyjama", "9782017376675", "2026", "Parution le 28 octobre 2026."),
                ("Le médecin", "9782017376682", "2026", "Parution le 4 novembre 2026.")],
    ),
    "Les Drôles de Petites Bêtes": dict(
        qprefix="", qkey="Krings",
        authors="Antoon Krings", publisher="Gallimard Jeunesse Giboulées",
        about="Les petites bêtes du jardin d'Antoon Krings, chacune avec son caractère et sa petite aventure. Albums numérotés, un classique de la littérature jeunesse.",
        numbered=True,
        owned=[(2, "Belle la coccinelle"), (22, "Hugo l'asticot"), (23, "Adrien le lapin"), (26, "Lulu la tortue"),
               (32, "Amélie la souris"), (34, "Samson le hérisson"), (35, "Valérie la chauve-souris"),
               (37, "Pierrot le moineau"), (39, "Léon, le roi des abeilles"), (42, "Blaise et Thérèse les punaises")],
        wanted=[(1, "Mireille l'abeille"), (3, "Siméon le papillon"), (4, "Chloé l'araignée"), (5, "Camille la chenille"),
                (6, "Marie la fourmi"), (7, "Léon le bourdon"), (8, "Margot l'escargot"), (9, "Barnabé le scarabée"),
                (10, "Patouch la mouche"), (11, "Carole la luciole"), (12, "Ursule la libellule"), (13, "Loulou le pou"),
                (14, "Frédéric le moustique"), (15, "Benjamin le lutin"), (16, "Adèle la sauterelle"), (17, "Oscar le cafard"),
                (18, "Luce la puce"), (19, "Pat le mille-pattes"), (20, "Pascale la cigale"), (21, "Huguette la guêpe"),
                (24, "Grâce la limace"), (25, "César le lézard"), (27, "Solange la mésange"), (28, "Georges le rouge-gorge"),
                (29, "Lorette la pâquerette"), (30, "Maud la taupe"), (31, "Antonin le poussin"), (33, "Juliette la rainette"),
                (36, "Benjamin, le Père Noël du jardin"), (38, "Zabeth la chouette"), (40, "Odilon le grillon"),
                (41, "Luna la petite ourse"), (43, "Léonard le têtard"), (44, "Édouard le loir"),
                (45, "Marion et Simon les chatons"), (46, "Victor le castor"), (47, "Merlin le merle"),
                (48, "Romain le lapin magicien"), (49, "Prosper le hamster"), (50, "Louis le papillon de nuit"),
                (51, "Noémie, princesse fourmi"), (52, "Théo le mulot"), (53, "Gaston le caneton"), (54, "Roméo le crapaud"),
                (55, "Gabriel, le lutin de Noël"), (56, "Henri le canari"), (57, "Bob le bonhomme de neige"),
                (58, "Robin, l'écureuil du jardin"), (59, "Cyprien le chien"), (60, "Léo le lérot"),
                (61, "Nora, petit rat de l'opéra"), (62, "Apollon le grillon")],
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
        owned=[("La pelleteuse et le papillon", "9782383222927"), "La pelleteuse et le caneton", "Nuit blanche pour la pelleteuse"],
        wanted=[("La pelleteuse et la fleur", "9782383220831"), "La pelleteuse et le sapin de Noël"],
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

# Collection presse Disney : représentée par des numéros
name = "Mes petits livres d'or Disney"
series_meta[name] = {"checkedAt": TODAY,
    "about": "Collection Hachette Collections vendue en kiosque et par abonnement : un grand classique Disney ou Pixar par numéro, en petit format relié doré.",
    "note": "Mahé a les numéros 1 à 83. Les numéros suivants se commandent à l'unité sur le site d'Hachette Collections."}
books.append({"id": "livres-or-disney-1-83", "title": "Numéros 1 à 83", "authors": "Disney", "publisher": "Hachette Collections",
              "series": name, "seriesNumber": 1, "owned": True, "isbn": "", "year": "", "addedAt": TODAY, "gid": "", "cover": "", "noCover": True,
              "synopsis": "Les 83 premiers numéros de la collection, déjà à la maison."})
books.append({"id": "livres-or-disney-84-plus", "title": "Numéros 84 et suivants", "authors": "Disney", "publisher": "Hachette Collections",
              "series": name, "seriesNumber": 84, "isbn": "", "year": "", "addedAt": TODAY, "gid": "", "cover": "", "noCover": True,
              "link": "https://www.hachette-collections.com/",
              "synopsis": "N'importe quel numéro à partir du 84 fera plaisir. Les numéros se commandent à l'unité sur le site d'Hachette Collections (rubrique « Commander un numéro »)."})

json.dump({"series": series_meta, "books": books}, open("mahe.json", "w"), ensure_ascii=False, indent=1)
print(len(books), "livres,", sum(1 for b in books if not b.get("owned")), "souhaités")
