def initialize():
    initial = [[[1,1,1,1,1],[1,1,1,1,1]], [0,0], [], ['Player 1','Player 2']]
    return initial

def name(names):
    buffer = input('Player 1\'s name? ')
    if (buffer != ''):
        names[0] = buffer
    buffer = input('Player 2\'s name? ')
    if (buffer != ''):
        names[1] = buffer
    return names

def life(soldiers, team):
    return sum(soldiers[team % 2])

def MT(soldiers, team):
    current_life = life(soldiers, team)
    if (current_life % 5 == 0):
        mean = int(current_life / 5)
        soldiers[team] = [mean for i in range (5)]
    return soldiers

def MA(soldiers, team):
    alive = 0
    for i in range(5):
        if (soldiers[team][i] != 0):
            alive += 1
    current_life = life(soldiers, team)
    if (current_life % alive == 0):
        mean = int(current_life / alive)
        for i in range(5):
            if (soldiers[team][i] != 0):
                soldiers[team][i] = mean
    return soldiers

def attack(soldiers, team, attacker, deffender):
    if (attacker >= 1 and attacker <= 5 and deffender >= 1 and deffender <= 5):
        if (soldiers[(team + 1) % 2][deffender - 1] != 0 and soldiers[team][attacker - 1] != 0):
            soldiers[(team + 1) % 2][deffender - 1] += soldiers[team][attacker - 1]
            soldiers[(team + 1) % 2][deffender - 1] %= 5
    return soldiers

def save(soldiers):
    backup = [[],[]]
    for i in range(2):
        backup[i] += soldiers[i]
    return backup

def register(log, data):
    log += [data]
    return log

def archive(log, names):
    print('\nLog:')
    file = open('modus-five.txt','a')
    file.write('New game:\n')
    file.write('Player 1\'s name: ' + names[0] + '\n')
    file.write('Player 2\'s name: ' + names[1] + '\n')
    for i in range(len(log)):
        print('Turn ' + str(log[i][0]) + ' (player ' + str(log[i][1] + 1) + '\'s turn): ' + str(log[i][2:]))
        file.write('Turn ' + str(log[i][0]) + ' (player ' + str(log[i][1] + 1) + '\'s turn): ' + str(log[i][2:]) + '\n')
    file.write('Game over.\n\n')
    file.close()

def draw(current_turn, log):
    draw_log = {}
    for size in range (1, 1 + int((current_turn + 1) / 6), 1):
        for i in range (0,6,2):
            slicer = slice(current_turn + 1 - size * (i + 2), current_turn - size * i, 2)
            item = log[slicer]
            key = []
            for line in item:
                key += [tuple(tuple(line[2][0])+tuple(line[2][1]))]
            key = tuple(key)
            if key in draw_log:
                draw_log[key] += 1
            else:
                draw_log[key] = 1
            if (draw_log[key] >= 3):
                return 1
    return 0
        
def turn(current_turn, team, soldiers, warnings, log, names):
    print('\nTurn ' + str(current_turn))
    print(names[team] + '\'s time:')
    backup = save(soldiers)
    move = int(input('Your move? '))
    if (move == 0):
        attacker = int(input('Your attacker? '))
        deffender = int(input(names[(team + 1) % 2] + '\'s deffender? '))
        attack(soldiers, team, attacker, deffender)
        move = (move, attacker, deffender)
    elif (move == 1):
        MT(soldiers, team)
    elif (move == 2):
        MA(soldiers, team)
    register(log, (current_turn, team, backup, move, soldiers))
    if (soldiers == backup):
        print(soldiers)
        warnings[team] += 1
        log.pop()
        print('Player ' + str(team + 1) + '\'s warning number [' + str(warnings[team]) + '/3].')
        if (warnings[team] < 3):
            turn(current_turn, team, soldiers, warnings, log, names)
        else:
            register(log, (current_turn, team, backup, 3, soldiers))
            print('\nPlayer ' + str((team + 1) % 2 + 1) + ' won!')
            print('Game over.')
            return log
    elif (life(soldiers, (team + 1) % 2) == 0):
        print('\nPlayer ' + str(team + 1) + ' won!')
        print('Game over.')
        return log
    elif (draw(current_turn, log)):
        print('\nDraw! No one won.')
        print('Game over.')
        return log
    else:
        print(soldiers)
        turn(current_turn + 1, (team + 1) % 2, soldiers, warnings, log, names)
        
def game():
    initial = initialize()
    soldiers = initial[0]
    warnings = initial[1]
    log = initial[2]
    names = initial[3]
    print('Turn 0')
    name(names)
    print(soldiers)
    turn(1, 0, soldiers, warnings, log, names)
    archive(log, names)
    print('\n')
    game()

print('Currently, move 0 is to attack, move 1 is to MT and move 2 is to MA.\nYour soldiers are labeled from 1 to 5.\n') 
game()
