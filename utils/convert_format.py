def read_words(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    words = []
    word = []
    for line in lines:
        line = line.strip()

        if len(line) == 0:
            continue

        if line.startswith('['):
            continue

        word.append(line)

        if len(word) == 2:
            words.append(tuple(word))
            word = []

    return words

words = read_words('english/9/Unit14.txt')
print(words)