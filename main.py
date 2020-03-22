from logic.game import Person, bcolors
from logic.magic import Spell
from logic.inventory import Item
import random

fire = Spell('Fire', 15, 600, 'black')
thunder = Spell('Thunder', 16, 590, 'black')
blizzard = Spell('Blizzard', 18, 750, 'black')
meteor = Spell('Meteor', 24, 1000, 'black')
quake = Spell('Quake', 19, 800, 'black')

cure = Spell('Cure', 15, 700, 'white')
cura = Spell('Cura', 22, 1500, 'white')
curaga = Spell('Curaga', 50, 6000, 'white')


potion = Item('Potion', 'potion', 'Heal 250 HP', 250)
hipotion = Item('Hi-Potion', 'potion', 'Heal 1000 HP', 1000)
superpotion = Item('Super Potion', 'potion', 'Heal 2000 HP', 2000)
elixer = Item('Elixer', 'elixer', 'Fully restores HP/MP of one party member', 9999)
hielixer = Item('MegaElixer', 'elixer', "Fully restores party's HP/MP", 9999)
grenade = Item('Grenade', 'attack', 'Deals 2000 damage', 2000)

player_mag = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_warrior = [quake, cure]
player_engineer = [fire, thunder, blizzard, cure, cura]
player_item_mag = [{'item': potion, 'quantity': 15},
               {'item': hipotion, 'quantity': 5},
               {'item': superpotion, 'quantity': 5}]
player_item_warrior = [{'item': potion, 'quantity': 10},
               {'item': hipotion, 'quantity': 5},
               {'item': elixer, 'quantity': 5}]
player_item_engineer = [{'item': potion, 'quantity': 10},
               {'item': hipotion, 'quantity': 3},
               {'item': hielixer, 'quantity': 2},
               {'item': grenade, 'quantity': 3}]


player1 = Person('Diego ', 4160, 50, 320, 50, player_warrior, player_item_warrior)
player2 = Person('Xartas', 2700, 200, 205, 25, player_mag, player_item_mag)
player3 = Person('Thorn ', 3175, 110, 250, 34, player_engineer, player_item_engineer)

enemy1 = Person('Imp  ', 1250, 24, 560, 325, [fire, cure], [])
enemy2 = Person('Magus', 18200, 50, 475, 25, [meteor, curaga], [])
enemy3 = Person('Imp  ', 1250, 24, 560, 325, [fire, cure], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

while running:
    print('==================================================================================')
    print('Name:                    HP                                          MP')
    for player in players:
        player.get_stats()

    print()
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input('Choose action: ')
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print('You attacked', enemies[enemy].name, 'for', dmg, 'points of damage.')

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name, 'has died')
                del enemies[enemy]
        elif index == 1:
            player.choose_spell()
            magic_choice = int(input('Choose spell: ')) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL, '\nNot enough MP\n' + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE, '\n', spell.name, 'heals for', str(magic_dmg), 'HP', bcolors.ENDC)
            elif spell.type == 'black':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE, '\n', spell.name, 'deals', str(magic_dmg), 'points of damage to',
                      enemies[enemy].name, bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name, 'has died')
                    del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input('Choose item: ')) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]['item']
            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL, '\n', 'None left...', bcolors.ENDC)
                continue
            player.items[item_choice]['quantity'] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN, '\n', item.name, 'heals for', str(item.prop), 'HP', bcolors.ENDC)
            elif item.type == 'elixer':
                if item.name == 'MegaElixer':
                    for party_member in players:
                        party_member.hp = party_member.maxhp
                        party_member.mp = party_member.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN, '\n', item.name, 'fully restores HP/MP', bcolors.ENDC)
            elif item.type == 'attack':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL, '\n', item.name, 'deals', str(item.prop), 'points of damage to',
                      enemies[enemy].name, bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name, 'has died')
                del enemies[enemy]
        else:
            continue

    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN, 'You win!', bcolors.ENDC)
        running = False

    print()

    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0 or enemy.mp < 15:
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name, 'attack', players[target].name, 'for', enemy_dmg, 'points of damage.')

            if players[target].get_hp() == 0:
                print(players[target].name, 'has died')
                del players[target]
                if len(players) == 0:
                    print(bcolors.FAIL, 'Your enemies have defeated you!', bcolors.ENDC)
                    running = False

        elif enemy_choice == 1 and enemy.mp > 15:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE, spell.name, 'heals', enemy.name, 'for', str(magic_dmg), 'HP', bcolors.ENDC)
            elif spell.type == 'black':
                target = random.randrange(0, len(players))
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE, '\n', enemy.name, spell.name, 'deals', str(magic_dmg), 'points of damage to',
                      players[target].name, bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name, 'has died')
                    del players[target]
                    if len(players) == 0:
                        print(bcolors.FAIL, 'Your enemies have defeated you!', bcolors.ENDC)
                        running = False
