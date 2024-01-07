'''
Texto críptico para el cumple de Raquel. Traductor py.
'''
import random
from unidecode import unidecode


def cesar(text, key):
    if key == 0:  # 0
        return text
    else:
        text = text.replace("á", chr(97)).replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")\
            .replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")\
            .replace("ñ", "n").replace("Ñ", "N").replace("ü", "u").replace("ï", "i")
        cipher = ""
        for x in range(len(text)):
            if text[x].isalpha():
                if text[x].islower():
                    cipher += chr((ord(text[x]) - 97 + key) % 26 + 97)
                else:
                    cipher += chr((ord(text[x]) - 65 + key) % 26 + 65)
            else:
                cipher += text[x]
        return cipher


def cesarhtml(text, key):
    in_tag = False
    if key == 0:  # 0
        return text
    else:
        text = text.replace("á", chr(97)).replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")\
            .replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")\
            .replace("ñ", "n").replace("Ñ", "N")
        cipher = ""
        for x in range(len(text)):
            if in_tag:
                if text[x] == ">":
                    in_tag = False
                cipher += text[x]
            else:
                if text[x] == "<":
                    in_tag = True
                    cipher += text[x]
                else:
                    if text[x].isalpha():
                        if text[x].islower():
                            cipher += chr((ord(text[x]) - 97 + key) % 26 + 97)
                        else:
                            cipher += chr((ord(text[x]) - 65 + key) % 26 + 65)
                    elif text[x].isnumeric():
                        cipher += f"{(int(text[x]) + key) % 10}"
                    else:
                        cipher += text[x]
        return cipher


raquel_text = '''
<h5>Bueeno, pues ya está!</h5>
...qué tal el viaje? jeje<br><br>

Tu amiga debe de haberme asesinado mentalmente con lo del vídeo de dos minutos hablando al revés...<br>
(y no sé si quiero saber cómo se las habrá apañado para usarlo), pero mira, así nos hemos echado unas risas.<br><br>

<i>...por cierto, si quieres ver el guión que he usado para grabarlo, puedes teclear "alcachofa".</i>
<hr>
 
En fin, que hace unos días me acordé de algo que escribí en 2011, hablando de ti.<br>
Es más o menos de la época en la que descubrí la filosofía, y entonces solía escribir de vez en cuando cosillas<br>
(en un blog que casi nadie sabía que existía) sobre la amistad y sobre las emociones y cosas así.<br><br>
...y por supuesto en esa época tú ya formabas parte de <i>esas</i> cosas.
<hr>
El blog lo escribía en catalán, en realidad (y si te digo la verdad las entradas tan antiguas me dan casi vergüenza),<br>
pero pensé que te traduciría algunos cachos de ese texto por tu cumple, que sería bonito.<br><br>

<i>...y bueno, luego la cosa se desmadró con lo del vídeo de Bea y aquí estamos. pffjajaja</i><br><br>

Pero te lo dejo aquí, que si has llegado casi te lo mereces ;)<br><br>

<div class="card raquel">
<div class="card-header">
    Julio de 2011 - <i>Por qué los niños pequeños se parecen a las frutas.</i>
</div>
<div class="card-body">

    Tenemos un problema a la hora de tratar con los niños pequeños.<br>
    De hecho, tenemos un problema a la hora de tratar a cualquier persona,<br> 
    pero con los niños pequeños es donde se ve de una manera más clara.<br><br>
    Que cuál es el problema? El problema se resume en una pregunta:<br>
    "En qué te basas para decidir cómo tratarás a alguien?".<br> 
    ...al principio, cuando no lo conoces.<br><br>
    
    Parece que tendemos a tratar a los demás por lo que son, en lugar de por <i>quién</i> son,<br>
    (...) generalizando, y considerando a las personas según su franja de edad (u otras clasificaciones),<br>
    y entendiéndolas según las etiquetas que las contengan (cuando en realidad podrían estar clasificadas<br>
    de cualquier otra manera, según cualquier otro parámetro).<br><br>
    Y esto, aunque con un abuelo podría suponer sólo que nos diga "tranquilo, ya puedo yo sólo",<br>
    con los más pequeños puede acabar siendo el motivo de que les neguemos sin darnos cuenta<br>
    la oportunidad de mostrar de verdad lo que son, y cómo de bonito es el corazón que llevan dentro.<br><br>
    
    (...)<br><br> 
    
    Pero a qué viene toda esta reflexión? (...) Todo empezó a raíz de una prima segunda que tengo<br>
    en Soria y que veo por vacaciones. Tiene diez años menos (tendrá unos seis, si no ha cumplido),<br>
    y los últimos dos (calculo a ojo), me ha ido cogiendo cariño ...y bueno, yo también.<br> 
    Pero parece que se ve más en una niña pequeña, por lo de que habla de mí y pregunta por mí a menudo.<br><br>
    
    ...y este hablarles de mí a los mayores llegó a un punto en el que un día me acabaron preguntando,<br>
    literalmente<code>*</code>: <i>"Pero qué le das a esta niña?"</i>.<br>
    
    <br><code>*Tu abuela, en concreto. ajajaja</code><br><br>
    Y claro, en el momento no supe qué contestar, pero me dejó pensando si habría hecho algo en especial.<br><br>
    
    (...) "lo mismo que a cualquier otra gran amiga", pensé (ya demasiado tarde). Pero era esa la respuesta.<br>
    Primero remarcar la fuerte amistad, y luego dar a entender que es precisamente no tratarla distinto<br>
    lo que marca la diferencia.<br><br>
    
    (...)<br><br>
    
    Tratarla por <i>quén</i> es (una amiga de verdad) y no por <i>qué</i> es (una niña pequeña, separada por diez años).<br>
    
    <hr>
    <div class="ml-4">
    "Nada de especial (por lo que es), pero todo lo especial. Por <i>quién</i> es.<br><br>
    
    Y mientras no podáis salir del <i>qué</i> la seguiréis tratando <i>sólo</i> como a una niña pequeña.<br>
    Y seguiréis sin poder entender nada de todo lo que lleva dentro.<br><br>
    
    (...)<br><br>
    
    Y pues qué hago? Que qué le doy?<br>
    Le doy la posibilidad de ser tratada no como a una niña pequeña, sino como a la persona bonita que es.<br><br>
    
    Y es eso, creo, y sólo eso, el motivo sencillo que hace que me quiera tanto.<br>
    Y es eso, creo, y sólo eso, lo que me permite a mí escapar de lo irrelevante del "<i>qué</i> es",<br>
    y quererla como la quiero... como demuestra su <i>quién</i> cómo de fácil es que la quieran."
    </div>
</div>
</div>
    <br>
    ...y pues ya ves.<br>
    Que no era broma cuando te decía que desde tus cuatro ya andábamos juntos.<br><br>
    Así que gracias, de verdad.<br><br>
    Por ser <i>quien</i> eres.<br>
'''


