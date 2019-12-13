from typing import List

class Tenji(object):

    t_table = ' ⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿'
    kana = [
        'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもらりるれろ',
        '　　　　　がぎぐげござじずぜぞだぢづでど　　　　　ばびぶべぼ',
        '　　　　　　　　　　　　　　　　　　　　　　　　　ぱぴぷぺぽ',
        'ゃ　ゅ　ょ',
        'やゆよわをっーん',
        '、。？！・'
    ]
    dan = [
        '100000', # a, ⠁
        '110000', # i, ⠃
        '100100', # u, ⠉
        '110100', # e, ⠋
        '010100'  # o, ⠊
    ]
    gyo = [
        '000000', # a, x
        '000001', # k, ⠠
        '000011', # s, ⠰
        '001010', # t, ⠔
        '001000', # n, ⠄
        '001001', # h, ⠤
        '001011', # m, ⠴
        '000010'  # r, ⠐
    ]
    special = [
        '001100',
        '001101',
        '001110',
        '001000',
        '001010',
        '010000',
        '010010',
        '001011'
    ]
    symbol = [
        ['000011', '000000'],
        ['010011', '000000', '000000'],
        ['010001'],
        ['011010'],
        ['000010', '000000']
    ]

    @staticmethod
    def xor(s1: str, s2:str) -> str:
        result = ''
        for i in range(6):
            result += str(int(s1[i]) ^ int(s2[i]))
        return result

    @staticmethod
    def code_to_tenji(code: str) -> str:
        '''Translate six-digit code to tenji.

        For example, '010101' to '⠪':
        1 4    0 1
        2 5 -> 1 0 -> ⠪
        3 6    0 1
        '''

        index = 0
        for i, c in enumerate(code):
            index += 2 ** i * int(c)
        return Tenji.t_table[index]

    @staticmethod
    def kana_string_to_codes(kanas: str) -> List[str]:
        codes = []
        for i, k in enumerate(kanas):
            if k == '　' or k == ' ':
                codes.append('000000')
            elif k in Tenji.kana[0]:
                index = Tenji.kana[0].find(k)
                code = Tenji.xor(Tenji.dan[index % 5], Tenji.gyo[index // 5])
                codes.append(code)
            elif k in Tenji.kana[1]:
                index = Tenji.kana[1].find(k)
                codes.append('000010')
                code = Tenji.xor(Tenji.dan[index % 5], Tenji.gyo[index // 5])
                codes.append(code)
            elif k in Tenji.kana[2]:
                index = Tenji.kana[2].find(k)
                codes.append('000001')
                code = Tenji.xor(Tenji.dan[index % 5], Tenji.gyo[index // 5])
                codes.append(code)
            elif k in Tenji.kana[3]:
                index = Tenji.kana[3].find(k)
                g = '00' + codes[-1][2] + '0' + codes[-1][4:6]
                codes[-1] = Tenji.xor(g, Tenji.dan[index])
                if kanas[i - 1] in Tenji.kana[0]:
                    codes.insert(-1, '000000')
                codes[-2] = Tenji.xor(codes[-2], '000100')
            elif k in Tenji.kana[4]:
                index = Tenji.kana[4].find(k)
                codes.append(Tenji.special[index])
            else:
                index = Tenji.kana[5].find(k)
                codes += Tenji.symbol[index]

        return codes

    @staticmethod
    def kana_string_to_tenji(kanas: str) -> str:
        codes = Tenji.kana_string_to_codes(kanas)
        result = ''
        for c in codes:
            result += Tenji.code_to_tenji(c)
        return result

if __name__ == '__main__':
    print(Tenji.kana_string_to_tenji('かなを　てんじに　へんかん　できる　つーる　です。'))
