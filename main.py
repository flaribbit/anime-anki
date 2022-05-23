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


text = read_srt('subtitle/Gochuumon wa Usagi Desuka_ Bloom (01-12, JP only)/Gochuumon wa Usagi Desuka.S03E01.ja.srt')
for line in text.split('\n'):
    print(split_words(line))
