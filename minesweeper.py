#todo: generate mines after first click

from random import randrange
size = 10#int(raw_input("Enter board size PLS: "))
num_mines = 10#int(raw_input("Enter number of mines PLS: "))
mines = []
for i in range(num_mines):
  diff = False
  while not diff:
    mine = (randrange(0, size), randrange(0, size))
    diff = not (mine in mines)
  mines.append(mine)
board_internal = [[0 for j in range(size)] for i in range(size)]
for mine in mines:
  for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
      x = mine[0]+i
      y = mine[1]+j
      if 0 <= x < size and 0 <= y < size and board_internal[x][y] < 9:
        board_internal[x][y] += 1
  board_internal[mine[0]][mine[1]] = 9
for mine in mines:
  print mine
#board_shown = [[str(board_internal[i][j]) for j in range(size)] for i in range(size)]
board_shown = [['#' for j in range(size)] for i in range(size)]
#print board_shown
def print_board(board):
  print ' ',
  for i in range(size):
    print i,
  print ''
  for i in range(size):
    print i,
    for j in range(size):
      print board[i][j],
    print ''

lost = False
print 'im here'

# design: functions refer to outside variables or take them all in? i'm doing a bit of both right now, seems like bad design

# # - none
# f - flagged
# s - scavenged
board_status = [['#' for j in range(size)] for i in range(size)]

#uses board_internal and board_shown
def show(x, y):
  '''pre: (x, y) is valid coordinate'''
  val = board_internal[x][y]
  board_shown[x][y] = str(val) if val != 0 else '-'

def scavenge_init(x, y):
  '''pre: (x, y) is valid coordinate'''
  if board_status[x][y] == 's':
    return # try again punk
  if (x, y) in mines:
    board_shown[x][y] = 'X'
    print 'hey!'
    global lost #wtfffwtwwfjktwjfwfwtwf
    lost = True
    print lost
    print 'o!'
    return
  board_status[x][y] = 's'
  show(x, y)
  for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
      #if not (i == j == 0): #don't need because already have scavenged check
      scavenge(x+i, y+j)

def scavenge(x, y):
  if not (0 <= x < size and 0 <= y < size):
    return
  if (x, y) in mines:
    return
  if board_status[x][y] == 's':
    return # try again punk
  board_status[x][y] = 's'
  show(x, y)
  if board_internal[x][y] != 0:
    return
  for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
      #if not (i == j == 0):
      scavenge(x+i, y+j)

def flag2(x, y):
  cur = board_status[x][y]
  if cur == 's':
    return # cannot flag this
  if cur == '#':
    board_status[x][y] = 'f'
    board_shown[x][y] = 'F'
  else: # already flagged
    board_status[x][y] = '#'
    board_shown[x][y] = '#'
  
def flag(x, y):
  if board_status[x][y] != '#':
    return
  board_status[x][y] = 'f'
  board_shown[x][y] = 'F'

def unflag(x, y):
  if board_status[x][y] != 'f':
    return
  board_status[x][y] = '#'
  board_shown[x][y] = '#'

def check_win():
  for i in range(size):
    for j in range(size):
      if (i, j) not in mines and board_shown[i][j] == '#':
        return False
  return True

commands = {'click': scavenge_init, 'flag': flag, 'unflag': unflag}

while not lost:
  #do actual checking of validity later
  #guess = raw_input('Enter a coordinate: ').split(' ')
  raw = raw_input('Enter a command: ').split(' ')
  if len(raw) != 3 or raw[0] not in commands:
    continue
  f = commands[raw[0]]
  x = y = 0
  try:
    [x, y] = map(int, raw[1:])
  except ValueError:
    continue
  if not (0 <= x < size and 0 <= y < size):
    continue
  #board_shown[x][y] = str(board_internal[x][y]) if (x, y) not in mines else 'X'
  f(x, y)
  #print_board(board_internal)
  print_board(board_shown)
  print lost
  print check_win()
  if check_win():
    break

if lost:
  print 'u lose'
else:
  print 'u win' 