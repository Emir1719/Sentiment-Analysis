class StopWords:
    def __init__(self):
        self.turkishWords: list[str] = self.__generateTurkishWords()

    def __generateTurkishWords(self) -> list[str]:
        return [
            "as", "sa", "bir", "ı", "a", "e", "i", "ki", "kı", "tü", "tu", "bi", "di", "şey", "de", "da",
            "bugun", "bugün", "selamun", "aleyküm", "selamunaleyküm", "bizi", "bize", "yüz", "tür"
            "dk", "cc", "c.c.", "c.c", "as", "sav", "s.a.v", "ra", "r.a.", "her", "herşey", "ile", "ya da",
            "biri", "hep", "biz", "sen", "onlar", "aslında", "ama", "fakat", "selam", "naber", "hoca",
            "birkaç", "bu", "şu", "bunlar", "şunlar", "dı", "defa", "daha", "diye", "lar", "ler",
            "eğer", "eger", "gibi", "der", "tüm", "tümü", "ve", "veya", "ya", "abi", "ağabey", "kardeş",
            "göre", "üzere", "sonra", "önce", "kadar", "bazı", "diğer", "herkes", "be", "rağmen", "bin", 
            "olan", "hz", "m", "n", "deki", "daki", "ta", "te", "taki", "bır", "birşey", "bırsey", "bişey"
        ]