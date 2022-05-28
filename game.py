import pygame
import random
import serial

# Use 2d vectors
vector = pygame.math.Vector2

# Initialize pygame
pygame.init()

# Set the display surface
window_width = 1200
window_height = 736
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("JumpDuino")

# Set fps and clock
fps = 200
clock = pygame.time.Clock()


class Game():
    def __init__(self, player, projectile_group,c):
        # Set constant variables
        self.c=c
        self.starting_projectile_creation_time = 5

        # Set the game values
        self.score = 0
        self.projectile_creation_time = self.starting_projectile_creation_time

        # Set fonts
        self.title_font = pygame.font.SysFont('calibri', 48,bold=True)
        self.HUD_font = pygame.font.SysFont('bahnschrift', 24)
        self.inst_font = pygame.font.SysFont('arial', 32,bold=True)

        # Set sounds
        self.player_hit_sound = pygame.mixer.Sound(
            'Sprites and Assets/player_hit.wav')
        self.player_jump_sound = pygame.mixer.Sound(
            'Sprites and Assets/jump_sound.wav')
        pygame.mixer.music.load(
            'Sprites and Assets/alex-productions-epic-cinematic-gaming-cyberpunk-reset.mp3')

        # Attach groups and sprites
        self.player = player
        self.projectile = projectile_group

    def update(self):
        # Check for gameplay collisions
        self.check_collisions()

        # Add zombies if zombie creation time is met
        self.add_projectile()

        self.check_game_over()
        self.c+=1
        if self.c>=100:
            Projectile(2,5,self.projectile)
            self.c=0

    def draw(self):
        white = (255, 255, 255)
        neonblue = (77, 77, 255)
        black=(0,0,0)

        # Set text
        score_text = self.HUD_font.render('Score: ' + str(self.score), True, white)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 10)

        health_text = self.HUD_font.render('Health: ' + str(self.player.health), True, white)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10, 50)

        title_text = self.title_font.render('JumpDuino', True, neonblue)
        title_rect = title_text.get_rect()
        title_rect.center = (window_width - 125, 25)

        instruction_text=self.inst_font.render('Place hand anywhere between 5 to 10 cm in front of Ultrasonic sensor', True, black)
        instruction_rect = title_text.get_rect()
        instruction_rect.topleft = (150, 268)

        # Draw the HUD
        display_surface.blit(score_text, score_rect)
        display_surface.blit(health_text, health_rect)
        display_surface.blit(title_text, title_rect)
        display_surface.blit(instruction_text, instruction_rect)

    def add_projectile(self):
        pass

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.projectile, True,pygame.sprite.collide_mask):
            self.player_hit_sound.play()
            self.player.health -= 10
            if self.player.health > self.player.starting_health:
                self.player.health = self.player.starting_health
        else:
            self.score += 1

    def check_game_over(self):
        if self.player.health <= 0:
            pygame.mixer.music.stop()
            self.pause_game('Game Over! Final Score: ' + str(self.score), 'Press Enter to play again')
            self.reset_game()

    def pause_game(self, main_text, sub_text):
        global running

        pygame.mixer.music.pause()

        white = (255, 255, 255)
        black = (0, 0, 0)
        green = (25, 200, 25)

        # Create main pause text
        main_text = self.title_font.render(main_text, True, white)
        main_rect = main_text.get_rect()
        main_rect.center = (window_width // 2, window_height // 2)

        sub_text = self.title_font.render(sub_text, True, white)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (window_width // 2, window_height // 2 + 64)

        # Display the pause text
        display_surface.fill(black)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        # Pause the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        pygame.mixer.music.play(-1, 0.0)
                # User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    pygame.mixer.music.stop()

    def reset_game(self):
        self.score = 0

        self.player.health = self.player.starting_health

        self.projectile.empty()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, projectile_group):
        super().__init__()

        # Set constant variables
        self.vertical_acceleration = 0.8  # Gravity
        self.vertical_jump_speed = 15 # Determines how high the player can jump
        self.starting_health = 100

        # Animation frames
        self.move_right_sprites = []
        self.jump_right_sprites = []

        # Moving
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterRunning_0.png'), (75, 75)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterRunning_1.png'), (75, 75)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterRunning_2.png'), (75, 75)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterRunning_3.png'), (75, 75)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterRunning_4.png'), (75, 75)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterRunning_5.png'), (75, 75)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterRunning_6.png'), (75, 75)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterRunning_7.png'), (75, 75)))

        # Jumping
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterJumping_0.png'), (75, 75)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/characterJumping_1.png'), (75, 75)))

        # Load image and get rect
        self.current_sprite = 0
        self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        # Attach sprite groups
        self.projectile_group = projectile_group

        # Animation Boolean
        self.animate_jump = False

        # Load Sounds
        self.jump_sound = pygame.mixer.Sound('Sprites and Assets/jump_sound.wav')
        self.hit_sound = pygame.mixer.Sound('Sprites and Assets/player_hit.wav')

        # Kinematics vectors
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, self.vertical_acceleration)

        # Set initial player values
        self.health = self.starting_health
        self.starting_x = x
        self.starting_y = y

    def update(self):
        self.check_collisions()
        self.check_animations()
        self.animate(self.move_right_sprites, 0.1)
        # Calculate new Kinematics values
        self.acceleration.x -= self.velocity.x * 0
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.bottomleft = self.position

    def check_collisions(self):
        # Collision check between player and platform when falling
        if self.velocity.y > 0:
            if self.position.y > window_height - 10:
                self.position.y = window_height - 10
                self.velocity.y = 0

    def check_animations(self):
        # Animate the player jump
        if self.animate_jump:
            self.animate(self.jump_right_sprites, 0.1)

    def jump(self):
        # Only jump if on a platform
        if self.position.y >= 670:
            self.jump_sound.play()
            self.velocity.y = -1 * self.vertical_jump_speed
            self.animate(self.jump_right_sprites, 0.2)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            # End the jump animation
            if self.animate_jump:
                self.animate_jump = False

        self.image = sprite_list[int(self.current_sprite)]


