import pgzrun
import random
import math
import sys

from pygame.mixer import music

WIDTH = 800
HEIGHT = 600
score = 0
game_music_playing = True

class AnimatedActor:
    def __init__(self, images, x, y, animation_speed=5):
        self.images = images
        self.image_index = 0
        self.actor = Actor(self.images[self.image_index])
        self.actor.x = x
        self.actor.y = y
        self.animation_speed = animation_speed
        self.animation_timer = 0

    def draw(self):
        self.actor.draw()

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= 60 / self.animation_speed:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.actor.image = self.images[self.image_index]
            self.animation_timer = 0

class Player(AnimatedActor):
    def __init__(self, x, y):
        images = ["hero_1.png", "hero_2.png"]
        super().__init__(images, x, y)

    def update(self):
        global score
        if keyboard.right and self.actor.x < WIDTH - self.actor.width:
            self.actor.x += 5
        elif keyboard.left and self.actor.x > 0:
            self.actor.x -= 5
        elif keyboard.down and self.actor.y < HEIGHT - self.actor.height:
            self.actor.y += 5
        elif keyboard.up and self.actor.y > 0:
            self.actor.y -= 5
        self.animate()
        score += 1

class Enemy(AnimatedActor):
    def __init__(self, x, y):
        images = ["enemy_1.png", "enemy_2.png"]
        super().__init__(images, x, y)
        self.direction = random.uniform(0, math.pi * 2)

    def update(self):
        self.move()
        self.animate()

    def move(self):
        speed = 2
        self.actor.x += speed * math.cos(self.direction)
        self.actor.y += speed * math.sin(self.direction)

        if self.actor.x < 0 or self.actor.x > WIDTH - self.actor.width or \
           self.actor.y < 0 or self.actor.y > HEIGHT - self.actor.height:
            self.direction = random.uniform(0, math.pi * 2)

class MusicPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.playing = False

    def play(self):
        if not self.playing:
            music.load(self.filename)
            music.play(-1)
            self.playing = True

    def stop(self):
        if self.playing:
            music.stop()
            self.playing = False

class Menu:
    def __init__(self):
        self.selected_option = 0
        self.options = ["Start Game", "Toggle Music", "Exit"]
        self.music_menu = MusicPlayer("sounds/menu.mp3")
        self.music_menu.play()
        self.music_game = MusicPlayer("sounds/sound.mp3")
        self.music_game.play()

    def draw(self):
        screen.clear()
        screen.draw.text("Main Menu", (WIDTH/2, 100), fontsize=60, color="white", center=(WIDTH/2, 100))
        for i, option in enumerate(self.options):
            color = "yellow" if i == self.selected_option else "white"
            screen.draw.text(option, (WIDTH/2, 200 + i * 50), fontsize=40, color=color, center=(WIDTH/2, 200 + i * 50))

    def update(self):
        pass

    def select_option(self):
        if self.selected_option == 0:
            start_game()
        elif self.selected_option == 1:
            toggle_music()
        elif self.selected_option == 2:
            reset_game()
            exit()

def reset_game():
    global enemies
    enemies = []
    global score
    score = 0

def start_game():
    global in_menu, game_music_playing
    in_menu = False
    game_music_playing = True
    if menu.music_menu.playing:
        menu.music_menu.stop()
        game_music.play()
    else:
        game_music_playing = False
    clock.schedule_interval(spawn_enemy, 5)


def toggle_music():
    global game_music_playing
    if in_menu:
        if menu.music_menu.playing:
            menu.music_menu.stop()
            if not menu.music_menu.playing and game_music_playing:
                game_music.stop()
                game_music_playing = False
        else:
            menu.music_menu.play()
            if not menu.music_menu.playing and not game_music_playing:
                game_music.stop()
                game_music_playing = False
    else:
        if game_music_playing:
            game_music.stop()
            game_music_playing = False
        else:
            game_music.play()
            game_music_playing = True


def exit():
    sys.exit()

def on_key_down(key):
    global in_menu, game_music_playing
    if in_menu:
        if key == keys.DOWN:
            menu.selected_option = (menu.selected_option + 1) % len(menu.options)
        elif key == keys.UP:
            menu.selected_option = (menu.selected_option - 1) % len(menu.options)
        elif key == keys.RETURN:
            menu.select_option()
    elif key == keys.ESCAPE:
        in_menu = True
        game_music.stop()
        menu.music_game.stop()
        menu.music_menu.play()

def draw():
    if in_menu:
        menu.draw()
    else:
        screen.clear()
        screen.blit("background.png", (0, 0))
        player.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text("Score: " + str(score), (10, 10), fontsize=30, color="white")

def update():
    global in_menu, game_music_playing
    if in_menu:
        menu.update()
        if not menu.music_menu.playing and game_music.playing:
            game_music.stop()
            game_music_playing = False
    else:
        player.update()
        for enemy in enemies:
            enemy.update()
        for enemy in enemies:
            if player.actor.colliderect(enemy.actor):
                reset_game()
                in_menu = True
                game_music.stop()
                menu.music_game.stop()
                menu.music_menu.play()

def spawn_enemy():
    enemy = Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    enemies.append(enemy)

player = Player(WIDTH // 2, HEIGHT // 2)
menu = Menu()
in_menu = True
enemies = []
game_music = MusicPlayer("sounds/sound.mp3")

pgzrun.go()
