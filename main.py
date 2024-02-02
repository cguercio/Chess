from graphics import gui

WIDTH, HEIGHT = 800, 800

def main():
    running = True

    while running:

        screen = gui.Screen(WIDTH, HEIGHT)
        screen.display()

        for event in gui.pygame.event.get():
            if event.type == gui.pygame.QUIT:
                running = False
                break

if __name__ == '__main__':
    main()