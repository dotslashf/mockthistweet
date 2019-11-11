class Kalimat:
    def __init__(self, kalimat):
        self.kalimat = kalimat

    def transform(self):
        kataJadi = ''
        kalimat = [i for j in self.kalimat.split() for i in (j, ' ')][:-1]
        for kata in kalimat:
            for i, huruf in enumerate(kata):
                if huruf.isupper():
                    huruf = huruf.lower()
                if i % 2 != 0:
                    huruf = huruf.upper()
                kataJadi += huruf
        self.kalimat = kataJadi
        return self.kalimat
