import random


def index_word_from_wordlist(solution, clues, all_indices=False):
    """Chooses the appropiate letter from each clue in order to get the solution"""
    solution = solution.upper()
    clues = [c.upper() for c in clues]

    # get which words can provide each letter
    clue_options = []
    for letter in solution:
        clue_options.append([letter, [i for i, c in enumerate(clues) if letter in c]])
    #print(clue_options)

    """  # something goes wrong with this, cause the bottom part finds stuff that this would discard 
    simplified = True
    while simplified:
        simplified = False
        for n in range(len(clues)):
            appearances = []
            for i, l in enumerate(clue_options):
                if len(l[1]) == 1 and l[1][0] == n:  # n is the only choice for the letter
                    # delete it from any other appearance
                    for x in clue_options:
                        if n in x[1] and x != l:
                            simplified = True
                            x[1].remove(n)
                    continue
                elif n in l[1]:
                    appearances.append(i)
            if len(appearances) == 1:  # if word can only be in one place, puts it there
                clue_options[appearances[0]][1] = [n]
    print(clue_options)"""

    def try_indexes(clue_options, choice=None, best_choice=None):
        if not choice:
            choice = [10000 + x for x in range(len(clue_options))]
        if not best_choice:
            best_choice = [x for x in choice]
        if len(clue_options) > 0:
            if not clue_options[0][1]:
                clue_options[0][1] = [best_choice[-len(clue_options)]]  # placeholder
            for n in clue_options[0][1]:
                choice[-len(clue_options)] = n
                try_indexes(clue_options[1:], choice, best_choice)
                if len(set(choice)) < len(choice):
                    choice[-len(clue_options)] = 20000 + len(clue_options)
                if len(set(x for x in choice if x < 10000)) > len(set(x for x in best_choice if x < 10000)):
                    for i, x in enumerate(choice):
                        best_choice[i] = x
                    #print(best_choice)
                if all(x < 10000 for x in choice):
                    return choice
        return best_choice

    choice = try_indexes(clue_options)

    indexed_list = []
    for i, c in enumerate(choice):
        if c < 10000:
            clue = clues[c]
            indices = [j+1 for j, x in enumerate(clue) if x == clue_options[i][0]]
            if all_indices:
                index = "/".join(f"{x}" for x in indices)
            else:
                index = random.choice(indices)
            indexed_list.append(f"{clue} ({index})")
        else:
            indexed_list.append(f"(couldn't find a spare {clue_options[i][0]})")

    return indexed_list


if __name__ == "__main__":
    solu = "SUDOKUS"
    lista = ["oro", "huevo", "domingo", "desdeluego", "alpaca", "seguro", "karakolus", "muro", "oliva"]
    for w in index_word_from_wordlist(solu, lista):
        print(w)
