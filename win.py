import pygame

class Winner(pygame.sprite.Sprite):

    def __init__(self, x_0, y_0):
        super().__init__()
        self.sprite = []
        for i in range(1,4):
            self.sprite.append(pygame.image.load('assets/win/win%s.gif'%i))
        self.image = self.sprite[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_0, y_0]
        self.current_image = 0

    def update(self):
        self.image = self.sprite[int(self.current_image)]
        self.current_image += 0.2
        if self.current_image >= len(self.sprite):
            self.current_image = 0 



screen = pygame.display.set_mode((600, 600))

clock = pygame.time.Clock()

win = Winner(100, 200)
grp = pygame.sprite.Group()
grp.add(win)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    grp.draw(screen)
    grp.update()
    pygame.display.update()

    clock.tick(60)