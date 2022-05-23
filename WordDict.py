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
        pass

    def load(self, filename: str, tag: str):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                row = line.rstrip().split('\t')
                if row[0] not in self.data:
                    self.data[row[0]] = row+[tag]


if __name__ == '__main__':
    wd = WordDict()
    # print(wd.find('あいうえお'))
    for k, v in wd.data.items():
        print(k, v)
