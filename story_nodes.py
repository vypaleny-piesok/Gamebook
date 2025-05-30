# story_nodes.py
class StoryNode:
    def __init__(self, text, options, coins=0, is_combat=False, enemy=None, condition=None):
        self.text = text
        self.options = options
        self.coins = coins
        self.coins_collected = False
        self.is_combat = is_combat
        self.enemy = enemy
        self.condition = condition


# Define story nodes
# NEW Story Nodes
# Story Nodes
nodes = {
    "start": StoryNode(
        "Prebudíš sa v temnom lese. Ruky máš od krvi, v nich zvieraš starý meč, a tvoj dych je ťažký. Tvoje spomienky sú prázdne. Nad hlavou je hmla, a ticho ťa dusí.",
        [
            {"text": "Preskúmať meč", "next": "inspect_sword"},
            {"text": "Zvolať o pomoc", "next": "call_for_help"}
        ],
        coins=5
    ),

    "inspect_sword": StoryNode(
        "Na čepeli je vyryté tvoje meno... ale je preškrtané. Spomienka na výkrik a plamene prebehne tvojou hlavou. Si vinný? Alebo obeť?",
        [
            {"text": "Vydaj sa za hlasom, ktorý začuješ v diaľke", "next": "voice_in_fog"},
            {"text": "Odísť do hĺbky lesa", "next": "deep_forest_entry"}
        ],
        coins=5
    ),

    "call_for_help": StoryNode(
        "Tvoj krik sa stratí v hmle. Namiesto odpovede počuješ ozvenu vlastného hlasu, akoby ti niečo odpovedalo rovnakým hlasom.",
        [
            {"text": "Nasledovať ozvenu", "next": "mirror_voice"},
            {"text": "Zbehnúť preč", "next": "run_from_voice"}
        ]
    ),

    "mirror_voice": StoryNode(
        "Postava podobná tebe sa vynorí z hmly. Jej oči sú prázdne a zrkadlia tvoje pohyby. 'Hollow,' povie. 'Čas sa kráti.'",
        [
            {"text": "Osloviť ju", "next": "talk_to_mirror"},
            {"text": "Zaútočiť", "next": "fight_mirror"}
        ]
    ),

    "talk_to_mirror": StoryNode(
        "Povie ti, že si bol kedysi Strážca Brány. Zradil si svoju misiu... alebo ťa zradili. Spomienky ti môžu byť vrátené – ak ich prežiješ.",
        [
            {"text": "Požiadať o spomienky", "next": "regain_memory"},
            {"text": "Odmietnuť minulosť a začať nový život", "next": "new_life"}
        ]
    ),

    "regain_memory": StoryNode(
        "Bol si poslaný strážiť portál medzi svetmi. Porušil si zákon a otvoril ho – ale nie z vlastnej vôle. V tvojej mysli sa odhalí meno: **Astra** – tvoja sestra, teraz väznená v inom svete.",
        [
            {"text": "Prisahať, že ju zachrániš", "next": "vow_to_save"},
            {"text": "Zavrhnúť minulosť", "next": "deny_truth"}
        ],
        coins=10
    ),

    "new_life": StoryNode(
        "Opúšťaš les, snažiac sa zabudnúť. Ale prázdnota v tvojej duši nikdy nezmizne. Si voľný… ale zlomený.",
        [
            {"text": "KONIEC: Sloboda bez pravdy", "next": "end_freedom"}
        ]
    ),

    "vow_to_save": StoryNode(
        "Hmla sa rozostúpi. Vidíš vežu. V nej je portál a niečo ho stráži. Tvoj cieľ je jasný. Vydávaš sa na cestu ako Strážca.",
        [
            {"text": "Pristúpiť k veži", "next": "tower_gate"}
        ]
    ),

    "deny_truth": StoryNode(
        "Snažíš sa utiecť pred tým, čo si bol. Ale tieň minulosti ťa nájde. V lesnej tme sa ozve hlas: 'Zlyhal si dvakrát.'",
        [
            {"text": "KONIEC: Zavrhnutý", "next": "end_doom"}
        ]
    ),

    "deep_forest_entry": StoryNode(
        "Les ťa pohlcuje. Stopy v blate vedú k starému oltáru. Pocítiš volanie – nie fyzické, ale duševné.",
        [
            {"text": "Dotknúť sa oltára", "next": "altar_memory"},
            {"text": "Odísť", "next": "explore_ruins"}
        ],
        coins=3
    ),

    "altar_memory": StoryNode(
        "Vidíš svoju sestru, zviazanú a obklopenú tieňmi. Tvoje rozhodnutia spôsobili túto kliatbu. Ale ešte ju môžeš zachrániť.",
        [
            {"text": "Prisahať vernosť svetlu", "next": "light_path"},
            {"text": "Objímať temnotu v mene pomsty", "next": "dark_path"}
        ]
    ),

    "light_path": StoryNode(
        "Tvoje telo sa naplní silou Svetla. Starý meč sa zmení na svetelný meč, nesúci runy Pravdy.",
        [
            {"text": "Pokračovať k veži", "next": "tower_gate"}
        ],
        coins=10
    ),

    "dark_path": StoryNode(
        "Temnota ťa prijme. Meč sa premení na tiene. Tvoja tvár sa zmení. Už nie si človek… si Sudca.",
        [
            {"text": "KONIEC: Nositeľ tieňov", "next": "end_shadow"}
        ]
    ),

    "tower_gate": StoryNode(
        "Pri veži stojí beštia – strážca portálu. Je to lev so štyrmi očami. Musíš ho poraziť, aby si mohol pokračovať.",
        [
            {"text": "Bojovať", "next": "fight_beast_portal"}
        ],
        is_combat=True,
        enemy={"name": "Strážca Portálu", "health": 60}
    ),

    "fight_beast_portal": StoryNode(
        "Po dlhom boji zviera padá. Portál sa otvára. Astra na teba čaká. Si pripravený.",
        [
            {"text": "Vstúpiť do portálu", "next": "portal_entry"}
        ],
        condition="win"  # Pridaná podmienka pre výhru
    ),

    "fight_beast_portal_lose": StoryNode(
        "Beštia je príliš silná. Tvoj meč sa zlomí a temnota ťa pohltí. Tvoje dobrodružstvo sa končí smrťou.",
        [
            {"text": "KONIEC: Zomrel si", "next": "end_death"}
        ]
    ),

    "portal_entry": StoryNode(
        "Prejdeš portálom. Astra leží v kruhu run, spí. Priložíš ruku na jej srdce. Otvorí oči – 'Brat?'",
        [
            {"text": "KONIEC: Spasiteľ", "next": "end_savior"}
        ]
    ),

    "voice_in_fog": StoryNode(
        "Z hmly sa ozýva šepot. Znie povedome, no zároveň strašidelne. Máš pocit, že ťa niečo volá... alebo varuje?",
        [
            {"text": "Nasledovať hlas", "next": "fog_path"},
            {"text": "Ignorovať hlas a ísť opačným smerom", "next": "explore_forest"}
        ],
        coins=2
    ),

    "tower_entry": StoryNode(
        "Vchádzaš do veže. Steny sú pokryté runami a cítiš silu starého mága. V strede miestnosti víri energia – portál. Ale nie si sám.",
        [
            {"text": "Priblížiť sa k portálu", "next": "tower_gate"},
            {"text": "Prehľadať vežu", "next": "search_tower"}
        ]
    ),

    "search_tower": StoryNode(
        "V jednej z kníh nachádzaš pravdu o portáli – funguje len ak v srdci nie je nenávisť. A nachádzaš tiež elixír (získal si +5 mincí).",
        [
            {"text": "Vrátiť sa k portálu", "next": "tower_gate"}
        ],
        coins=5
    ),

    "fog_path": StoryNode(
        "Nasleduješ hlas cez hmlu, až kým sa pred tebou neobjaví záhadná veža, ktorá nebola na mape. Hmla sa rozplýva.",
        [
            {"text": "Vstúpiť do veže", "next": "tower_entry"},
            {"text": "Ujsť a hľadať inú cestu", "next": "explore_forest"}
        ]
    ),

    # Nové nodes pre chýbajúce odkazy
    "run_from_voice": StoryNode(
        "Utiecť z hmly sa zdá ako dobrý nápad, no les sa stáva hustejším. Narazíš na staré ruiny, ktoré vyzerajú opustene.",
        [
            {"text": "Preskúmať ruiny", "next": "explore_ruins"},
            {"text": "Pokračovať ďalej", "next": "deep_forest_entry"}
        ],
        coins=2
    ),

    "explore_ruins": StoryNode(
        "V ruinách nachádzaš starú mapu lesa. Ukazuje cestu k veži, o ktorej si počul legendy. Cítiš, že si bližšie k pravde.",
        [
            {"text": "Vydaj sa k veži", "next": "tower_entry"},
            {"text": "Vrátiť sa do lesa", "next": "deep_forest_entry"}
        ],
        coins=3
    ),

    "explore_forest": StoryNode(
        "Ignoruješ hlas a kráčaš opačným smerom. Les je tichý, no nachádzaš stopy, ktoré vedú k starému oltáru.",
        [
            {"text": "Dotknúť sa oltára", "next": "altar_memory"},
            {"text": "Pokračovať v hľadaní", "next": "deep_forest_entry"}
        ],
        coins=1
    ),

    "fight_mirror": StoryNode(
        "Zaútočíš na postavu, no tvoj meč prechádza cez ňu ako cez hmlu. Postava sa rozplynie a ty cítiš slabosť. Strácaš čas.",
        [
            {"text": "Pokračovať k veži", "next": "tower_entry"},
            {"text": "Vrátiť sa do lesa", "next": "deep_forest_entry"}
        ]
    ),

    # Koncové nodes
    "end_freedom": StoryNode(
        "Si voľný… ale nikdy celistvý. V tvojej duši ostáva diera, ktorú pravda mohla zaplniť.",
        []
    ),

    "end_doom": StoryNode(
        "Zavrhol si seba samého. A temnota to využila. Zmizneš bez mena, bez stopy.",
        []
    ),

    "end_shadow": StoryNode(
        "Stávaš sa legendou tieňov. Tvoje meno sa šeptá medzi dimenziami. Si konečný rozsudok.",
        []
    ),

    "end_savior": StoryNode(
        "Spomienky sú späť. Tvoja sestra žije. Tvoja cesta sa naplnila. Si opäť Strážca.",
        []
    ),

    "end_death": StoryNode(
        "Tvoje dobrodružstvo sa skončilo. Zomrel si v boji. Možno nabudúce prežiješ dlhšie.",
        []
    )
}
