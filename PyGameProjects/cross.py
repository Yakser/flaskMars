import pygame

if __name__ == '__main__':
    # try:
        n = int(input())
        if n <= 0:
            raise Exception
        size = width, height = 300, 300
        pygame.init()
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Ромбики")

        w, h = width, height
        x, y = 0, 0
        rect = pygame.rect.Rect(0, 0, n, n)

        rect = pygame.draw.rect(screen, pygame.color.Color("orange"), pygame.rect.Rect(0, 0, n, n))


        # for i in range(0, height, n):
        #     for j in range(0, width, n):
        #         pygame.draw.rect(screen, pygame.color.Color("orange"), (i, j, n, n))

        while pygame.event.wait().type != pygame.QUIT:
            pygame.display.flip()
        pygame.quit()
    # except:
    #     print("Неправильный формат ввода")
