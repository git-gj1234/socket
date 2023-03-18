import socket
from tkinter import *
from tkinter.ttk import *
import time
import errno
import tkinter as tk
import random
GAME_PORT = 5007
def moveBaseLR(c,base, direction, x, y = 0):
    x1, y1, x2, y2 = c.coords(base)
    if ((x1 > 0 and direction == 'l') or (x2 < 400 and direction == 'r')):
        c.move(base, x, y)
        c.update()

def key_press(event,game_socket):
  #print("a\n"*10)
  a = str(event.keycode)
  print(a)
  game_socket.send(a.encode())
  #print("sent")

def key_press2(event,game_socket,base,c):
  #print("a\n"*10)
  a = int(event.keycode)
  if(int(a) == 37):
       moveBaseLR(c,base, 'l', 0-10)
  if(int(a) == 39):
       moveBaseLR(c,base, 'r', 10)
     
  #print("sent")
# represents the game state
board = ''

#def print_current_board():
#  print('board:..')

#def get_users_move():
#  move = input('What is your move: ')
#  return move

def update_game_state(player, move,base,c):
  global board 

  if(move ):
    if(( move.lstrip('g'))):
      if(move.lstrip('g').rstrip('g')):
       print(move.lstrip('g').rstrip('g'))
  # update the board
  if(int(move) == 37):
       moveBaseLR(c,base, 'l', 0-10)
  if(int(move) == 39):
       moveBaseLR(c,base, 'r', 10)
  
  if 'g' not in move:
    board = board + move
    print(player + ' played ' + move)
    

def has_game_ended():
  if (board == 'abcd'):
    return True
  else:
    return False

def game_server():

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as accepter_socket:
      accepter_socket.bind(('', GAME_PORT))
      accepter_socket.listen(1)

      game_socket, addr = accepter_socket.accept()
      game_socket.setblocking(False)

      with game_socket:
        print('Game Started')

        root = Tk()
        score1 = 0
        score2 = 0
        root.minsize(400,400)
        basespeed = 10
        ballspeed = 1
        
        isFailed = False

        c = Canvas(width=400, height=400, background='#000')
        coordinates = 0,200,400,200

    # Draw a dashed vertical line, 5px dash and 1px space
        c.create_line(coordinates, dash=(5,1), fill="white")
        c.pack()
        base = c.create_rectangle(150, 385, 250, 400, fill='blue', outline='blue')
        base2 =  c.create_rectangle(150, 0, 250, 20, fill='blue', outline='blue')
        ball = c.create_oval(190, 365, 210, 385, fill='red', outline='red')    
        txtS = tk.Entry(c, text='2')
        txtS2 = tk.Entry(c, text='1')
        txtScore = c.create_window(380, 180, anchor='nw', window=txtS)
        txtScore2 = c.create_window(380, 200, anchor='nw', window=txtS2)
        lblM = tk.Label(c, text='Failed!!!Press Enter key to start again')
        lblID = c.create_window(100, 190, anchor='nw', window=lblM)
        c.itemconfigure(lblID, state='hidden')
       
        root.bind('<Key>', lambda event: key_press2(event,game_socket,base,c),(game_socket,base,c))
        #startBall(c,txtS,txtS2,lblID,ball, ballspeed,base,base2)
        s = random.randint(-ballspeed, ballspeed)
        x, y = s,ballspeed #Start. Ball to move in random direction. 0-speed is used to get negative value
        c.move(ball, x, y)
        while True:

          

          l, t, r, b = c.coords(ball)
          txtS.delete(0, END)
          #txtS2.delete(0, END)
          txtS.insert(0, str(score1))
          #txtS2.insert(0, str("score2"))
          #Need to change direction on hitting wall. Eight options are there.
          if(r >= 400 and x >= 0 and y < 0): #Ball moving ↗ and hit right wall
              x, y = 0-ballspeed, 0-ballspeed
          elif(r >= 400 and x >= 0 and y >= 0): #Ball moving ↘ and hit right wall
              x, y = 0-ballspeed, ballspeed
          elif(l <= 0 and x < 0 and y < 0): #Ball moving ↖ and hit left wall
              x, y = ballspeed, 0-ballspeed
          elif(l <= 0 and x < 0 and y >= 0): #Ball moving ↙ and hit left wall
              x, y = ballspeed, ballspeed
          # elif(t <= 0 and x >= 0 and y < 0): #Ball moving ↗ and hit top wall
          #     x, y = speed, speed
          # elif(t <= 0 and x < 0 and y < 0): #Ball moving ↖ and hit top wall
          #     x, y = 0-speed, speed
          elif(b >= 385): #Ball reached base level. Check if base touches ball
              tchPt = l + 10 #Size is 20. Half of it.
              bsl, bst, bsr, bsb = c.coords(base)
              if(tchPt >= bsl and tchPt <= bsr): #Ball touch base
                  n = random.randint(-ballspeed, ballspeed)
                  x, y = n, 0-ballspeed
              else: #Hit bottom. Failed
                  c.itemconfigure(lblID, state='normal')
                  
                  isFailed = True
                  score1 = score1+1
                  print(score1,score2)
                  txtS.delete(0, END)
                  #txtS2.delete(0, END)
                  txtS.insert(0, str(score1))
                  #txtS2.insert(0, str(score2))
                  break

          elif(b <= 40): #Ball reached base level. Check if base touches ball
              tchPt = l + 10 #Size is 20. Half of it.
              bsl, bst, bsr, bsb = c.coords(base2)
              if(tchPt >= bsl and tchPt <= bsr): #Ball touch base
                  n = random.randint(-ballspeed, ballspeed)
                  x, y =  0-ballspeed,ballspeed
              else: #Hit bottom. Failed
                  c.itemconfigure(lblID, state='normal')
                  score2 = score2+1
                  print(score1,score2)
                  isFailed = True
                  
                  txtS2.delete(0, END)
                  
                  txtS2.insert(0, str(score2))
                  break
        
          time.sleep(.025)
          c.move(ball, x, y)
          c.update()
          root.update()
          print("c1")
          try :
            opp_move = game_socket.recv(1024)
          except socket.error as e:
            if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
              continue
          print("c2")
        
        # if not opp_move:
        #   break
          opp_move = opp_move.decode()
          update_game_state('opp', opp_move,base2,c)


      #print_current_board()
      print('Game ended')

def game_client(opponent):

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
      game_socket.connect((opponent, GAME_PORT))
      game_socket.setblocking(False)
      print('Game Started')

      root2 = Tk()
      root2.geometry('200x100')
      root2.bind('<Key>', lambda event: key_press(event,game_socket),game_socket)

      while True:


        
        root2.update()
        #print_current_board()
        
        try :
          opp_move = game_socket.recv(1024)
        except socket.error as e:
          if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
            continue
        
        # if not opp_move:
        #   break

        
        
        if has_game_ended():
          break
        time.sleep(0.25)

  #print_current_board()
  print('Game ended')