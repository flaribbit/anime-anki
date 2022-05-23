from typing import List, Dict


class WordDict:
    def __init__(self) -> None:
        self.data: Dict[str, List[str]] = {}

        self.load('dict/N5.txt', 'N5')
        self.load('dict/N4.txt', 'N4')
        self.load('dict/N3.txt', 'N3')
        self.load('dict/N2.txt', 'N2')
        self.load('dict/N1.txt', 'N1')

    def find(self, text: str) -> List[str]:
        if text in self.data:
            return self.data[text]
        return []

    def load(self, filename: str, tag: str):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                row = line.rstrip().split('\t')
                if row[0] not in self.data:
                    self.data[row[0]] = row+[tag]
                if row[1] not in self.data:
                    self.data[row[1]] = row+[tag]
                else:
                    if row[0] in self.data[row[1]][0]:  # 重复
                        continue
                    v = self.data[row[1]].copy()
                    v[0] += '<br>'+row[0]
                    v[3] += '<br>'+row[3]
                    self.data[row[1]] = v


if __name__ == '__main__':
    wd = WordDict()
    print(wd.find('大きな'))
    print(wd.find('おおきな'))
    # for k, v in wd.data.items():
    #     print(k, v)