class Projectile(pygame.sprite.Sprite):
    def __init__(self, min_speed, max_speed,projectile_group):
        super().__init__()

        self.projectile_group=projectile_group

        # Set constant variables
        self.horizontal_acceleration = 0.001

        # Animation frames
        self.shoot_sprites = []

        self.shoot_sprites.append(pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/charged1.png'), (25,25)), True, False))
        self.shoot_sprites.append(pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/charged2.png'), (25,25)), True, False))
        self.shoot_sprites.append(pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/charged3.png'), (25,25)), True, False))
        self.shoot_sprites.append(pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/charged4.png'), (25,25)), True, False))
        self.shoot_sprites.append(pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/charged5.png'), (25,25)), True, False))
        self.shoot_sprites.append(pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('Sprites and Assets/charged6.png'), (25,25)), True, False))

        self.current_sprite = 0

        self.image = self.shoot_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = (window_width + 10, window_height - 30)

        # Load Sounds
        self.hit_sound = pygame.mixer.Sound('Sprites and Assets/Laser Blaster-SoundBible.com-1388608841.mp3')

        # Kinematics vectors
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(-1 * random.randint(min_speed, max_speed), 0)
        self.acceleration = vector(self.horizontal_acceleration, 0)

        projectile_group.add(self)


    def update(self):
        self.move()
        self.check_collisions()

    def move(self):

        self.animate(self.shoot_sprites, 0.5)

        # Calculate new Kinematics values
        self.velocity += -1 * self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # Update rect based on kinematic calculations and add wrap around movement

        self.rect.bottomleft = self.position

        if self.position.x < 0:
            self.kill()



    def check_collisions(self):
        pass

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]

# Background
background_image = pygame.transform.scale(
    pygame.image.load('D:\My_programing_projects\Game_using_Pygame_and_Arduino\Sprites and Assets\city-background.jpg'),
    (1280, 736))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

my_player_group = pygame.sprite.Group()
my_projectile_group = pygame.sprite.Group()


my_player = Player(100, window_height -10, my_projectile_group)
my_player_group.add(my_player)

c=0
my_game = Game(my_player, my_projectile_group,c)
pygame.mixer.music.play(-1, 0.0)


arduinoSerial = serial.Serial('com3', 9600)
co=0
l = 1
running = True
while l == 1:
        if arduinoSerial.inWaiting() > 0:
            myData = arduinoSerial.readline()
            while running:
                co+=1
                if co==25:
                    myData = arduinoSerial.readline()
                    co=0
                # The main game loop
                distance = int(myData)
                print(co,distance)
                # Check to see if the user wants to quit
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        l=0

                    # Check for jumping
                if distance>=25:
                    my_player.jump()

                # Blit the background
                display_surface.blit(background_image, background_rect)

                my_player_group.update()
                my_player_group.draw(display_surface)

                my_projectile_group.update()
                my_projectile_group.draw(display_surface)

                # Update and draw the game
                my_game.update()
                my_game.draw()

                # Update the display and tick the clock
                pygame.display.update()
                clock.tick(fps)
            pygame.quit()
