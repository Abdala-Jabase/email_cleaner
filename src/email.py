from re import S


class Email:

    def __init__(self, f: str, s: str, c: str):
        self.f = f
        self.s = s
        self. c = c

    

    # def cleanBody(self, str) -> str:
    #     greaterThan = 0
    #     curly = 0
    #     s = ''
    #     for i in range(0, len(str)):
    #         if str[i] == '<':
    #             greaterThan += 1
    #             i += 1
    #         elif str[i] == '{':
    #             curly += 1
    #             i += 1
    #         elif str[i] == '}':
    #             curly -= 1
    #             i += 1
    #         elif str[i] == '>':
    #             greaterThan -= 1
    #             i += 1
    #         if curly + greaterThan == 0:
    #             s = s + str[i]
    #     s = " ".join(s.split())
    #     s = re.sub(r"http\S+", "", s)
    #     return s
        
    # def cleanBody(self, str) -> str:
    #     words = [word for word in str.split() if word.isalnum()]

    #     result = ' '.join(words)
    #     return result
