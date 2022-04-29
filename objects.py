# -*- coding: utf-8 -*-

# JEU D'ECHEC --> Second File
# COPYRIGHT ©2020, L.A. 

import pygame, pickle, os
from pygame.locals import *
from tkinter import filedialog

def wht_is_the_color(p):
    if p == 0:
      return "white"
    else:
      return "black"

def inverse_player(p):
    if p == 1:
        return 0
    else:
        return 1

def inverse_color(c,c1,c2):
  if c == c1:
    return c2
  else:
    return c1

def save_game(obj,name_file=""):
    url = "./saves/"
    index = 1
    for elt in obj.sqr:
        for elt2 in elt:
            elt2.img = 0
    
    if name_file == "":
        while 1:
            file_url = url + "save_" + str(index) + ".dat"
            if os.path.isfile(file_url) is False:
                with open(file_url,"wb") as file:
                    pickle.dump(obj,file)
                break
            else:
                index+=1
    else:
        with open(name_file,"wb") as file:
            pickle.dump(obj,file)
    
    for elt in obj.sqr:
        for elt2 in elt:
            elt2.imgSetup = False
            elt2.load_Img()
            
def load_game(name_file):
    with open(name_file,'rb') as file:
        board = pickle.load(file)
        for elt in board.sqr:
            for elt2 in elt:
                elt2.imgSetup = False
                elt2.load_Img()
        return board

def setup_game(url):
    
    if url != None:
        try:
            board = load_game(url)
            if type(board) is ChessBoard:
                return board
            else:
                file_error = os.path.split(url)
                print("Le fichier de sauvegarde {} est corrompue.".format(
                file_error[1]))
        except:
            print("La partie n'a pas pu être charge.")
    board = ChessBoard(10,70,72,72,(255,255,255),(107,127,177))
    return board

class ChessBoard:
  
  def __init__(self,x,y,w,h,c1,c2,border_c=(0,0,0)):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.c1 = c1
    self.c2 = c2
    self.img_setup = False
    self.border_c = border_c
    self.setup()

  def disp(self,window):
    c = self.c1
    for j in range(8):
      for i in range(8):
        pygame.draw.rect(window, (0,0,0), pygame.Rect(self.x+i*self.w, 
        self.y+j*self.h, self.w, self.h), 3)
        pygame.draw.rect(window, c, pygame.Rect(self.x+1+i*self.w, 
        self.y+1+j*self.h, self.w-2, self.h-2), 0)
        c = inverse_color(c,self.c1,self.c2)
      c = inverse_color(c,self.c1,self.c2)

  def load_all_img(self):
    for elt in self.sqr:
      for elt2 in elt:
        elt2.imgSetup = False
        elt2.load_Img()
    self.img_setup = True

  def supp_all_img(self):
    for elt in self.sqr:
      for elt2 in elt:
        elt2.img = 0
    self.img_setup = False
    
  def refresh_sqr(self,window,column,line,underline=False,fill=False):
    
    tx = self.x+(column*self.w)
    ty = self.y+(line*self.h)
    if fill:
        pygame.draw.rect(window, (255,255,0), pygame.Rect(tx+1, ty+1, self.w-2, 
        self.h-2), 0)
    elif underline:
        pygame.draw.rect(window, (255,0,0), pygame.Rect(tx, ty, self.w, 
        self.h), 1)
    else:
        pygame.draw.rect(window, (0,0,0), pygame.Rect(tx, ty, self.w, 
        self.h), 1)
        
  def paste(self,window):
    for i,elt in enumerate(self.sqr):
      for j,elt2 in enumerate(elt):
        if elt2.alive:
          elt2.paste(window)
  def test_coords(self,c,l):
    if c < 0 or c > 7 or l < 0 or l > 7:
        return -1
    for i,elt in enumerate(self.sqr):
      for j,elt2 in enumerate(elt):
        if elt2.c == c and elt2.l == l:
          return (i,j)

    return 1

  def check(self,window,player,coord=None,):
    try:
        c = coord[0]
        l = coord[1]
    except:
      if player == 1:
        c = self.sqr[0][4].c # Correspond au roi noir
        l = self.sqr[0][4].l
      else:
        c = self.sqr[3][4].c # Correspond au roi blanc
        l = self.sqr[3][4].l
      for i in range(4):
        for elt in self.sqr[i]:
          if elt.typeOf == inverse_player(player):
            for elt2 in elt.hilfe(window,self,color=False):
                if elt2 == (c,l):
                  return 0
      return 1

  def setup(self):
      self.sqr = [[0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0]]

      chess_list = ["rook","knight","bishop","queen",
                    "king","bishop","knight","rook"]
      
      # On charges les pions NOIRS:
      for i in range(8):
        self.sqr[0][i] = ChessPiece(chess_list[i],1,i,0,self)
        
      for i in range(8):
          self.sqr[1][i] = ChessPiece("pawn",1,i,1,self)
        
      # On charge les pions BLANCS :
      for i in range(8):
          self.sqr[2][i] = ChessPiece("pawn",0,i,6,self)
          
      for i in range(8):
        self.sqr[3][i] = ChessPiece(chess_list[i],0,i,7,self)
        
  def inverse_board(self):
    for j in range(4):
        for i in range(8):
            self.sqr[j][i].inverse_pos(self)

