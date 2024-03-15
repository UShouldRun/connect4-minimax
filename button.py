from pygame import draw, font, Rect

class Button:
    def __init__(self, screen, x: int, y: int, width, height: int, color: tuple[int, int, int], text: str, _font: str, fontSize: int, textColor: tuple[int, int, int]):
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.text = text 
        self.font = font.SysFont(_font, fontSize)
        self.textColor = textColor
        self.clicked = False

    def getSurface(self): return self.font.render(self.text, True, self.textColor)
    def getRect(self): return Rect(self.x, self.y, self.width, self.height)
    def getClicked(self): return self.clicked

    def setClicked(self, state: bool): self.clicked = state

    def draw(self):
        draw.rect(self.screen, self.color, self.getRect()) 
        self.screen.blit(self.getSurface(), (self.x + self.width//2 - self.getSurface().get_width()//2, self.y + self.height//2 - self.getSurface().get_height()//2))
