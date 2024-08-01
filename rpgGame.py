import pygame
import random
import button

pygame.init()

clk = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel


screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('RPG Game')

#Defining Game Variables
current_fighter = 1
total_fighter = 3
action_cooldown = 0
action_waitTime = 90
attack = False
potion = False
potion_effect = 15
click = False
game_over = 0 #1 for win -1 for lost

#Defining Fonts
font = pygame.font.SysFont('Times New Roman',26)

#Defining Colors
red = (255,0,0)
green = (0,255,0)

#Images
#Background images
background_img = pygame.image.load('Images/Background/background.png').convert_alpha()
#Panel Image
panel_img = pygame.image.load('Images/Icons/panel.png').convert_alpha()
#Button Image
potion_img = pygame.image.load('Images/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('Images/Icons/restart.png').convert_alpha()
#Sword Image
sword_img = pygame.image.load('Images/Icons/sword.png').convert_alpha()
#Victory/Defeat Images
victory_img = pygame.image.load('Images/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('Images/Icons/defeat.png').convert_alpha()


#Creating function for Text
def draw_text(text,font,text_col,x,y):
    image = font.render(text,True,text_col)
    screen.blit(image,(x,y))

#Function for background images
def background():
    screen.blit(background_img,(0,0))

def panel():
    screen.blit(panel_img,(0,screen_height - bottom_panel)) #Draws panel rectangle
    #Showing Knight Stats
    draw_text(f'{Knight.name} HP: {Knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(Bandit_List):
        #Showing name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10)+ count * 60)

#Game Characters
class Fighter():
    def __init__(self,x,y,name,max_hp,strength,potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0 is Idle, 1 is attack, 2 is hurt, 3 is dead animations. In simple words action is an animation handler
        self.update_time = pygame.time.get_ticks()

        #Loading Idle Images
        temp_list = []
        for i in range(8):
            image = pygame.image.load(f'Images/{self.name}/Idle/{i}.png')
            image = pygame.transform.scale(image,(image.get_width() * 3, image.get_height()*3))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        #Loading Attack Images
        temp_list = []
        for i in range(8):
            image = pygame.image.load(f'Images/{self.name}/Attack/{i}.png')
            image = pygame.transform.scale(image,(image.get_width() * 3, image.get_height()*3))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        #Load Hurt Images
        temp_list = []
        for i in range(3):
            image = pygame.image.load(f'Images/{self.name}/Hurt/{i}.png')
            image = pygame.transform.scale(image,(image.get_width() * 3, image.get_height()*3))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        #Load Death Images
        temp_list = []
        for i in range(10):
            image = pygame.image.load(f'Images/{self.name}/Death/{i}.png')
            image = pygame.transform.scale(image,(image.get_width() * 3, image.get_height()*3))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index] #Handling animation and updating images
        if pygame.time.get_ticks() - self.update_time > animation_cooldown: #Check if enough time has passed
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #If animation has run out, reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
           if self.action == 3:
            self.frame_index = len(self.animation_list[self.action]) - 1
           else:
            self.idle()


    def idle(self):
        #Set Variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self,target):
        #Deal damage to enemy
        no = random.randint(-5,5)
        damage = self.strength + no
        target.hp -= damage
        #Enemy Hurt Animation
        target.hurt()
        #Checking if target had died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #Set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        #Set Variables to Hurt Animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #Set Variables to Death Animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self,x,y,hp,max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self,hp):
        #Update with new health
        self.hp = hp
        #Calculting Health Ratio
        ratio = self.hp/self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150*ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0 

    def update(self):
        #Move Damage Text Up
        self.rect.y -= 1
        #Delete Text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()
        

Knight = Fighter(200,260,'Knight',30, 10, 3)
Bandit1 = Fighter(550,270,'Bandit',20, 6, 1)
Bandit2 = Fighter(700,270,'Bandit',20, 6, 1)
Bandit_List=[]
Bandit_List.append(Bandit1)
Bandit_List.append(Bandit2)

Knight_HealthBar = HealthBar(100, screen_height - bottom_panel + 40, Knight.hp, Knight.max_hp)
Bandit1_HealthBar = HealthBar(550, screen_height - bottom_panel + 40, Bandit1.hp, Bandit1.max_hp)
Bandit2_HealthBar = HealthBar(550, screen_height - bottom_panel + 100, Bandit2.hp, Bandit2.max_hp)

#Creating buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

counter = True
while counter:

    clk.tick(fps)
    background()

    panel()
    Knight_HealthBar.draw(Knight.hp)
    Bandit1_HealthBar.draw(Bandit1.hp)
    Bandit2_HealthBar.draw(Bandit2.hp)

    Knight.update()
    Knight.draw()
    for Bandit in Bandit_List:
        Bandit.update()
        Bandit.draw()

    #Draw Damage Text
    damage_text_group.update()
    damage_text_group.draw(screen)

    #Control Player Actions
    #reset action variables
    attack = False
    potion = False
    target = None
    #Making sure mouse is visible
    pygame.mouse.set_visible(True)
    cursor_position = pygame.mouse.get_pos()
    for count, Bandit in enumerate(Bandit_List):
        if Bandit.rect.collidepoint(cursor_position):
            #Hide Mouse
            pygame.mouse.set_visible(False)
            #Showing sword in place of cursor
            screen.blit(sword_img,cursor_position)
            if clicked == True and Bandit.alive == True:
                attack = True
                target = Bandit_List[count]
    if potion_button.draw():
        potion = True
    #Showing the amount of potions available
    draw_text(str(Knight.potions), font, red, 150, screen_height - bottom_panel + 70)


    if game_over == 0:
        #Player Action
        if Knight.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_waitTime:
                    #Looking for player action
                    #Attack
                    if attack == True and target != None:
                        Knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    #Potion
                    if potion == True:
                        if Knight.potions > 0:
                            #Checking player health first
                            if Knight.max_hp - Knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = Knight.max_hp - Knight.hp
                            Knight.hp += heal_amount
                            Knight.potions -= 1
                            damage_text = DamageText(Knight.rect.centerx, Knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1


        #Enemy Action
        for count, Bandit in enumerate (Bandit_List):
            if current_fighter == 2 + count:
                if Bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_waitTime:
                        #Checking if Bandit needs to heal
                        if (Bandit.hp / Bandit.max_hp) < 0.5 and Bandit.potions > 0:
                            if Bandit.max_hp - Bandit.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = Bandit.max_hp - Bandit.hp
                            Bandit.hp += heal_amount
                            Bandit.potions -= 1
                            damage_text = DamageText(Bandit.rect.centerx, Bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        #attack
                        else:
                            Bandit.attack(Knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1
        #If all fighters have had a turn then reset
        if current_fighter > total_fighter:
            current_fighter = 1

    #Checking if all bandits are dead
    alive_bandits = 0
    for Bandit in Bandit_List:
        if Bandit.alive == True:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1

    #Checking if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250,50))
        if game_over == -1:
            screen.blit(defeat_img, (290,50))
        if restart_button.draw():
            Knight.reset()
            for Bandit in Bandit_List:
                Bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            counter = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
