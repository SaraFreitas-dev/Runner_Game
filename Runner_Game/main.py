import pygame
from sys import exit
from random import randint, choice

pygame.init()

# Window the player will see
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner Game")  # Display Title

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly_frame1 = pygame.image.load("Runner_Game/graphics/fly/fly1.png").convert_alpha()
            fly_frame2 = pygame.image.load("Runner_Game/graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load("Runner_Game/graphics/snail/snail1.png").convert_alpha()
            snail_frame2 = pygame.image.load("Runner_Game/graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        if self.rect.x <= -100:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_index = 0
        self.gravity = 0
        player_walk1 = pygame.image.load("Runner_Game/graphics/Player/player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("Runner_Game/graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_jump = pygame.image.load("Runner_Game/graphics/Player/jump.png").convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))

        self.jump_sound = pygame.mixer.Sound("Runner_Game/audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -23
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def draw_menu(score):
    screen.fill((94, 129, 162))

    # Draw Score above the logo
    if score > 0:
        score_surface = test_font.render(f"Score: {score}", False, (111, 196, 169))
        score_rect = score_surface.get_rect(center=(400, 75))
        screen.blit(score_surface, score_rect)

    # Draw Logo
    screen.blit(player_logo, player_logo_rect)

    # Draw Game Over Title
    screen.blit(gameOver_surface, gameOver_rect)

    # Draw Play Again Button
    pygame.draw.rect(screen, "#A9A9A9", playAgain_bg_rect, border_radius=10)
    pygame.draw.rect(screen, "#000000", playAgain_bg_rect, width=3, border_radius=10)
    screen.blit(playAgain_button, playAgain_text_rect)

    # Draw Exit Button
    pygame.draw.rect(screen, "#A9A9A9", exit_bg_rect, border_radius=10)
    pygame.draw.rect(screen, "#000000", exit_bg_rect, width=3, border_radius=10)
    screen.blit(exit_button, exit_text_rect)

game_active = True
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

clock = pygame.time.Clock()  # Control frame rate
test_font = pygame.font.Font("Runner_Game/font/Pixeltype.ttf", 50)

bg_music = pygame.mixer.Sound("Runner_Game/audio/music.wav")
bg_music.set_volume(0.7)
bg_music.play(loops=-1)

# Graphics BG
sky_bg = pygame.image.load("Runner_Game/graphics/Sky.png")
ground_bg = pygame.image.load("Runner_Game/graphics/ground.png")

# Change Title
gameOver_surface = test_font.render("Game Over", False, (111, 196, 169))
gameOver_rect = gameOver_surface.get_rect(center=(400, 40))

# Logo Intro Screen
player_logo = pygame.image.load("Runner_Game/graphics/Player/player_walk_1.png").convert_alpha()
player_logo = pygame.transform.scale(player_logo, (140, 160))
player_logo_rect = player_logo.get_rect(center=(400, 185))

# Buttons Game Over
playAgain_button = test_font.render("Play Again", False, ("#000000"))
exit_button = test_font.render("Exit", False, ("#000000"))

# Play Again Button
playAgain_bg_rect = pygame.Rect(0, 0, 200, 70)
playAgain_bg_rect.center = (280, 320)
playAgain_text_rect = playAgain_button.get_rect(center=playAgain_bg_rect.center)

# Exit Button
exit_bg_rect = pygame.Rect(0, 0, 200, 70)
exit_bg_rect.center = (520, 320)
exit_text_rect = exit_button.get_rect(center=exit_bg_rect.center)

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 400)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

    if game_active:
        screen.blit(sky_bg, (0, 0))  # x, y positions
        screen.blit(ground_bg, (0, 300))
        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision detection
        game_active = collision_sprite()

    else:
        draw_menu(score)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if playAgain_bg_rect.collidepoint(pos):
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                score = 0
            if exit_bg_rect.collidepoint(pos):
                pygame.quit()
                exit()

    pygame.display.update()
    clock.tick(60)  # the max velocity of the loop so it doesn't run too fast
