import random


def new_bld_letters(scheme=None, n=16):
    try:
        n = int(n)
    except Exception as e:
        print(e)
        n = 16
    n = n + random.choice([0, 1])
    letters = [c for c in scheme]
    letters += random.choices(letters, k=random.randint(1, 3))
    random.shuffle(letters)
    n = min(len(letters), n)
    for i in reversed(range(len(letters) - 2)):
        if letters[i] == letters[i + 1]:
            letters[i + 1], letters[i + 2] = letters[i + 2], letters[i + 1]
    print(letters[:n])
    return "".join(letters[:n])
