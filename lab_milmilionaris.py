
milmilionaris = [  # està en dòlars tot
    {"name": "Suma dels 3428 milmilionaris que hi ha", "wealth": 20_100_000_000_000, "short": "$20.1 T", "src": "wikipedia", "date": "2026/06"},
    {"name": "Suma dels 10 senyors més rics", "wealth": 2_679_000_000_000, "short": "$2679 G", "src": "wikipedia"},
    {"name": "Elon Musk", "wealth": 839_000_000_000, "short": "$839 G", "src": "wikipedia", "date": "2026/06"},
    {"name": "Jeff Bezos", "wealth": 259_000_000_000, "short": "$259 G", "src": "wikipedia", "date": "2026/06"},
    {"name": "Mark Zuckerberg", "wealth": 252_000_000_000, "short": "$252 G", "src": "wikipedia", "date": "2026/06"},
    {"name": "Amancio Ortega", "wealth": 148_000_000_000, "short": "$148 G", "src": "wikipedia", "date": "2026/06"},
    {"name": "Donald Trump", "wealth": 6_000_000_000, "short": "$6 G", "src": "CelebrityNetWorth", "date": "2026/06"},
    {"name": "La Família Kardashian", "wealth": 3_100_000_000, "short": "$3.1 G", "src": "CelebrityNetWorth", "date": "2026/06"},
    {"name": "Mr Beast", "wealth": 2_600_000_000, "short": "$2.6 G", "src": "CelebrityNetWorth", "date": "2026/06"},
    {"name": "Taylor Swift", "wealth": 1_800_000_000, "short": "$1.8 G", "src": "CelebrityNetWorth", "date": "2026/06"},
    {"name": "Mil milions exactes", "wealth": 1_000_000_000, "short": "$1 G", "src": "Les mates de primària"},
]

