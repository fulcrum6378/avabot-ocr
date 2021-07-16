class RGB(tuple):
    def __new__(cls, r: int, g: int, b: int):
        if r > 255 or g > 255 or b > 255:
            raise Exception("RGB maximum number is 255!")
        if r < 0 or g < 0 or b < 0:
            raise Exception("RGB minimum number is 0!")
        return tuple.__new__(RGB, (r, g, b))

    @staticmethod
    def isRGB(tup: tuple):
        return False not in [
            len(tup) == 3,
            0 <= tup[0] < 256,
            0 <= tup[1] < 256,
            0 <= tup[2] < 256,
        ]

    def compare(self, another: tuple) -> int:
        if not RGB.isRGB(another):
            raise Exception("Please enter a valid RGB value!")
        dif = 100
        dif -= (100 / 255) * abs(self[0] - another[0]) / 3
        dif -= (100 / 255) * abs(self[1] - another[1]) / 3
        dif -= (100 / 255) * abs(self[2] - another[2]) / 3
        return dif

    def knn(self, others: list):
        if len(others) == 0: return None
        dif = list()
        for o in others:
            dif.append(self.compare(o))
        mx = 0
        for d in range(len(dif)):
            if dif[d] > mx: mx = d
        return mx
