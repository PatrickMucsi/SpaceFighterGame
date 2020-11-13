import pygame
import time
import SpaceFighterTools as SFTools

class WeaponCoolDownBar:
    def __init__(self, position):
        self.position = position
        self.dimensions = (21, 81)
        self.bar = (21, 81)
        self.color = (0, 255, 0)

    def render(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.position, self.dimensions))
        pygame.draw.rect(window, (128, 128, 128), pygame.Rect(self.position, self.bar))

    def update(self, cooldown, cooldown_limit):
        time_passed = time.time() - cooldown
        if time_passed < cooldown_limit:
            self.bar = (21, self.dimensions[1] - ((self.dimensions[1] / cooldown_limit) * time_passed))

class DamageIndicator:
    def __init__(self, damage, position, time):
        self.damage = pygame.font.SysFont('Arial', 20).render(f'-{damage}', False, (255, 0, 0))
        self.position = position
        self.time = time

class HealthBar:
    def __init__(self, health, position, thickness, length):
        self.health = health
        self.current_health = health
        self.bar_thickness = thickness
        self.bar_length = length
        self.position = position

    def update(self, new_health, new_position):
        self.current_health = new_health
        self.position = new_position

    def render(self, window):
        #render total health
        pygame.draw.rect(window, (128, 128, 128), pygame.Rect(self.position, (self.bar_length, self.bar_thickness)))
        #render current health
        pygame.draw.rect(window, (255, 51, 51), pygame.Rect(self.position, (self.current_health * (self.bar_length / self.health), self.bar_thickness)))

class WeaponChoice:
    def __init__(self, type, image, key, position):
        self.type = type
        self.image = image
        self.key = key
        self.is_selected = False
        self.cool_down_remaining = None
        self.choice = pygame.Surface((100, 100))
        self.position = position
        self.small_font = pygame.font.SysFont('Arial', 8)

    def render(self, window, font):
        if self.is_selected:
            self.choice.fill((150, 150, 150))
        else:
            self.choice.fill((230, 230, 230))
        #self.choice.blit(self.image, self.position)
        key_to_select = font.render(f'{self.key}', False, (0,0,0))
        text = font.render(self.type, False, (0,0,0))
        text_loc = text.get_rect(center=self.choice.get_rect().center)
        self.choice.blit(key_to_select, (5,5))
        self.choice.blit(text, (text_loc.x, text_loc.y))
        window.blit(self.choice, self.position)

    def update(self):
        pass


class WeaponSelector:
    def __init__(self, position):
        self.position = position
        self.selector = pygame.Surface((450, 100))
        self.selector_image = SFTools.load_image('assets', 'test-hud-gun-selector.png')
        self.weapon_image = SFTools.load_image('assets', 'test-hud-weapon.png')
        self.weapon_names = ['Basic', 'Super', 'Mega'] #, 'Mega', 'Ultra']
        self.weapon_choices = []
        self.weapon_cooldowns = []
        self.create_weapons()

    def create_weapons(self):
        count = 0
        for name in self.weapon_names:
            pos = ((count * 100) + 5 + (count * 5) , 0) if count == 0 else ((count * 100) + 5 + (count * 35), 0)
            choice = WeaponChoice(name, self.weapon_image, count + 1, pos)
            cooldown = WeaponCoolDownBar((pos[0] + 107, 10))
            self.weapon_choices.append(choice)
            self.weapon_cooldowns.append(cooldown)
            count += 1

    def render(self, window, font):
        self.selector.blit(self.selector_image, (0,0))
        for weapon in self.weapon_choices:
            weapon.render(self.selector, font)
        for cooldown in self.weapon_cooldowns:
            cooldown.render(self.selector)
        window.blit(self.selector, self.position)

    def update(self, selected_weapon, cool_downs, cool_down_limits):
        for weapon in self.weapon_choices:
            if weapon.key == selected_weapon:
                weapon.is_selected = True
            else:
                weapon.is_selected = False
        counter = 0
        for cooldown in self.weapon_cooldowns:
            cooldown.update(cool_downs[counter], cool_down_limits[counter])
            counter += 1

class SpaceFighterHUD:
    def __init__(self, player):
        self.font = pygame.font.SysFont('Arial', 30)
        self.player = player
        self.position = (0, 850)
        self.HUD = pygame.Surface((950, 100))
        self.hud_image = SFTools.load_image('assets', 'test-hud.png')
        self.health_bar = HealthBar(self.player.health, (5, 40), 25, 150)
        self.weapon_selector = WeaponSelector((200, 0))

    def render(self, window):
        #self.HUD.fill((0, 0, 0))
        self.HUD.blit(self.hud_image, (0, 0))
        self.health_bar.render(self.HUD)
        self.weapon_selector.render(self.HUD, self.font)
        self.HUD.blit(self.font.render('Health: {}%'.format(self.health_bar.current_health), False, (0, 0, 0)), (5, 5))
        window.blit(self.HUD, self.position)

    def update(self):
        self.health_bar.update(self.player.health, self.health_bar.position)
        self.weapon_selector.update(self.player.current_weapon, self.player.cool_downs, self.player.cool_down_amounts)
