from flask_babel import lazy_gettext as _l

docents = {
        _l("Bachillerato"): {
            "anchor": "BAT",
            "contents": {
                "General": {
                    "anchor": "BATgeneral",
                    "icon": "📚",
                    "contents": {
                        _l("Resumen"): {
                            _l("Las Carreras Explicadas"): {"lang": "CA", "prefix": "G", "url": "/carreres"}
                        },
                    },
                },
                _l("Mates científicas"): {
                    "anchor": "matesC",
                    "icon": "🔢",
                    "contents": {
                        _l("Esquemas y Formularios"): {
                            _l("Tipos de Funciones"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_TipusDeFuncions.pdf"},
                            _l("Ecuaciones exponenciales y logarítmicas"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M1_ExpLog.pdf"},
                            _l("Números Complejos"): {"lang": "CA", "prefix": "M1", "url": "/static/pdf/M1_Complexos.pdf"},
                            _l("Combinatoria"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_Combinatoria.pdf"},
                            _l("Probabilidad"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_Probabilitat.pdf"},
                            _l("Límites y Continuidad"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_LimitsCD.pdf"},
                            _l("Representación de funciones"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M2_Funcions.pdf"},
                            _l("Relación entre gráficas y derivadas"): {"lang": "CA", "prefix": "M2", "url": "/static/pdf/M2_VennDerivades.pdf", "extra_level": True},
                            _l("Recetas y Problemas de funciones"): {"lang": "CA", "prefix": "M2", "url": "/static/pdf/M2_Receptes.pdf"},
                            _l("Discusión de Sistemas"): {"lang": "CA", "prefix": "M2", "url": "/static/pdf/M2_Rouche.pdf"},
                            _l("Optimización"): {"lang": "CA", "prefix": "M2", "url": "/static/pdf/M2_Optimitzacio_v2.pdf"},
                            _l("Geometría 3D"): {"lang": "CA", "prefix": "M2", "url": "/static/pdf/M2_Geo3D.pdf"},
                        },
                        _l("Fichas"): {
                            _l("Ficha de Derivadas Definitiva"): {"prefix": "M", "url": "/static/pdf/M_Derivades.pdf"},
                            _l("Potencias y raíces"): {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/powsqr/"},
                            _l("Sistemas 3D"): {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/equacions/"},
                            _l("Derivadas"): {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/derivades/"},
                        },
                        _l("Temario"): {
                            _l("Temario optimizado") + " PAU": {"lang": "CA", "prefix": "M", "url": "/static/pdf/MPAU_Temari.pdf"},
                        },
                        "Labs": {
                            _l("Funciones trigonométricas"): {"lang": "CA", "prefix": "M", "url": "https://www.geogebra.org/m/cbtwmydd"},
                        }
                    }
                },
                _l("Mates sociales"): {
                    "anchor": "matesS",
                    "icon": "📈",
                    "contents": {
                        _l("Esquemas y Formularios"): {
                            _l("Tipos de Funciones"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_TipusDeFuncions.pdf"},
                            _l("Ecuaciones exponenciales y logarítmicas"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M1_ExpLog.pdf"},
                            _l("Combinatoria"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_Combinatoria.pdf"},
                            _l("Probabilidad"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_Probabilitat.pdf"},
                            _l("Límites y Continuidad"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_LimitsCD.pdf"},
                            _l("Matemática Financiera"): {"lang": "CA", "prefix": "MS1", "url": "/static/pdf/MS1_Financera.pdf"},
                            _l("Mnemotecnia Financiera"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/MS1_Financera_memo.pdf", "extra_level": True},
                            _l("Recetas y Problemas de funciones"): {"lang": "CA", "prefix": "M2", "url": "/static/pdf/M2_Receptes.pdf"},
                            _l("Representación de funciones"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M2_Funcions.pdf"},
                            _l("Relación entre gráficas y derivadas"): {"lang": "CA", "prefix": "M2", "url": "/static/pdf/M2_VennDerivades.pdf", "extra_level": True},
                            _l("Optimización"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M2_Optimitzacio_v2.pdf"},
                        },
                        _l("Fichas"): {
                            _l("Ficha de Derivadas Definitiva"): {"prefix": "M", "url": "/static/pdf/M_Derivades.pdf"},
                            _l("Potencias y raíces") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/powsqr/"},
                            _l("Sistemas 3D") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/equacions/"},
                            _l("Derivadas") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/derivades/"},
                        },
                        _l("Temario"): {
                            _l("Temario optimizado") + " PAU": {"lang": "CA", "prefix": "MS", "url": "/static/pdf/MSPAU_Temari.pdf"},
                        },
                    }
                },
                "Física": {
                    "anchor": "fis",
                    "icon": "📦",
                    "contents": {
                        _l("Formularios"): {
                            _l("Movimientos"): {"lang": "CA", "prefix": "F", "url": "/static/pdf/F1_Moviments.pdf"},
                            _l("Gráficos de MRUA"): {"lang": "", "prefix": "F", "url": "/static/img/F1_MRUA.png", "extra_level": True},
                            _l("Fuerzas"): {"lang": "CA", "prefix": "F", "url": "/static/pdf/F1_Forces.pdf"},
                            _l("Campo Gravitatorio y Eléctrico"): {"lang": "CA", "prefix": "F", "url": "/static/pdf/F2_CampsGE.pdf"},
                            _l("Física Nuclear"): {"lang": "CA", "prefix": "F", "url": "/static/pdf/F2_Nuclear.pdf"},
                            _l("Ondas"): {"lang": "CA", "prefix": "F", "url": "/static/pdf/F2_Ones.pdf", "wip": True},
                        }
                    },
                },
                "Química": {
                    "anchor": "quim",
                    "icon": "🧪",
                    "contents": {
                        _l("Apuntes"): {
                            _l("Números cuánticos"): {"lang": "CA", "prefix": "Q1", "url": "/static/pdf/Q1_QuanticNums.pdf"},
                            _l("Teorías Atómicas, Espectros y Cosas Cuánticas"): {"lang": "CA", "prefix": "Q1", "url": "/static/pdf/Q1_TeoriaAtomica.pdf"},
                            _l("Propiedades Periódicas"): {"lang": "CA", "prefix": "Q1", "url": "/static/pdf/Q1_PropietatsPeriodiques.pdf"},
                        },
                        _l("Formularios"): {
                            _l("Termoquímica"): {"lang": "CA", "prefix": "Q2", "url": "/static/pdf/Q2_Termoq.pdf"},
                        },
                        _l("Temario"): {
                            _l("Temario optimizado") + " PAU": {"lang": "CA", "prefix": "Q", "url": "/static/pdf/QPAU_Temari.pdf"},
                        },
                        _l("Mnemotecnia"): {
                            _l("Valencias de los Elementos"): {"lang": "CA", "prefix": "Q", "url": "/static/pdf/Mn_Valencies.pdf"},
                        },
                        "Labs": {
                            _l("Equilibrio Químico"): {"lang": "CA", "prefix": "Q", "url": "/labs/q/eq/"},
                            _l("Le Châtelier"): {"lang": "CA", "prefix": "Q", "url": "/labs/q/chatelier/"},
                            _l("Radio Atómico"): {"lang": "CA", "prefix": "Q", "url": "/labs/q/radi/"},
                        }
                    }
                },
                _l("Tecnología"): {
                    "anchor": "tecno",
                    "icon": "⚙️",
                    "contents": {
                        _l("Formularios"): {
                            _l("Formulario") + " PAU (2023)": {"lang": "CA", "prefix": "T", "url": "/static/pdf/T_FormulariPAU.pdf"},
                        }
                    }
                },
                _l("Dibujo técnico"): {
                    "anchor": "dt",
                    "icon": "📐",
                    "contents": {
                        _l("Apuntes"): {
                            _l("Poliedros: Construcciones Auxiliares y Vistas Principales"): {"lang": "CA", "prefix": "DT2", "url": "/static/pdf/DT_Poliedres.pdf"},
                        },
                        "Labs": {
                            _l("Cambios de plano"): {"lang": "CA", "prefix": "DT2", "url": "https://www.geogebra.org/m/nu3gubu7"},
                        }
                    }
                },
                _l("Economía de la empresa"): {
                    "anchor": "ede",
                    "icon": "💵",
                    "contents": {
                        _l("Apuntes"): {
                            _l("Asientos"): {"lang": "CA", "prefix": "EdE2", "url": "/static/pdf/EdE2_Assentaments.pdf"},
                            _l("Fuentes de Financiación"): {"lang": "CA", "prefix": "EdE2", "url": "/static/pdf/EdE2_FontsFin.pdf"},
                        },
                        "Labs": {
                            _l("Qué podría pagar con mil millones?"): {"lang": "CA", "prefix": "EdE", "url": "/labs/milmilionaris", "wip": True},
                        }
                    }
                },
            },
            "index_jump": True,
        },
        _l("Pruebas de Aptitud Personal"): {
            "anchor": "PAP",
            "contents": {
                _l("Competencia Logicomatemática"): {
                    "anchor": "clomPAP",
                    "icon": "🔢",
                    "contents": {
                        _l("Resumen"): {
                            _l("Resumen") + " EsPAPtacular": {"lang": "CA", "prefix": "PAP", "url": "/static/pdf/PAP_Resum.pdf"},
                        },
                        "Labs": {
                            _l("Calcula la nota de mates"): {"lang": "CA", "prefix": "PAP", "url": "/papuladora"},
                        }
                    }
                },
            },
        },
        _l("Prueba de acceso") + " CFGS": {
            "anchor": "CFGS",
            "contents": {
                _l("Dibujo Técnico"): {
                    "anchor": "dtCFGS",
                    "icon": "📐",
                    "contents": {
                        _l("Temario"): {
                            _l("Temario optimizado"): {"lang": "CA", "prefix": "DT", "url": "/static/pdf/DTGS_Temari.pdf"},
                        }
                    }
                },
                _l("Tecnología"): {
                    "anchor": "tecnoCFGS",
                    "icon": "⚙️",
                    "contents": {
                        _l("Temario"): {
                            _l("Temario optimizado"): {"lang": "CA", "prefix": "T", "url": "/static/pdf/TGS_Temari.pdf"},
                        }
                    }
                },
            },
        },
        _l("Prueba de acceso") + " CFGM": {
            "anchor": "CFGM",
            "contents": {
                _l("Tecnología"): {
                    "anchor": "tecnoCFGM",
                    "icon": "⚙️",
                    "contents": {
                        _l("Fichas"): {
                            _l("Circuitos Eléctricos"): {"lang": "CA", "prefix": "T", "url": "/static/pdf/T_Circuits.pdf"},
                            _l("Electrónica Digital"): {"lang": "CA", "prefix": "T", "url": "/static/pdf/T_ElectroDigital.pdf"},
                            _l("Energías"): {"lang": "CA", "prefix": "T", "url": "/static/pdf/T_Energies.pdf"},
                            _l("Pneumática"): {"lang": "CA", "prefix": "T", "url": "/static/pdf/T_Pneum.pdf"},
                            _l("Telecomunicaciones"): {"lang": "CA", "prefix": "T", "url": "/static/pdf/T_Telecos.pdf"},
                            _l("Máquinas de Combustión"): {"lang": "CA", "prefix": "T", "url": "/static/pdf/T_Comb.pdf"},
                        }
                    }
                },
            },
        },
        _l("Grado Profesional de Música"): {
            "anchor": "musGP",
            "contents": {
                _l("Armonía"): {
                    "anchor": "harmonia",
                    "icon": "🎼",
                    "contents": {
                        _l("Apuntes"): {
                            _l("Canciones para los intervalos"): {"lang": "CA", "prefix": "H", "url": "/static/pdf/MusGP_Intervals.pdf"},
                        },
                        "App": {
                            _l("Editor de Esquemas Armónicos"): {"lang": "CA", "prefix": "H", "url": "https://play.google.com/store/apps/details?id=com.rusca8.hEditor.android"},
                        }
                    }
                },
            },
            "index_jump": True,
        },
        _l("Educación Secundaria (ESO)"): {
            "anchor": "ESO",
            "contents": {
                "Mates": {
                    "anchor": "matesESO",
                    "icon": "🔢",
                    "contents": {
                        _l("Formularios"): {
                            _l("Combinatoria"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M_Combinatoria.pdf"},
                            _l("Ecuaciones exponenciales y logarítmicas"): {"lang": "CA", "prefix": "M", "url": "/static/pdf/M1_ExpLog.pdf"},
                        },
                        _l("Fichas"): {
                            _l("Operaciones con Enteros") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/enters/"},
                            _l("Fracciones") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/fraccions/"},
                            _l("Potencias y raíces") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/powsqr/"},
                            _l("Ecuaciones") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/equacions/"},
                            _l("Proporcionalidad") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/proporcionalitat/"},
                        },
                        "Labs": {
                            _l("Funciones trigonométricas"): {"lang": "CA", "prefix": "M", "url": "https://www.geogebra.org/m/cbtwmydd"},
                        }
                    }
                },
                _l("Física y Química"): {
                    "anchor": "natusESO",
                    "icon": "🔬",
                    "contents": {
                        "Labs": {
                            _l("Masa y peso"): {"lang": "CA", "prefix": "FiQ", "url": "/labs/pmg"},
                        },
                        _l("Mnemotecnia"): {
                            _l("Valencias de los Elementos"): {"lang": "CA", "prefix": "FiQ", "url": "/static/pdf/Mn_Valencies.pdf"},
                        }
                    }
                },
                _l("Tecnología"): {
                    "anchor": "tecnoESO",
                    "icon": "⚙️",
                    "contents": {
                        _l("Formularios"): {
                            _l("Rendimiento"): {"lang": "CA", "prefix": "T2E", "url": "/static/pdf/T2E_Rendiment.pdf"},
                        },
                        _l("Fichas"): {
                            _l("Fuerzas"): {"lang": "CA", "prefix": "T3E", "url": "/static/pdf/T3E_Forces.pdf"},
                            _l("Máquinas simples"): {"lang": "CA", "prefix": "T3E", "url": "/static/pdf/T3E_MSimples2_CA.pdf"},
                            _l("Máquinas simples") + " (sim. ex.)": {"lang": "CA", "prefix": "T3E", "url": "/static/pdf/T3E_MSimples_CA.pdf", "altlang": {"EN": "/static/pdf/T3E_MSimples_EN.pdf"}},
                        }
                    }
                },
                _l("Sociales"): {
                    "anchor": "socialsESO",
                    "icon": "👤",
                    "contents": {
                        _l("Mnemotecnia"): {
                            _l("Comarcas de Cataluña"): {"lang": "CA", "prefix": "SE", "url": "/static/pdf/Mn_Comarques.pdf"},
                        }
                    }
                },
                _l("Inglés"): {
                    "anchor": "angESO",
                    "icon": "🇬🇧",
                    "contents": {
                        "Online": {
                            "Irregular Verbs Test": {"lang": "CA/ES", "prefix": "EE", "url": "/ivtest", "ft": "Josep Ruscalleda"},
                        }
                    }
                },
            }
        },
        _l("Educación Primaria (EP)"): {
            "anchor": "EP",
            "contents": {
                "Mates": {
                    "anchor": "matesEP",
                    "icon": "🔢",
                    "contents": {
                        _l("Fichas"): {
                            _l("Operaciones sencillas") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/enters/"},
                            _l("Ecuaciones sencillas") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/equacions/"},
                            _l("Operaciones en columna") + " (Dynamic Deures)": {"lang": "CA", "prefix": "M", "url": "http://ruscalatex.eu.pythonanywhere.com/apilades/"},
                        }
                    }
                }
            },
            "index_jump": True,
        },
        _l("Misceláneo"): {
            "anchor": "MISC",
            "contents": {
                _l("Programación"): {
                    "anchor": "coding",
                    "icon": "🖥",
                    "contents": {
                        _l("Apuntes"): {
                            _l("Apuntes") + " HTML / CSS / JS / LaTeX": {"lang": "CA", "prefix": "P", "url": "/anki/code/"},
                            _l("Apuntes y Trucos") + " Python": {"lang": "CA", "prefix": "P", "url": "/static/pdf/Python.pdf"},
                        }
                    }
                },
                "Sardanes": {
                    "anchor": "sardanes",
                    "icon": "🩰",
                    "contents": {
                        _l("Apuntes"): {
                            _l("El Manual Definitiu de Repartiment"): {"lang": "CA", "prefix": "SAR", "url": "/static/pdf/manual_definitiu_de_repartiment.pdf"},
                        }
                    }
                },
                "Kubb": {
                    "anchor": "kubb",
                    "icon": "👑",
                    "contents": {
                        _l("Apuntes"): {
                            _l("Reglament"): {"lang": "CA", "prefix": "K", "url": "/static/pdf/kubb_CA.pdf"},
                        }
                    }
                },
                _l("Juegos de Lengua"): {
                    "anchor": "llengua",
                    "icon": "✏️",
                    "contents": {
                        "Online": {
                            _l("Diacríptic"): {"lang": "CA", "prefix": "LL", "url": "/diacriptic/"},
                            _l("Catagrama del día"): {"lang": "CA", "prefix": "LL", "url": "/catagrama/"},
                            _l("Crucigramas crípticos"): {"lang": "CA", "prefix": "LL", "url": "/encreuats/"},
                        }
                    }
                },
                _l("Ventriloquía"): {
                    "anchor": "ventri",
                    "icon": "🙊",
                    "contents": {
                        "Lab": {
                            _l("Traductor de Ventriloquía"): {"lang": "CA", "prefix": "V", "url": "/ventriloquia/"},
                        }
                    }
                }
            }
        }
    }

juegos = {
    _l("Juegos digitales"): {
        "anchor": "",
        "contents": {
            _l("Juegos de Lengua"): {"icon": "✏️", "anchor": "lengua"},
            _l("Juegos de Mates"): {"icon": "🔢", "anchor": "mates"},
        },
        "index_jump": True,
    },
    _l("Diseños de juegos de mesa"): {
        "anchor": "bgdesign",
        "contents": {
            _l("Prototipos"): {
                "anchor": "protos",
                "icon": "🚧",
            }
        },
        "index_jump": True,
    },
    _l("Recursos para juegos de mesa"): {
        "anchor": "bgrec",
        "contents": {
            _l("Dragones y Mazmorras (5ª Edición)"): {
                "icon": "⚔️",
                "anchor": "DnD5e",
            },
            "Terraforming Mars": {
                "icon": "🌏",
                "anchor": "terraforming",
            },
            "Riichi Mahjong": {
                "icon": "🀄️",
                "anchor": "riichi",
            }
        }
    }
}
