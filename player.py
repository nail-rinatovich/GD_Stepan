import pygame

class Player(pygame.sprite.Sprite):
    """Класс игрока-кубика с анимацией вращения."""
    def __init__(self, x, y):
        super().__init__()
        self.size = 40
        # Базовая поверхность кубика
        self.base_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.base_image.fill((0, 255, 100))
        # Внутренняя рамка
        pygame.draw.rect(self.base_image, (0, 150, 50), (5, 5, 30, 30), 3)
        
        # ВАЖНО: Создаем маску для точных коллизий
        self.mask = pygame.mask.from_surface(self.base_image)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        # Логическая рамка всегда остается квадратом; визуальная поверхность
        # вращается отдельно, чтобы поворот не менял физику столкновений.
        self.draw_rect = self.rect.copy()
        
        self.velocity_y = 0
        self.gravity = 1600
        self.jump_force = -580
        self.is_on_ground = True
        self.floor_y = 500
        
        # Параметры вращения
        self.angle = 0  # Начинаем с 0 градусов (кубик ровно стоит)
        self.rotation_speed = 360 
        
        # Для отслеживания предыдущей позиции (нужно для коллизий с блоками)
        self.prev_rect = self.rect.copy()
        self.prev_bottom = self.rect.bottom
        self.dead = False

    def jump(self):
        if self.is_on_ground:
            self.velocity_y = self.jump_force
            self.is_on_ground = False

    def die(self):
        """Метод смерти игрока."""
        self.dead = True

    def update(self, dt):
        # Сохраняем предыдущую позицию для определения стороны коллизии
        self.prev_rect = self.rect.copy()
        self.prev_bottom = self.rect.bottom
        
        if not self.is_on_ground:
            self.velocity_y += self.gravity * dt
            self.angle = (self.angle - self.rotation_speed * dt) % 360
        else:
            # Округляем угол до ближайших 90 градусов, когда на земле
            self.angle = round(self.angle / 90) * 90 % 360
        
        self.rect.y = round(self.rect.y + self.velocity_y * dt)
        
        # Проверка пола
        if self.rect.bottom >= self.floor_y:
            self.rect.bottom = self.floor_y
            self.velocity_y = 0
            self.is_on_ground = True
        
        self.rotate_sprite()

    def check_block_collisions(self, blocks):
        """
        Проверяет коллизии игрока со списком блоков.
        Возвращает True, если игрок умер (врезался сбоку).
        """
        # Повторно проверяем опору каждый кадр.
        self.is_on_ground = False
        
        # Сначала проверяем пол
        if self.rect.bottom >= self.floor_y:
            self.rect.bottom = self.floor_y
            self.velocity_y = 0
            self.is_on_ground = True
        
        # Теперь проверяем все блоки
        for block in sorted(blocks, key=lambda item: item.rect.top):
            if not self.rect.colliderect(block.rect):
                continue

            horizontal_overlap = self.rect.right > block.rect.left and self.rect.left < block.rect.right
            crossed_top = self.prev_rect.bottom <= block.rect.top and self.rect.bottom >= block.rect.top
            crossed_bottom = self.prev_rect.top >= block.rect.bottom and self.rect.top <= block.rect.bottom

            # Любое падение через верхнюю грань — приземление, даже если
            # за кадр кубик успел глубоко войти в блок.
            if horizontal_overlap and self.velocity_y >= 0 and crossed_top:
                self.rect.bottom = block.rect.top
                self.velocity_y = 0
                self.is_on_ground = True
                continue

            # При подъеме упираемся головой в нижнюю грань.
            if horizontal_overlap and self.velocity_y < 0 and crossed_bottom:
                self.rect.top = block.rect.bottom
                self.velocity_y = 0
                continue

            # Контакт сбоку смертелен; касание сверху/снизу не считается боком.
            if not crossed_top and not crossed_bottom:
                self.die()
                return True
        
        return False

    def rotate_sprite(self):
        """Поворачивает изображение, не меняя физическую рамку игрока."""
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.draw_rect = self.image.get_rect(center=self.rect.center)
