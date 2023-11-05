import os


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


if __name__ == '__main__':
    unit_template = "    '{unit_id}' : {unit_words},\n"

    unit_id_words = []

    def sort_key(filename):
        # 去掉文件名的扩展名和前缀，然后转换为整数
        return int(filename.replace('Unit', '').replace('.txt', ''))

    root_dir = 'english/9'
    for filename in sorted(os.listdir(root_dir), key=sort_key):
        if not filename.endswith('.txt'):
            continue

        id = filename[4:-4]
        words = read_words(os.path.join(root_dir, filename))
        id_words = unit_template.format(unit_id=id, unit_words=words)
        unit_id_words.append(id_words)

    result_template = "{\n%s}"
    result = result_template % ''.join(unit_id_words)

    with open('english/results/9.txt', 'w') as file:
        file.write(result)
