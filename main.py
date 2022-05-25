from typing import List
import MeCab


def read_srt(filename: str) -> str:
    res = ''
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line == '\n':
                continue
            if '0' <= line[0] <= '9':
                continue
            res += line
    return res


def split_words(text: str) -> List[str]:
    tagger = MeCab.Tagger()
    parsed = tagger.parse(text)
    res = []
    for line in parsed.split('\n'):
        row = line.split('\t')
        if len(row) < 8:
            break
        if '助詞' in row[4] or '助動詞' in row[4] or '感動詞' in row[4] or '記号' in row[4] or '空白' == row[4]:
            continue
        if '-' in row[3]:
            continue
        res.append(row[3])
    return res


def get_gochiusa_cards():
    from WordDict import WordDict
    wordDict = WordDict()
    cards = {}
    for ep in range(1, 13):
        print(f'processing EP{ep}')
        filename = f'subtitle/Gochuumon wa Usagi Desuka_ Bloom (01-12, JP only)/Gochuumon wa Usagi Desuka.S03E{ep:02}.ja.srt'
        text = read_srt(filename).replace('\u3000', ' ')
        for line in text.split('\n'):
            for word in split_words(line):
                if word in cards:
                    if f'E{ep:02}' in cards[word][4]:
                        continue
                    cards[word][4] += f' 点兔S03E{ep:02}'
                    continue
                res = wordDict.find(word)
                if len(res) > 0:
                    cards[word] = res+[line]  # 汉字，假名，声调，翻译，标签，原句
                    cards[word][4] += f' 点兔S03E{ep:02}'
                else:
                    cards[word] = [word, '-', '-', '-', '-', line]
    with open('anki/点兔S03.txt', 'w', encoding='utf-8') as f:
        for word, v in cards.items():
            f.write('\t'.join(v)+'\n')


def get_elaina_cards():
    from WordDict import WordDict
    wordDict = WordDict()
    cards = {}
    for ep in range(1, 13):
        print(f'processing EP{ep}')
        filename = f'subtitle/Wandering Witch_The Journey of Elaina/S01E{ep:02}.ja.srt'
        text = read_srt(filename).replace('\u3000', ' ')
        for line in text.split('\n'):
            for word in split_words(line):
                if word in cards:
                    if f'E{ep:02}' in cards[word][4]:
                        continue
                    cards[word][4] += f' 魔女之旅E{ep:02}'
                    continue
                res = wordDict.find(word)
                if len(res) > 0:
                    cards[word] = res+[line]  # 汉字，假名，声调，翻译，标签，原句
                    cards[word][4] += f' 魔女之旅E{ep:02}'
                else:
                    cards[word] = [word, '-', '-', '-', '-', line]
    with open('anki/魔女之旅.txt', 'w', encoding='utf-8') as f:
        for word, v in cards.items():
            f.write('\t'.join(v)+'\n')


get_gochiusa_cards()
get_elaina_cards()