preus = {
    "Luxe Quotidià": {"desc": "Maneres caríssimes de cobrir les necessitats del dia a dia.", "list":  [
        {"desc": "Rolls-Royce Droptail", "item": "El cotxe més car del món", "src": "USNews", "price": 32_000_000, "max": 4, "date": "2025/02", "url": "https://cars.usnews.com/cars-trucks/advice/most-expensive-cars", "icon": "🚗"},
        {"desc": "University of Southern California", "item": "La carrera universitària més cara del món", "src": "USNews", "price": 75_162, "premult": 4, "date": "2025/02", "url": "https://www.usnews.com/education/best-colleges/the-short-list-college/articles/10-most-least-expensive-private-colleges", "icon": "🎓"},
        {"desc": "Sublimotion (Ibiza)", "item": "Sopar al restaurant més car del món cada dia de la teva vida", "src": "Identitá Golose", "price": 1650, "premult": 36500, "date": "19/07", "url": "https://www.identitagolose.com/sito/en/132/23679/carlo-mangio/weve-been-to-the-most-expensive-restaurant-in-the-world-and-its-worth-it-if-you-can-afford-it.html", "icon": "🍽️"},
        {"desc": "Industry Kitchen Pizza", "item": "La pizza més cara del món un cop al dia tots els dies de la teva vida", "src": "Guinness World Records", "price": 2_700, "premult": 35600, "date": "2017/04", "url": "https://www.guinnessworldrecords.com/world-records/most-expensive-pizza", "icon": "🍕"},
        {"desc": "OMER, Ltd. (Japan)", "item": "El gelat més car del món un cop al dia tots els dies de la teva vida", "price": 6_211, "premult": 36500, "date": "2023/03", "src": "Guinness World Records", "url": "https://www.guinnessworldrecords.com/world-records/731181-most-expensive-of-ice-cream", "icon": "🍨"},
        {"icon": "👜", "item": "La bossa de mà més cara del món", "desc": "Debbie Wingham's Upcylced Egg Bag", "price": 6_700_000, "src": "MyGemma", "url": "https://mygemma.com/blogs/news/10-most-expensive-handbags?srsltid=AfmBOoqhwz_apRT61FSo0Zr5RpM9SyLPtE43F6pp0C4pTg_QOdbZEghK"},
        {"desc": "N'hi ha un bon grapat per triar", "item": "Una casa de luxe \"barata\" a les Maldives", "price": 2_000_000, "src": "JamesEdition", "url": "https://www.jamesedition.com/real_estate/maldives?eur_price_cents_from=45000000&eur_price_cents_to=286044400", "icon": "🏠"},
        {"desc": "The One (Bel Air, California)", "item": "La mansió més cara del món", "price": 500_000_000, "max": 1, "src": "W[Report]", "url": "https://getthewreport.com/architecture/15-of-the-most-expensive-homes-in-the-world-for-sale/", "icon": "🏠"},
        {"desc": "Middle Gap Road (Hong Kong)", "item": "La 2a mansió més cara del món", "price": 447_000_000, "max": 1, "src": "W[Report]", "url": "https://getthewreport.com/architecture/15-of-the-most-expensive-homes-in-the-world-for-sale/", "icon": "🏠"},
        {"desc": "Els majordoms més cars que hi ha als Estats Units", "item": "Un majordom d'elit durant tota la teva vida", "price": 180_000, "premult": 100, "src": "Household Staff", "url": "https://www.householdstaff.agency/how-much-does-a-butler-cost/", "icon": "🤵🏼‍♂️"},
        {"desc": "Sikorsky S-92 Executive", "item": "L'helicòpter privat més car del món", "price": 27_000_000, "src": "Robb Report", "url": "https://robbreport.com/motors/aviation/gallery/most-expensive-helicopters-1236157444/lead-aston-martin-pm_38_515_515791-vd1mxlvpf5-jpg/", "icon": "🚁"},
        {"desc": "Bombardier Global 7500", "item": "El jet privat més car del món", "price": 81_000_000, "src": "Global Air", "url": "https://www.globalair.com/articles/here-are-5-of-the-most-expensive-private-jets-in-the-world/7261", "icon": "🛩️"},
        {"desc": "Amb el Bombardier, suposant que treballes durant 50 anys a 1h (en jet) de casa teva", "item": "Anar en jet privat a la feina cada dia de la teva carrera", "price": 2_000_000 + 14_000 * 2 * 365, "premult": 50, "src": "Global Air", "url": "https://www.globalair.com/articles/here-are-5-of-the-most-expensive-private-jets-in-the-world/7261", "icon": "🛫"},
    ]},
    "Altres Excentricitats": {"desc": "Coses que no serveixen per res però que les compres igualment només perquè pots.", "list": [
        {"desc": "Shot Sage Blue Marilyn", "item": "La serigrafia més cara d'Andy Warhol", "price": 195_000_000, "max": 1, "date": "2022/05", "src": "Guinness World Records", "url": "https://www.guinnessworldrecords.com/world-records/62448-most-expensive-screenprint-by-warhol", "icon": "🖼️"},
        {"desc": "Apex (80% d'un Estegosaure de 8.2 metres)", "item": "L'esquelet de dinosaure més car del món", "price": 44_600_000, "max": 1, "date": "2024/12", "src": "Science.org", "url": "https://www.science.org/content/article/apex-stegosaur-most-expensive-dinosaur-fossil-ever-sold-heads-museum", "icon": "🦖"},
        #{"desc": "Burning Flames Killer Exclusive (Team Fortress 2)", "item": "El barret virtual més car del món", "src": "Guinness World Records", "price": 10_821, "date": "2014/03", "url": "https://www.guinnessworldrecords.com/world-records/117221-most-expensive-virtual-hat"},
    ]},
    "Projectes Puntuals": {"desc": "Esdeveniments o projectes que podries pagar-te o que podries finançar de manera completament altruista.", "list": [
        {"desc": "Rolling Stones, Rihanna, Madonna, Elton John, Taylor Swift, No Doubt, Mumford & Sons, Pink, The Killers, Nickelback (+ despeses del festival)", "item": "Un festival amb un concert de cadascun dels 10 grups que més cobren.", "price": int((8.1 + 8 + 5 + 3.4 + 1 + 0.75 + 0.75 + 0.6 + 0.5 + 0.5) * 1_000_000) + (100 + 100 + 160 + 250 + 50 + 800 + 50 + 30) * 1_000, "date": "2024/05", "src": "94.7 WCSX", "url": "https://wcsx.com/2021/01/15/10-most-expensive-bands-to-hire/", "src2": "175doubledrop (productor musical) @ Reddit", "url2": "https://www.reddit.com/r/aves/comments/7zi893/comment/duqdqu4/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button", "icon": "🎤"},
        {"desc": "Enredados", "item": "La pel·lícula d'animació més cara de crear de la història", "src": "Guinness World Records", "price": 260_000_000, "date": "2013/02", "icon": "🎬"},
        {"desc": "Genshin Impact", "item": "El videojoc més car de desenvolupar de la història", "src": "VGSales Fandom Wiki", "price": 750_000_000, "date": "2020", "inflation_price": 910_000_000, "inflation_date": "2025", "url": "https://vgsales.fandom.com/wiki/List_of_most_expensive_video_games", "icon": "🎮"},
    ]},
    "Escala Global": {"desc": "Coses que podries fer per millorar el món si estiguessis disposat a regalar una part dels teus diners.", "list": [
        {"desc": "Solucionar el problema (a 8 anys vista) i alimentar a tothom que ho necessiti mentre encara ho estiguem resolent", "item": "Acabar amb la fam a tots els països del món", "price": 40_000_000_000, "premult": 8, "max": 1, "src": "World Food Program USA", "url": "https://wfpusa.org/news/how-much-would-it-cost-to-end-world-hunger/", "icon": "🍞"},
        {"icon": "🌳", "desc": "Parc d'uns 4000 m² (construcció + manteniment durant 50 anys)", "item": "Construir un parc al costat de cada hospital del món i mantenir-lo cuidat", "price": 200_000 + 20_000 * 50, "premult": 215_977, "date": "2026", "src": "Keunhyun Park" , "url": "https://keunhyunpark.com/2021/04/21/tedxusu/"}
    ]},
}
