from typing import List, Dict


class WordDict:
    _count = 0

    def __init__(self) -> None:
        self.data: Dict[str, List[str]] = {}
        self.exdata: List[str] = []

        self.load('dict/N5.txt', 'N5')
        self.load('dict/N4.txt', 'N4')
        self.load('dict/N3.txt', 'N3')
        self.load('dict/N2.txt', 'N2')
        self.load('dict/N1.txt', 'N1')
        self.load('dict/EX.txt', 'EX')

    def find(self, text: str) -> List[str]:
        if text in self.data:
            return self.data[text]
        res = self.online_hj(text)
        if res:
            self.exdata.append(res)
            self.add_word(res, 'EX')
            return res
        return []

    def load(self, filename: str, tag: str):
        print('loading dict '+filename)
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                row = line.rstrip().split('\t')
                self.add_word(row, tag)

    def add_word(self, row: List[str], tag: str):
        if row[0] not in self.data:
            self.data[row[0]] = row+[tag]
        if row[1] not in self.data:
            self.data[row[1]] = row+[tag]
        else:
            if row[0] in self.data[row[1]][0]:  # 重复
                return
            v = self.data[row[1]].copy()
            v[0] += '<br>'+row[0]
            v[3] += '<br>'+row[3]
            self.data[row[1]] = v

    def save_exdict(self):
        print('saving exdict')
        with open('dict/EX.txt', 'w', encoding='utf8') as f:
            for data in self.exdata:
                f.write('\t'.join(data))
                f.write('\n')

    def online_hj(self, text: str):
        from lxml import etree
        import requests
        WordDict._count += 1
        if WordDict._count % 10 == 0:
            self.save_exdict()
        try:
            print('searching online: '+text)
            res = requests.get('https://dict.hjenglish.com/jp/jc/'+text, headers={
                'cookie': 'HJ_UID=40e16cb0-69f2-8b35-d09b-4a8627f5cf3b; HJ_SID=s063zt-a49b-40d0-b3dc-e3625b640f9f',
            })
            doc = etree.HTML(res.text)
            header = doc.cssselect('.word-details-pane-header')[0]
            return [
                text,  # 单词
                get_string(header, '.pronounces span', 0)[1:-1],  # 假名
                get_string(header, '.pronounces span', 2),  # 声调
                ' '.join(get_string(header, '.simple h2,li'))  # 释义
            ]
        except Exception as e:
            print(e)
            return []


def get_string(el, css, n=None):
    if n is None:
        return [e.xpath('string()') for e in el.cssselect(css)]
    return el.cssselect(css)[n].xpath('string()')


if __name__ == '__main__':
    wd = WordDict()
    print(wd.find('大きな'))
    print(wd.find('おおきな'))
    # for k, v in wd.data.items():
    #     print(k, v)
