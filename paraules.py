from flask_babel import lazy_gettext as _l


def build_links(paraules):
    for i, p in paraules.items():
        desc = p["desc"]
        if "[[" in desc:
            desc_list = desc.split("[[")
            rebuilt = []
            for segment in desc_list:
                if "]]" in segment:
                    link, rest = segment.split("]]")
                    link_text, link_num = link.split("|")
                    rebuilt.append("<span class='desc-link pointer' onclick='load_word(" + link_num + ")'>" + link_text + "</span>")
                    rebuilt.append(rest)
                else:
                    rebuilt.append(segment)
            paraules[i]["desc"] = "".join(rebuilt)
    return paraules


def build_words():
    words_by_topic = {}
    for i, word in build_links(paraules).items():
        temas = word.get("temas", [])
        if temas:
            for tema in temas:
                if tema not in words_by_topic:
                    words_by_topic[tema] = {"name": temas_list.get(tema, {}).get("name", "(" + tema + ")"), "contents": {}}
                words_by_topic[tema]["contents"][i] = word
        else:
            if "none" not in words_by_topic:
                words_by_topic["none"] = {"name": "Sin Tema", "contents": {}}
            words_by_topic["none"]["contents"][i] = word
    return words_by_topic


temas_list = {
    "POL": {"name": _l("Política")},
    "ECON": {"name": _l("Economía")},
    "ECOL": {"name": _l("Ecología")},
    "TEC": {"name": _l("Tecnología")},
    "ESTAD": {"name": _l("Estadística")},
    "ANT": {"name": _l("Antropología")},
    "FIS": {"name": _l("Física")},
    "SAL": {"name": _l("Salud")},
    "PSI": {"name": _l("Psicología")},
    "ART": {"name": _l("Arte")},
    "BIO": {"name": _l("Biología")},
    "URB": {"name": _l("Urbanismo")},
}


