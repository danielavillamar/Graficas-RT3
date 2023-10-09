import Lights.Light as Light


class Ambient(Light.Light):
    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "AMBIENT")