def new_transposition_alphabet(plaintext="ABCDEFGHIJKLMNOPQRSTUVWXYZ", return_plain=False, quote=None, avoid=""):
    """ Transposes plaintext so that letters aren't in their original places.
        If quote and avoid, tries to swap the "avoid" letters for letters not in the quote
    """
    # get letters not in quote, to swap for the "avoid" ones
    non_quote_letters = []
    if quote is not None and avoid:
        non_quote_letters = [c for c in plaintext if c not in quote]

    # filter avoided
    avoid = [c for c in avoid if c in plaintext]

    # place the unused ones on front
    plaintext = "".join(non_quote_letters) + "".join(c for c in plaintext if c not in non_quote_letters)

    # swapping (LTRand(R))
    alpha = [c for c in plaintext]
    for i in range(len(alpha)-1):
        if i < len(avoid) and i < len(non_quote_letters):  # if non_quote
            still_unavoided = [c for c in alpha[i:] if c in avoid]
            if still_unavoided:
                j = alpha.index(random.choice(still_unavoided))
            else:
                j = random.randint(i+1, len(alpha)-1)
        else:
            j = random.randint(i+1, len(alpha)-1)
        alpha[i], alpha[j] = alpha[j], alpha[i]
    else:
        if alpha[-1] == plaintext[-1]:
            j = random.randint(0, len(alpha)-2)
            alpha[-1], alpha[j] = alpha[j], alpha[-1]
    if return_plain:
        return plaintext, alpha
    return "".join(alpha)


def get_frequencies(text, only_alpha=True):
    freqs = {}
    for c in text:
        if c.isalpha():
            freqs[c] = freqs.get(c, 0) + 1
    return freqs


def unidecode_but(text, preserve="", post_replace=None):
    text = "".join(c if c in preserve else unidecode(c) for c in text)

    if post_replace:
        for old, new in post_replace.items():
            text = text.replace(old, new)

    return text
