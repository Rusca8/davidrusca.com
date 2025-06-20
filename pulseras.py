"""Creado a posteriori. Datos sobre los colores y diseños.
Idealmente, los colores del JS y esas cosas beberían de aquí para centralizarlo.
"""
from flask_babel import gettext

beads = {
    1: {
        "hex": "#1c1c1c",
        "nombre": "negro",
        "prod": [{"brand": "MY", "id": "OL-464"}, {"brand": "MY", "id": "O-401"}],
    },
    2: {
        "hex": "#f2f2f2",
        "nombre": "blanco",
        "prod": [{"brand": "MY", "id": "OL-420"}],
    },
    3: {
        "hex": "#ffdf0f",
        "nombre": "amarillo",
        "prod": [{"brand": "my", "id": "OL-422"}],
    },
    4: {
        "hex": "#fc7b2b",
        "nombre": "naranja",
        "prod": [{"brand": "my", "id": "OL-423"}],
    },
    5: {
        "hex": "#e02b2b",
        "nombre": "rojo",
        "prod": [{"brand": "my", "id": "OL-425"}],
    },
    6: {
        "hex": "#8a2424",
        "nombre": "granate",
        "prod": [{"brand": "my", "id": "OL-426"}],
    },
    7: {
        "hex": "#492c96",
        "nombre": "azul oscuro",
        "prod": [{"brand": "my", "id": "OL-434"}],
    },
    8: {
        "hex": "#50b9eb",
        "nombre": "azul parís",
        "prod": [{"brand": "th", "id": "OL-403"}],
    },
    9: {
        "hex": "#9ae4f5",
        "nombre": "azul claro",
        "prod": [{"brand": "th", "id": "OL-124"}],
    },
    10: {
        "hex": "#dff048",
        "nombre": "verde amarillo",
        "prod": [{"brand": "my", "id": "OL-439"}],
    },
    11: {
        "hex": "#4ca652",
        "nombre": "verde",
        "prod": [{"brand": "my", "id": "OL-431"}],
    },
    12: {
        "hex": "#616061",
        "nombre": "gris gunmetal",
        "prod": [{"brand": "my", "id": "M-451"}],
    },
    13: {
        "hex": "#fcd9eb",
        "nombre": "rosa",
        "prod": [{"brand": "my", "id": "OL-428"}],
    },
    14: {
        "hex": "#f0c169",
        "nombre": "beige",
        "prod": [{"brand": "th", "id": "OL-123D"}],
    },
    15: {
        "hex": "#fce9dc",
        "nombre": "crema",
        "prod": [{"brand": "my", "id": "CY-529"}],
    },
    16: {
        "hex": "#80edd9",
        "nombre": "turquesa",
        "prod": [{"brand": "th", "id": "OR-413"}],
    },
    17: {
        "hex": "#1f5c35",
        "nombre": "verde oscuro",
        "prod": [{"brand": "th", "id": "OL-130D?"}],
    },
    18: {
        "hex": "#8486e8",
        "nombre": "lila",
        "prod": [{"brand": "my", "id": "CY-538"}],
    },
}