class ChessPiece(ChessBoard):
    
  def __init__(self,piece,typeOf,c,l,board,alive=True):
    self.typeOf = typeOf
    self.piece = piece
    self.c = c
    self.l = l
    self.x = board.x+c*board.w
    self.y = board.y+l*board.h
    self.alive = alive
    self.img = 0
    self.imgSetup = False
    self.load_Img()
  def load_Img(self):
    if self.imgSetup is False:
      self.imgSetup = True
      if self.typeOf == 0:
        url = "data/w_"
      else:
        url = "data/b_"
      self.img = pygame.image.load(url+self.piece+".png")#.convert() --> cree un bug
      
  def paste(self,window):
      if self.alive:
          window.blit(self.img,(self.x,self.y))
  
  def inverse_pos(self,board):
      self.c = 7-self.c
      self.l = 7-self.l
      self.refresh_coord(board)
  
  def refresh_coord(self,board):
      self.x = board.x+self.c*board.w
      self.y = board.y+self.l*board.h
        
  def set_coord(self,c,l,board):
      self.c = c
      self.l = l
      self.refresh_coord(board)
      
  def hilfe(self,window,board,color=True):
    p = self.piece
    c = self.c
    l = self.l
    try_coords = {"pawn":[(c-1,l-1),(c+1,l-1)],
                  "knight":[(c-1,l-2),(c+1,l-2),(c-1,l+2),(c+1,l+2),
                  (c-2,l+1),(c-2,l-1),(c+2,l+1),(c+2,l-1)],
                  "king":[(c-1,l-1),(c,l-1),(c+1,l-1),(c-1,l),
                  (c+1,l),(c-1,l+1),(c,l+1),(c+1,l+1)]}
    sucess_coords = list()
    if p == "pawn":
      if self.l == 6:
        if board.test_coords(c,l-1) == 1:# and board.test_coords(c,l-2) == 1:
          board.refresh_sqr(window,c,l-1,fill=color)
          board.refresh_sqr(window,c,l-2,fill=color)
          sucess_coords.append((c,l-1))
          sucess_coords.append((c,l-2))
      
      if board.test_coords(c,l-1) == 1:
        board.refresh_sqr(window,c,l-1,fill=color)
        sucess_coords.append((c,l-1))
              
    if p == "rook" or p == "queen":
      k=1;j=1;h=0
      for i in range(4):
          if k == 1:
              k = -1
          elif k == -1:
              k = 1
              
          if j != 0:
              j = k
          else:
              h = k
              
          stop = False
          while (j < 8 and j > -8) and (h < 8 and h > -8) and stop is False:
            coord = (c+h,l+j)
            test_coord = board.test_coords(coord[0],coord[1])
            if type(test_coord) is tuple:
                if board.sqr[test_coord[0]][test_coord[1]].typeOf != self.typeOf:
                  stop = True
                else:
                    break
            if board.test_coords(c+h,l+j) != -1:# and board.test_coords(c+h,l+j) != 2:
              board.refresh_sqr(window,coord[0],coord[1],fill=color)
              sucess_coords.append(coord)
            if j!= 0:
              j += k
            else:
              h += k
          
          if k == 1:
            j = 0
            
    if p == "queen" or p == "bishop":
        k=1;j=1;h=0;w=0
        for i in range(4):
            
            if i == 0:
              h=1;j=1
            elif i == 1:
              h=-1;j=-1
            elif i == 2:
              j=1;h=-1
            else:
              j=-1;h=1
            k=j;w=h
            stop = False
            while (j < 8 and j > -8) and (h < 8 and h > -8) and stop is False:
              coord = (c+j,l+h)
              test_coord = board.test_coords(coord[0],coord[1])
              if type(test_coord) is tuple:
                  if board.sqr[test_coord[0]][test_coord[1]].typeOf != self.typeOf:
                    stop = True
                  else:
                      break
              
              if board.test_coords(c+j,l+h) != -1 and board.test_coords(c+j,l+h) != 2:
                board.refresh_sqr(window,coord[0],coord[1],fill=color)
                sucess_coords.append(coord)
              j += k
              h += w       

    try:
      for elt in try_coords[p]:
          attack_coord = board.test_coords(elt[0],elt[1])
          if type(attack_coord) is tuple:
            if board.sqr[attack_coord[0]][attack_coord[1]].typeOf != self.typeOf:
             # if board.sqr[attack_coord[0]][attack_coord[1]].piece != "king":
                board.refresh_sqr(window,elt[0],elt[1],fill=color)
                sucess_coords.append(elt)
          elif attack_coord == 1 and p != "pawn":
              board.refresh_sqr(window,elt[0],elt[1],fill=color)
              sucess_coords.append(elt)
    except:
      pass
    
    return tuple(sucess_coords)
      
  def delete(self):
      self.c = 99+self.c
      self.l = 99+self.l
      self.alive = 0
      
    
    
   
    
    
    
    
    
    
    
