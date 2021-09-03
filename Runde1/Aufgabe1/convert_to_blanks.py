import random

def make_blank(word):
    l = random.randint(0, len(word)-1)
    new_word = list("_"*len(word))
    new_word[l] = word[l]
    return "".join(new_word)

file = "Beispiele/test5.txt"

with open(file, "r", encoding="utf8") as f:
    l = "".join(f.readlines()).split()

words, blanks = [], []
for word in l:
    if any([i in ["!", ".", ",", "?"] for i in word]):
        word, extra = word[:-1], word[-1]
        words.append(word)
        blanks.append(make_blank(word)+extra)
    else:
        words.append(word)
        blanks.append(make_blank(word))

print(words)
print(blanks)

with open(file, "w", encoding="utf8") as f:
    f.write(" ".join(blanks) + "\n")
    f.write(" ".join(words))

