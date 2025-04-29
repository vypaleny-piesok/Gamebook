

# Story node class
class StoryNode:
    def __init__(self, text, options, is_combat=False, enemy=None, coins=0):
        self.text = text
        self.options = options
        self.is_combat = is_combat
        self.enemy = enemy  # Dict like {"name": "Wolf", "health": 30}
        self.coins = coins  # New attribute to store coin rewards
        self.coins_collected = False


# Define story nodes
nodes = {
    "start": StoryNode(
        "Zobudíš sa v lese, tvoja hlava bolí a nič si nepamätáš. Okolo teba je hustý les a vzduch je chladný. Pripadáš si dezorientovaný a stratený. Zrazu si uvedomíš, že máš v rukách krvavý meč, ale vôbec netušíš, odkiaľ pochádza. Kde si? Čo sa stalo?",
        [
            {"text": "Skúsiť si spomenúť, čo sa stalo", "next": "memory_lost"},
            {"text": "Preskúmať les", "next": "explore_forest"}
        ],
        coins=10  # Give 10 coins for this node
    ),
    "memory_lost": StoryNode(
        "Snažíš sa spomenúť na niečo z minulosti, ale tvoje myšlienky sú roztrieštené. Cítiš len zúfalstvo a chaos. Bolesť v hlave sa zintenzívňuje, ale nedokážeš si vybaviť nič. Srdce ti bije rýchlo. Čo ak si niekto alebo niečo vymazalo tvoje spomienky?",
        [
            {"text": "Pokúsiť sa upokojiť a pokračovať v hľadaní útočišťa", "next": "find_shelter"},
            {"text": "Získať sa na chvíľu a sedieť", "next": "rest_under_tree"}
        ],
        coins = 5
    ),
    "explore_forest": StoryNode(
        "Kráčaš ďalej lesom, ale čím viac sa dostávaš do hlbšieho lesa, tým viac sa cítiš znepokojený. Kde sa nachádzaš? Zrazu počuješ niečo šuchotať v kroví.",
        [
            {"text": "Skontrolovať, čo je v kroví", "next": "check_bush"},
            {"text": "Pokračovať v ceste ďalej", "next": "deeper_forest"}
        ],
        coins = 3
    ),
    "find_shelter": StoryNode(
        "Rozhodneš sa hľadať útočište predtým, než sa zotmie. Po chvíli nájdeš malú jaskyňu, kde sa môžeš skryť. Je tam ticho a bezpečne sa cítiš. Možno tu nájdeš nejaké stopy o tom, čo sa stalo.",
        [
            {"text": "Preskúmať jaskyňu", "next": "cave_exploration"},
            {"text": "Odpočinúť si a pokúsiť sa spomenúť", "next": "rest_under_tree"}
        ]
    ),
    "rest_under_tree": StoryNode(
        "Rozhodneš sa sedieť pod stromom a upokojiť sa. Snažíš sa vyprázdniť svoju myseľ, ale v tvojich myšlienkach stále pretrváva chaos. Zrazu zazrieš niečo pohybujúce sa medzi stromami.",
        [
            {"text": "Skontrolovať, čo sa pohybuje medzi stromami", "next": "forest_figure"},
            {"text": "Pokúsiť sa opäť získať kontrolu nad svojimi myšlienkami", "next": "memory_lost"}
        ]
    ),
    "check_bush": StoryNode(
        "Podídete k krovu a zbadáte malú zvieraciu stopu. Je to divoká zver, ale nezjavuje sa. Možno ste sa na chvíľu stratili v lese, alebo to môže byť niečo nebezpečnejšie.",
        [
            {"text": "Pokračovať v hľadaní zvieraťa", "next": "hunt_animal"},
            {"text": "Vrátiť sa k hľadaniu útočišťa", "next": "find_shelter"}
        ]
    ),
    "deeper_forest": StoryNode(
        "Les sa ešte viac zhusťuje. Vzduch je ťažký a vlhký. Na zemi sa objavuje stopy zvieraťa. Možno sa približuješ k niečomu nebezpečnému.",
        [
            {"text": "Pokúsiť sa sledovať stopy", "next": "follow_tracks"},
            {"text": "Zastaviť a preskúmať okolie", "next": "rest_under_tree"}
        ]
    ),
    "cave_exploration": StoryNode(
        "Jaskyňa je temná a vlhká, ale zdá sa, že tu niekto pred tebou niekedy bol. Nájdeš staré, vyblednuté nápisy na stene, ale nie sú zrozumiteľné.",
        [
            {"text": "Pokúsiť sa opísať nápisy", "next": "explore_forest"},
            {"text": "Opustiť jaskyňu a pokračovať hľadaním", "next": "find_shelter"}
        ]
    ),
    "rest_under_tree": StoryNode(
        "Zrazu sa z lesa vytrhne zviera a rýchlo sa rozbehne k tebe.",
        [
            {"text": "Bojovať", "next": "fight_beast"},
            {"text": "Utiecť", "next": "run_away"}
        ]
    ),
    "forest_figure": StoryNode(
        "Stojíš a sleduješ, čo sa pohybuje medzi stromami. Zrazu zbadáš postavu, ktorá sa zdá byť rovnaká ako ty. Ale je to naozaj ty?",
        [
            {"text": "Pokúsiť sa oslovit postavu", "next": "speak_figure"},
            {"text": "Utiecť pred neznámou postavou", "next": "run_away"}
        ]
    ),
    "speak_figure": StoryNode(
        "Keď sa priblížiš, postava zmizne. Cítiš, že niečo nie je v poriadku.",
        [
            {"text": "Pokračovať v hľadaní útočišťa", "next": "find_shelter"},
            {"text": "Opäť skúsiť sa spomenúť, čo sa stalo", "next": "memory_lost"}
        ]
    ),
    "hunt_animal": StoryNode(
        "Chceš sa pripraviť na lov, ale je to riskantné. Zvieratá sú tu nebezpečné. Po chvíli sa nájdeš v konfrontácii s divokým medveďom.",
        [
            {"text": "Bojovať s medveďom", "next": "fight_bear"},
            {"text": "Utiecť", "next": "run_away"}
        ]
    ),
    "follow_tracks": StoryNode(
        "Sleduješ stopy až k rieke. Rieka je divoká a nebezpečná, ale možno sa ti podarí prejsť.",
        [
            {"text": "Pokúsiť sa prejsť rieku", "next": "cross_river"},
            {"text": "Vrátiť sa späť a preskúmať les", "next": "explore_forest"}
        ]
    ),
    "fight_bear": StoryNode(
    "Boj s medveďom je drsný a vyčerpávajúci. Po tvrdých úderoch medveď ustúpi, ale je to ťažká výhra. Máš veľa rán.",
    [
        {"text": "Pokračovať ďalej", "next": "end"}
    ],
    is_combat=True,  # Nastavené na True, aby sa zapol systém boja
    enemy={"name": "Medveď", "health": 50}  # Definovanie nepriateľa, ktorý bude použitý pri boji
),
    "fight_beast": StoryNode(
        "Bojoval si statočne, ale zviera ťa porazilo. Bolesť je neznesiteľná, a ty padáš na zem.",
        [
            {"text": "Zomrel si", "next": "end"}
        ]
    ),
    "cross_river": StoryNode(
        "Prejdenie rieky bolo ťažké, ale nakoniec sa ti podarilo. Na druhej strane nájdeš niečo neznáme, ale niečo, čo ti môže pomôcť v ceste.",
        [
            {"text": "Preskúmať neznámu oblasť", "next": "unknown_area"},
            {"text": "Pokračovať v ceste", "next": "explore_forest"}
        ]
    ),
    "run_away": StoryNode(
        "Ušiel si do bezpečia, ale si zranený a unavený.",
        [
            {"text": "Pokračovať v ceste", "next": "explore_forest"}
        ]
    ),
    "unknown_area": StoryNode(
        "Dostal si sa do neznámej oblasti. Tu to vyzerá inak. Cítiš, že sa niečo zmenilo.",
        [
            {"text": "Preskúmať oblasť", "next": "explore_forest"},
            {"text": "Pokúsiť sa nájsť pomoc", "next": "find_shelter"}
        ]
    ),
    "end": StoryNode(
        "Tvoje dobrodružstvo pokračuje... až do ďalšieho dňa.",
        []
    )
}