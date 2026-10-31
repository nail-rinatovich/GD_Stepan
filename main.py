import pygame
import sys
from states import MainMenuState
from database import DatabaseManager

class StateManager:
    """Контроллер, который управляет текущим экраном игры и хранит общие ресурсы."""
    def __init__(self):
        self.current_state = None
        # Инициализируем базу данных прямо внутри менеджера состояний
        self.db = DatabaseManager()

    def change_to(self, new_state_class):
        """Метод для смены экрана."""
        self.current_state = new_state_class(self)


def main():
    pygame.init()
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Geometry Dash Clone")
    
    clock = pygame.time.Clock()
    manager = StateManager()
    
    # Задаем стартовое состояние — Главное меню
    manager.change_to(MainMenuState)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0 
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if manager.current_state:
            manager.current_state.handle_events(events)
            manager.current_state.update(dt)
            manager.current_state.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