paraules = {
    1: {"temas": ["POL"], "name": _l("Ventana de Overton"), "desc": _l("<p>Conjunto de ideas políticas que se consideran 'aceptables' en la sociedad en general y, por tanto, que pueden acabar convirtiéndose en leyes.</p>Las ideas más aceptadas están en el centro de la ventana, las que son algo más atrevidas están en los bordes, y las más radicales están fuera de la ventana. La ventana se mueve con el tiempo a medida que la opinión pública cambia, ya sea de forma natural o porque personas o partidos influyentes (y dispuestos a aceptar las reprimiendas) eligen repetir las ideas radicales hasta que el público se acostumbra a ellas."), "url": {"wiki": _l("https://es.wikipedia.org/wiki/Ventana_de_Overton")}},
    2: {"temas": ["POL"], "name": _l("Radical vs Extremista"), "desc": _l("<p>Usamos las dos palabras como si fueran equivalentes, pero la etimología nos da dos matices distintos.</p><p><b>Radical</b> es alguien dispuesto a cambiar las cosas de raíz. <b>Extremista</b> es alguien dispuesto a llevar las cosas al extremo.</p><i>Por ejemplo, querer que la vivienda sea gratis para todo el mundo no es 'Extrema Izquierda', es 'Izquierda Radical'. 'Extrema Izquierda' sería por ejemplo torturar a los milmillonarios hasta que acepten dejar de serlo.</i>")},
    3: {"temas": ["POL"], "name": _l("Índice de la Dignidad"), "desc": _l("El <b>Índice de la Dignidad</b> (en inglés <i>Dignity Index</i>) es una escala que mide el grado de humanidad con el que los discursos hablan de otras personas. Va del 1 al 8, y es muy útil para detectar pronto la polarización y la deriva que lleva al <b>Alto conflicto</b>."), "urls": {"web": "https://www.dignity.us/"}},
    4: {"temas": ["POL"], "name": _l("Emprendedores del Conflicto"), "desc": _l("Aquellas personas que se benefician del [[Alto Conflicto|9]] y que eligen deliberadamente provocarlo y alimentarlo."), "cred": _l("Acuñado por Amanda Ripley en su (recomendadísimo) libro <i>High Conflict: Why We Get Trapped and How We Get Out</i>")},
    5: {"temas": ["POL"], "name": _l("La regla del 3.5%"), "desc": _l("<p>Siempre que un <b>3.5% de la población</b> ha protestado de manera <b>noviolenta</b> contra un gobierno autoritario, el gobierno autoritario ha caído.</p>Es decir, para provocar un cambio en el mundo siempre hace falta mucha menos gente de la que parece.")},
    6: {"temas": ["POL"], "name": _l("El propósito de un sistema es aquello que hace"), "desc": _l("<p>(En inglés <b>POSIWID</b>, <i>The purpose of a system is what it does</i>)<br>Es la idea de que no tiene sentido juzgar un sistema en función de las supuestas intenciones de sus creadores o promotores si a la hora de la verdad constantemente consigue o provoca otros resultados.</p>Si algo siempre 'funciona mal' y nadie lo corrige, es sensato asumir que la intención real es que funcione mal.")},
    7: {"temas": ["POL"], "name": _l("Los ricos te quieren racista"), "desc": ""},
    8: {"temas": ["POL"], "name": _l("Guerra jurídica"), "desc": _l("<p>En inglés <i>Lawfare</i>. Es cuando se usa el poder y favor de los jueces de forma abusiva o ilegal para intentar eliminar oponentes, ya sea inhabilitándoles o simplemente dañando su reputación al hacer que parezca que sus problemas con la justicia son legítimos.</p>En general acaba siendo <b>judicial y mediática</b> e implicando cuatro actores: las <b>organizaciones</b> que ponen denuncias falsas, los <b>jueces corruptos</b> que las aceptan sin pruebas, los <b>medios de comunicación</b> que aprovechan para provocar revuelo, y las <b>cuentas en redes sociales</b> que amplifican esas noticias falsas o esos casos judiciales ilegítimos.")},
    9: {"temas": ["POL"], "name": _l("Alto Conflicto"), "desc": "Conflicto en el que ya no hay espacio para la curiosidad porque la polarización y el [[tribalismo|11]] lo han invadido todo.<br>Estadio de los conflictos, opuesto al <b>Conflicto Sano</b>, en el que las cosas sólo empeoran para las dos partes, porque ambas están más preocupadas por <i>ganar</i> y <i>humillar</i> que por resolver el problema subyacente.", "cred": _l("Acuñado por Amanda Ripley en su (recomendadísimo) libro <i>High Conflict: Why We Get Trapped and How We Get Out</i>")},
    10: {"temas": ["POL"], "name": _l("Appartheid"), "desc": _l("Sistema político en el que las propias instituciones y leyes separan y discriminan a las personas en función de su raza.")},
    11: {"temas": ["POL"], "name": _l("Tribalismo"), "desc": _l("<p>Dinámica en la que las personas se identifican con un grupo y sienten una fuerte lealtad hacia ese grupo, favoreciéndolo frente a los demás y a menudo excluyendo o discriminando a los miembros de los demás grupos.</p><i>Lo que pasa, por ejemplo, con los seguidores de equipos de fútbol, o con los votantes que defienden a 'su' partido haga lo que haga.</i>")},
    12: {"temas": ["POL"], "name": "Intervencionismo de EUA", "desc": ""},
    13: {"temas": ["POL"], "name": "Sanciones de EUA", "desc": ""},  # i.e. Albanese &

    16: {"temas": ["POL"], "name": "Qui escull què és 'Terrorisme'", "desc": ""},  # i.e. surveilance & bibi changes
    17: {"temas": ["POL"], "name": "La Lista Epstein", "desc": ""},
    18: {"temas": ["POL"], "name": "El que sigui que passa amb el CGPJ", "desc": ""},
    19: {"temas": ["POL"], "name": _l("Gerrymandering"), "desc": _l("<p>Cambiar las fronteras de las circunscripciones electorales de manera maliciosa para intentar favorecer o perjudicar a un partido o grupo de personas.</p><i>Por ejemplo, dividir a los votantes de un partido en muchos sectores distintos para que no ganen representación en ninguno de ellos, o amontonarlos de manera excesiva en un sólo distrito para que no les sobre suficiente gente como para ganar en ninguno de los demás.</i>")},  # "<p>Canviar les fronteres de les circumscripcions electorals de manera maliciosa per intentar afavorir o perjudicar a un partit o grup de persones.</p><i>Per exemple, dividir els votants d'un partit en molts sectors diferents per tal que no guanyin representació a cap d'ells, o apilonar-los de manera excessiva en un sol sector per tal que no els sobri prou gent per guanyar a cap dels altres.</i>"
    20: {"temas": ["POL"], "name": "La gent no sap quan no es mor", "desc": ""},  # ft. hank
    21: {"temas": ["POL"], "name": _l("Terrorismo estocástico"), "desc": _l("<p>La manera como repetir discursos hostiles públicamente acaba desencadenando en violencia impartida por personas anónimas (incluso si no se les pide explícitamente que sean violentas), simplemente por probabilidad.</p>El modo en el que los actores que quieren dañar a ciertos grupos de personas no necesitan pedir violencia explícitamente ni cometerla ellos mismos, porque saben que si señalan y siembran suficiente odio, alguien entre el público acabará decidiendo cometerla por su cuenta.")},
    22: {"temas": ["POL"], "name": _l("Abya Yala"), "desc": _l("Nombre con el que se refieren al continente americano las culturas indígenas que habitan en él y muchos movimientos sociales. Se plantea como alternativa a términos como <b>América</b> o <b>Nuevo mundo</b>, que fueron impuestos por los colonizadores europeos.")},
    23: {"temas": ["POL"], "name": "Zionisme", "desc": ""},
    24: {"temas": ["POL", "ECON"], "name": _l("Pinkwashing"), "desc": _l("Tácticas publicitarias en las que las empresas y gobiernos posan como aliadas del colectivo LGBT+ para intentar parecer progresistas.")},
    25: {"temas": ["POL"], "name": _l("Interseccionalidad"), "desc": _l("<p>La idea de que no podemos analizar las injusticias sociales de modo aislado, sino que hay que tener en cuenta cómo se afectan entre ellas, porque cada persona o conjunto de personas tendrá su combinación única de discriminaciones y privilegios en función de los grupos sociales a los que pertenezca.</p><i>Por ejemplo, es <b>Feminismo Interseccional</b> aquél que se preocupa por incluír y dar la misma voz a todas las mujeres (i.e. no sólo a las blancas, cristianas, cis...), y por entender y solidarizarse con las causas por las que éstas puedan estar luchando en paralelo a la feminista.</i>")},
    26: {"temas": ["POL"], "name": "Les guerres tenen normativa", "desc": ""},
    27: {"temas": ["POL"], "name": "Externalització de fronteres", "desc": ""},
    28: {"temas": ["POL"], "name": "Okupació vs Violació de Domicili", "desc": ""},
    29: {"temas": ["POL"], "name": "Sud Global", "desc": ""},
    30: {"temas": ["POL"], "name": "Reaccionario", "desc": ""},
    31: {"temas": ["POL"], "name": "Polarización", "desc": ""},
    32: {"temas": ["POL"], "name": "Europa no es un continente", "desc": ""},
    33: {"temas": ["ECON"], "name": "Tener dinero da dinero", "desc": ""},
    34: {"temas": ["ECON", "TEC"], "name": _l("Obsolescencia Programada"), "desc": _l("")},
    35: {"temas": ["ECON"], "name": "Doughnut Economics", "desc": ""},
    36: {"temas": ["ECON"], "name": "El PIB no funciona", "desc": ""},
    37: {"temas": ["ECON"], "name": "Right to Repair", "desc": ""},
    38: {"temas": ["ECON"], "name": "Neocolonialismo", "desc": ""},
    39: {"temas": ["ECON"], "name": "Monopsony", "desc": ""},
    40: {"temas": ["ECON"], "name": "Enshittification", "desc": ""},
    41: {"temas": ["ECON"], "name": _l("Reduflación"), "desc": _l("En inglés <i>Shrinkflation</i>, es el modo en el que las empresas suben el precio de las cosas a base de mantener el precio del producto pero reducir su tamaño o cantidad de producto.")},
    42: {"temas": ["ECON"], "name": "Dynamic Pricing", "desc": ""},
    43: {"temas": ["ECON"], "name": "Paradoja de Jevon", "desc": ""},
    44: {"temas": ["ECON"], "name": "Patriotic Millionaires", "desc": ""},
    45: {"temas": ["ECON"], "name": "MLM", "desc": ""},
    46: {"temas": ["ECON"], "name": "Economía de la Atención", "desc": ""},
    47: {"temas": ["ECON"], "name": "Extractivismo", "desc": ""},
    48: {"temas": ["ECON", "POL"], "name": _l("Curva de Laffer"), "desc": _l("<p>Relación entre el <b>porcentaje de impuestos</b> que se le exige a los ricos y la <b>recaudación</b> que se puede conseguir con ese porcentaje, suponiendo que esos ricos se pudieran llevar sus riquezas a otros países si el porcentaje sube más de lo que están dispuestos a soportar.</p><p>La idea es que la <b>máxima recaudación</b> ocurre en un punto por el medio entre <i>'Poco porcentaje pero hay muchos ricos'</i> y <i>'Mucho porcentaje pero quedan pocos ricos'</i>. El modelo es criticablemente simple, pero los análisis empíricos dicen que la mayoría de los países están <b>por debajo</b> del punto óptimo (i.e. que les valdría la pena subir el impuesto a los ricos <i>incluso</i> si eso hace que una parte de ellos se vayan).")},
    49: {"temas": ["ECON"], "name": "Better Life Index", "desc": ""},
    50: {"temas": ["ECON", "POL"], "name": "Violencia Simbólica", "desc": ""},
    51: {"temas": ["ECOL"], "name": "Tipping Points", "desc": ""},
    52: {"temas": ["ECOL"], "name": "Temperatura de Bulbo Húmedo", "desc": ""},
    53: {"temas": ["ECOL"], "name": "NIMBY", "desc": ""},
    54: {"temas": ["ECOL"], "name": "Self-Organized Criticality", "desc": ""},  # ft els incendis s'apaguen a l'hivern
    55: {"temas": ["ECOL"], "name": "Greenwashing", "desc": ""},  # e.g. Gas 'Natural'
    57: {"temas": ["ECOL"], "name": "Semillas con derechos de autor", "desc": ""},
    58: {"temas": ["ECOL"], "name": "La trampa de la fruta sin pepitas", "desc": ""},
    59: {"temas": ["ECOL"], "name": "Ciclo de vida del producto", "desc": ""},
    60: {"temas": ["ECOL"], "name": "Responsabilidad corporativa", "desc": ""},

    71: {"temas": ["TEC"], "name": "FOSS", "desc": ""},
    72: {"temas": ["TEC"], "name": "KISS", "desc": ""},
    74: {"temas": ["TEC"], "name": "Alineamento de los Mesa-objectivos", "desc": ""},
    75: {"temas": ["TEC"], "name": "Las empresas de IA trituran llibros únicos", "desc": ""},
    76: {"temas": ["TEC"], "name": "Una máquina de adivinar palabras", "desc": ""},
    77: {"temas": ["TEC"], "name": "Creador vs Influencer", "desc": ""},
    78: {"temas": ["TEC"], "name": "Graceful degradation", "desc": ""},
    79: {"temas": ["TEC"], "name": "Model collapse", "desc": ""},

    81: {"temas": ["ESTAD"], "name": "Correlació vs Causalitat", "desc": ""},
    82: {"temas": ["ESTAD"], "name": "Ley de los números realmente grandes", "desc": ""},

    91: {"temas": ["ANT"], "name": "Els bons guanyen si estan connectats", "desc": ""},  # ft veritasium
    92: {"temas": ["ANT"], "name": "Comunicació NoViolenta", "desc": ""},
    93: {"temas": ["ANT"], "name": "Game Theory", "desc": ""},

    101: {"temas": ["FIS"], "name": "L'univers té píxels", "desc": ""},
    102: {"temas": ["FIS"], "name": "La paradoxa de Fermi", "desc": ""},
    103: {"temas": ["FIS"], "name": "La cosa és més a prop quan corres", "desc": ""},
    104: {"temas": ["FIS"], "name": "El temps passa més lent a l'everest", "desc": ""},
    105: {"temas": ["FIS"], "name": "Acció", "desc": ""},

    111: {"temas": ["SAL"], "name": "Violència Obstèrica", "desc": ""},
    112: {"temas": ["SAL"], "name": "Endometrosis", "desc": ""},
    113: {"temas": ["SAL"], "name": "La medicina es basa en el cos dels homes", "desc": ""},
    114: {"temas": ["SAL"], "name": "El primer Crash Test Dummy femení", "desc": ""},
    115: {"temas": ["SAL"], "name": "Placebo", "desc": ""},
    116: {"temas": ["SAL"], "name": "Nocebo", "desc": ""},
    117: {"temas": ["SAL"], "name": "Homeopatia", "desc": _l("La superstición que dice que puedes fabricar el antídoto para un veneno a base de mezclar ese mismo veneno con tantísima agua que al final sólo te queda agua.")},
    118: {"temas": ["SAL"], "name": "Psicosomàtic", "desc": ""},

    121: {"temas": ["PSI"], "name": "Freud s'ho patillava tot", "desc": ""},
    122: {"temas": ["PSI"], "name": "Biaix de supervivència", "desc": ""},
    123: {"temas": ["PSI"], "name": "Biaix de confirmació", "desc": ""},
    124: {"temas": ["PSI"], "name": "Biaix d'autoritat", "desc": ""},
    125: {"temas": ["PSI"], "name": "L'enneagrama no funciona", "desc": ""},
    126: {"temas": ["PSI"], "name": "Big 5", "desc": ""},
    127: {"temas": ["PSI"], "name": "Quan vam posar a prova els astròlegs", "desc": ""},
    128: {"temas": ["PSI"], "name": "Flow", "desc": ""},  # ft czickszentmihalyi
    129: {"temas": ["PSI"], "name": "Dunning-Krugger", "desc": ""},
    130: {"temas": ["PSI"], "name": "Biaix de disponibilitat", "desc": ""},
    131: {"temas": ["PSI"], "name": "Mem", "desc": ""},
    132: {"temas": ["PSI"], "name": "White Savior Complex", "desc": ""},
    133: {"temas": ["PSI"], "name": "Autotèlic vs Heterotèlic", "desc": ""},
    134: {"temas": ["PSI"], "name": _l("Saliencia"), "desc": _l("La facilidad que tiene algo para destacar sobre lo demás. Especialmente relevante en la [[Economía de la Atención|46]].")},
    135: {"temas": ["PSI"], "name": "Saturación semántica", "desc": ""},

    141: {"temas": ["ART"], "name": "Si l'autor cobra, no el pots separar de l'obra", "desc": ""},  # ft rowling
    142: {"temas": ["ART"], "name": "L'espai negatiu", "desc": ""},
    143: {"temas": ["ART"], "name": "Kerning", "desc": ""},

    151: {"temas": ["BIO"], "name": "Peix no significa res", "desc": ""},
    152: {"temas": ["BIO"], "name": "Els ocells són dinosaures", "desc": ""},
    153: {"temas": ["POL"], "name": "Poder blando", "desc": ""},

    160: {"temas": ["URB"], "name": "Camino del Deseo", "desc": ""},
    161: {"temas": ["POL"], "name": "Golpe blando", "desc": ""},
    162: {"temas": ["ANT"], "name": "Cultura de la violación", "desc": ""},

}