designs = {
    gettext("Arcoíris"): {
        "Simple": {
            "id": "Ai",
            "code": "7,8,9,10,3,4,5,6x12",
        },
        gettext("Negro"): {
            "id": "An",
            "code": "5,6,1,1,7,8,9,10,3,4x10",
        },
        gettext("Suave"): {
            "id": "Sn",
            "code": "3,4,5,3,4,5,3,4,5,3,4,5,4,5,6,4,5,6,4,5,6,4,5,6,5,6,7,5,6,7,5,6,7,5,6,7,6,7,8,6,7,8,6,7,8,6,7,8,7,8,9,7,8,9,7,8,9,7,8,9,8,9,10,8,9,10,8,9,10,8,9,10,9,10,3,9,10,3,9,10,3,9,10,3,10,3,4,10,3,4,10,3,4,10,3,4",
            "sub": "Neus",
            "date": "2011-06",
            "notes": gettext("Como despedida y recuerdo el último día de conservatorio."),
        },
    },
    gettext("Pulso de color"): {
        gettext("Azul"): {
            "id": "Ak",
            "code": "1,7,8,9,8,7,1,12x12",
            "sub": "Gina",
            "date": "2011-04",
            "notes": gettext("Como regalo en un reencuentro después de la orquestada."),
        },
        gettext("Verde"): {
            "id": "Ak_v",
            "code": "1,11,10,3,10,11,1,12x12",
        },
        gettext("Rojo"): {
            "id": "Ak_r",
            "code": "1,5,4,3,4,5,1,12x12",
        },
    },
    gettext("Luz y sombra"): {
        gettext("Iceberg"): {
            "id": "Se",
            "sub": "Evgenia",
            "notes": gettext("Como despedida y recuerdo el último día de casal de tenis."),
            "code": "8,7,8,9,7,8,9,7,8,9,8,9,2,8,9,2,8,9,2,9,2,9,2,2,2,9,2,9,8,2,9,8,2,9,8,9,8,7,9,8,7,9,8,7,8,7,8,7,7,7,8,7,8,9,7,8,9,7,8,9,8,9,2,8,9,2,8,9,2,9,2,9,2,2,2,9,2,9,8,2,9,8,2,9,8,9,8,7,9,8,7,9,8,7,8,7,8,7,7,7",
        },
        gettext("Incendio"): {
            "id": "Se_i",
            "sub": "Judit",
            "notes": gettext("Como despedida y recuerdo el último día de casal de tenis."),
            "code": "4,5,4,3,5,4,3,5,4,3,4,3,2,4,3,2,4,3,2,3,2,3,2,2,2,3,2,3,4,2,3,4,2,3,4,3,4,5,3,4,5,3,4,5,4,5,4,5,5,5,4,5,4,3,5,4,3,5,4,3,4,3,2,4,3,2,4,3,2,3,2,3,2,2,2,3,2,3,4,2,3,4,2,3,4,3,4,5,3,4,5,3,4,5,4,5,4,5,5,5",
        },
        gettext("Erupción"): {
            "id": "Se_e",
            "code": "5,6,5,4,6,5,4,6,5,4,5,4,3,5,4,3,5,4,3,4,3,4,3,3,3,4,3,4,5,3,4,5,3,4,5,4,5,6,4,5,6,4,5,6,5,6,5,6,6,6,5,6,5,4,6,5,4,6,5,4,5,4,3,5,4,3,5,4,3,4,3,4,3,3,3,4,3,4,5,3,4,5,3,4,5,4,5,6,4,5,6,4,5,6,5,6,5,6,6,6",
        },
        gettext("Jungla"): {
            "id": "Se_j",
            "code": "17,6,17,11,6,17,11,6,17,11,17,11,10,17,11,10,17,11,10,11,10,11,10,10,10,11,10,11,17,10,11,17,10,11,17,11,17,6,11,17,6,11,17,6,17,6,17,6,6,6,17,6,17,11,6,17,11,6,17,11,17,11,10,17,11,10,17,11,10,11,10,11,10,10,10,11,10,11,17,10,11,17,10,11,17,11,17,6,11,17,6,11,17,6,17,6,17,6,6,6",
        }
    },
    gettext("Cuatro elementos"): {
        gettext("Tierra"): {
            "id": "E",
            "code": "1,3,4,3,3,4,4,3,4,4,4,5,4,4,5,4,5,5,5,5,1,12,2,12,1,1,9,8,9,9,8,8,9,8,8,8,7,8,8,7,8,7,7,7,7,1,12,2,12,1,1,3,14,3,3,14,14,3,14,14,14,6,14,14,6,14,6,6,6,6,1,12,2,12,1,1,2,9,2,2,9,9,2,9,9,9,8,9,9,8,9,8,8,8,8,1,12,2,12,1",
        },
        gettext("Bosque"): {
            "id": "E",
            "code": "1,3,4,3,3,4,4,3,4,4,4,5,4,4,5,4,5,5,5,5,1,12,2,12,1,1,9,8,9,9,8,8,9,8,8,8,7,8,8,7,8,7,7,7,7,1,12,2,12,1,1,10,11,10,10,11,11,10,11,11,11,6,11,11,6,11,6,6,6,6,1,12,2,12,1,1,2,9,2,2,9,9,2,9,9,9,8,9,9,8,9,8,8,8,8,1,12,2,12,1",
        }
    },
    gettext("Dibujando cosas"): {
        gettext("Día soleado"): {
            "id": "En",
            "code": "9,9,8,9,9,9,9,3,9,9,9,3,3,9,9,3,3,3,9,3,3,3,3,3,3,3,3,9,3,3,3,9,9,3,3,9,9,9,3,9,9,9,9,8,9,9,9,8,8,9,9,8,8,8,9,8,8,8,8,10,10,10,10,11,11,10,10,10,11,11,11,11,10,11,11,11,11,10,10,10,11,11,10,10,10,10,8,8,8,8,9,8,8,8,9,9,8,8,9",
        },
        gettext("Ying-Yang en color"): {
            "id": "Yy",
            "code": "1,1,7,18,8,9,2,9,2,2,1,5,6,4,3,3,4,6,5,1,2,2,2,2,2,9,2,2,9,2,9,8,2,9,8,9,8,18,9,8,18,8,18,7,18,7,1,7,1,1,2,2,3,4,5,6,1,6,1,1,2,8,9,18,7,7,18,9,8,2,1,1,1,1,1,6,1,1,6,1,6,5,1,6,5,6,5,4,6,5,4,5,4,3,4,3,2,3,2,2",
        }
    },
    gettext("Escondiendo mensajes"): {
        gettext("Agua y cuarzo (Morse: David)"): {
            "id": "Md",
            "code": "8,7,7,8,8,8,7,8,8,8,8,9,8,8,8,9,9,8,8,9,9,9,9,9,9,9,9,9,8,8,9,9,8,8,8,9,8,8,8,8,7,8,8,8,7,7,8,8,7,7,7,8,7,7,7,7,1,2,1,2,1,1,2,2,1,10,1,2,10,1,1,10,1,10,1,10,1,10,10,1,1,2,1,10,2,1,2,1,2,1,1,7,7,7,7,8,7,7,7,8",
        }
    },
    "hidden": {
        "": {"id": "", "code": ""},
        "Mercè": {"id": "Lx",
             "sub": "Mercè",
             "date": "2021-07",
             "code": "1,1,7,1,7,18,1,7,18,8,7,18,8,18,8,9,8,9,2,8,9,2,9,2,9,2,2,2,3,2,3,2,3,4,2,3,4,3,4,5,4,5,6,4,5,6,1,5,6,1,6,1,1,1,7,1,7,18,1,7,18,8,7,18,8,18,8,9,8,9,2,8,9,2,9,2,9,2,2,2,3,2,3,2,3,4,2,3,4,3,4,5,4,5,6,4,5,6,1,5,6,1,6,1"
        },
        "Marta": {
            "id": "Lx_m",
            "sub": "Marta",
            "date": "2021-11",
            "code": "1,1,6,1,6,5,6,5,4,6,5,4,5,4,14,4,14,2,4,14,2,14,2,14,2,2,2,3,2,3,2,3,10,2,3,10,3,10,11,10,11,17,10,11,17,11,17,1,17,1,1,1,6,1,6,5,6,5,4,6,5,4,5,4,14,4,14,2,4,14,2,14,2,14,2,2,2,3,2,3,2,3,10,2,3,10,3,10,11,10,11,17,10,11,17,11,17,1,17,1"
        },
        "Shs_Brils": {
            "id": "Sh_b",
            "code": "1,17,1,17,11,17,11,10,11,10,3,10,3,2,3,2,2,2,3,2,3,4,3,4,5,4,5,6,5,6,1,6,1,1,1,17,1,17,11,17,11,10,11,10,3,10,3,2,3,2,2,2,3,2,3,4,3,4,5,4,5,6,5,6,1,6,1,1,1,17,1,17,11,17,11,10,11,10,3,10,3,2,3,2,2,2,3,2,3,4,3,4,5,4,5,6,5,6,1,6,1,1",
            "sub": "Brils",
            "date": "2022-07",
            "notes": gettext("Como despedida y recuerdo el último día de orquesta del curso."),
        },
        "Shs_Emma": {
            "id": "Sh_b",
            "code": "1,7,1,7,18,7,18,8,18,8,9,8,9,2,9,2,2,2,3,2,3,4,3,4,5,4,5,6,5,6,1,6,1,1,1,7,1,7,18,7,18,8,18,8,9,8,9,2,9,2,2,2,3,2,3,4,3,4,5,4,5,6,5,6,1,6,1,1,1,7,1,7,18,7,18,8,18,8,9,8,9,2,9,2,2,2,3,2,3,4,3,4,5,4,5,6,5,6,1,6,1,1",
            "sub": "Emma",
            "date": "2022-07",
            "notes": gettext("Como despedida y recuerdo el último día de orquesta del curso."),
        },
        "Shs_Mireia": {
            "id": "Sh_b",
            "code": "1,7,1,7,18,7,18,8,18,8,9,8,9,2,9,2,2,2,3,2,3,10,3,10,11,10,11,17,11,17,1,17,1,1,1,7,1,7,18,7,18,8,18,8,9,8,9,2,9,2,2,2,3,2,3,10,3,10,11,10,11,17,11,17,1,17,1,1,1,7,1,7,18,7,18,8,18,8,9,8,9,2,9,2,2,2,3,2,3,10,3,10,11,10,11,17,11,17,1,17,1,1",
            "sub": "Mireia",
            "date": "2022-07",
            "notes": gettext("Como despedida y recuerdo el último día de orquesta del curso."),
        },
        "Shs_Jo": {
            "id": "Sh_b",
            "code": "1,7,1,7,18,7,18,8,18,8,9,8,9,2,9,2,2,2,3,2,3,4,3,4,5,4,5,6,5,6,1,6,1,1,1,17,1,17,11,17,11,10,11,10,3,10,3,2,3,2,2,2,9,2,9,8,9,8,18,8,18,7,18,7,1,7,1,1,1,6,1,6,5,6,5,4,5,4,3,4,3,2,3,2,2,2,3,2,3,10,3,10,11,10,11,17,11,17,1,17,1,1",
            "sub": "(" + gettext("para mí") + ")",
            "date": "2022-07",
            "notes": gettext("Entrelazando los colores de las otras tres."),
        },
        "Sunlai_L": {
            "id": "Ls",
            "code": "18,8,9,2,2,9,8,18,8,18,7,18,7,7,6,7,6,5,4,14,2,2,14,4,5,4,5,6,5,6,6,7,6,7,18,8,9,2,2,9,8,18,8,18,7,18,7,7,6,7,6,5,4,14,2,2,14,4,5,4,5,6,5,6,6,7,6,7,18,8,9,2,2,9,8,18,8,18,7,18,7,7,6,7,6,5,4,14,2,2,14,4,5,4,5,6,5,6,6,7,6,7",
            "sub": "Lai",
            "date": "2025-06",
            "notes": gettext("Como recuerdo de despedida y amuleto para selectividad."),
        },
        "Sunlai_S": {
            "id": "Ls_s",
            "code": "18,8,9,2,2,9,8,18,8,18,7,18,7,7,17,7,17,11,10,3,2,2,3,10,11,10,11,17,11,17,17,7,17,7,18,8,9,2,2,9,8,18,8,18,7,18,7,7,17,7,17,11,10,3,2,2,3,10,11,10,11,17,11,17,17,7,17,7,18,8,9,2,2,9,8,18,8,18,7,18,7,7,17,7,17,11,10,3,2,2,3,10,11,10,11,17,11,17,17,7,17,7",
            "sub": "Sun",
            "date": "2025-06",
            "notes": gettext("Como recuerdo de despedida y amuleto para selectividad."),
        },
    }
}


def get_chrono():
    chrono = []
    for group, combis in designs.items():
        for name, combi in combis.items():
            if "sub" in combi:
                chrono.append(combi)
    return sorted(chrono, key=lambda x: x.get("date", ""))
