# -*- coding: utf-8 -*-

##############################################################################
#                                                                            #
#                               JEU D'ECHEC :                                #
#                                                                            #
#                           COPYRIGHT ©2020, L.A.                            #
#                                                                            #
#                            ALL RIGHTS RESERVED                             #
#                                                                            #
##############################################################################

import tkinter as tk
import socket, threading
from math import floor
from objects import * # Second File

tk_window = 0
th_C = 0
th_R = 0
end = False
msg_recv = False
urlSave = ""
chess_board = 0
menu = 0

class ThreadCreateSocket(threading.Thread):
    
    def __init__(self,host,port,widgets):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.widgets = widgets
        
    def run(self):
        global th_R, tk_window
        
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind((self.host, self.port))
        self.connection.listen(5)
        self.widgets[2][6].grid(row=0,column=0)
        print("\nLe serveur ecoute a  present sur le port {}".format(self.port))
        try:
            connection_client, infos_connection = self.connection.accept()
        except:
            print("Une erreur est survenue lors de la creation du socket.")
        else:
            print("CONNEXION ETABLIE...")
            self.widgets[2][6].grid_forget()
            self.widgets[2][7].grid(row=0,column=0)
            self.widgets[2][8].grid(row=1,column=0)
            self.widgets[2][9].grid(row=1,column=1)
            self.widgets[2][10].grid(row=0,column=0)
        
        th_R = ThreadReception(self.connection,connection_client)
        th_R.start()

class ThreadReception(threading.Thread):
    
    def __init__(self,connection,connection_client):
        threading.Thread.__init__(self)
        self.connection = connection
        self.connection_client = connection_client
        
    def run(self):
        global chess_board, th_C, msg_recv, tk_window, end
        msg = b""
        try:
            while msg != b"EXIT":
                msg = self.connection_client.recv(1024)
                if msg == b"GO":
                    msg = b"READY"
                    self.connection_client.send(msg)
                    data = b""
                    packet = self.connection_client.recv(4096)
                    data += packet
                    
                    chess_board = pickle.loads(data)
                    end = 1 # stoppe la boucle de tkinter
                elif msg == b"READY":
                    #chess_board.supp_all_img()
                    obj = pickle.dumps(chess_board)
                    self.connection_client.send(obj) # il faut que les img soit supp
                    chess_board.img_setup = True # indique qu'on peut recharger les imgs
                else:
                    tab = pickle.loads(msg)
                    #tab = "".join(str(v) for v in tab)
                    print("message recv : ",tab)
                    
                    chess_board.inverse_board() # on inverse le sens du terrain
                    
                    chess_board.sqr[tab[0]][tab[1]].set_coord(tab[2],tab[3],chess_board)
                    if tab[4] == 1:
                        chess_board.sqr[tab[0]][tab[1]].piece = "queen"
                        chess_board.sqr[tab[0]][tab[1]].imgSetup = False
                        chess_board.sqr[tab[0]][tab[1]].load_Img()
                    if tab[5] != 99:
                        chess_board.sqr[tab[5]][tab[6]].delete()

                    chess_board.inverse_board() # on remet le terrain ds le bon sens
                    msg_recv = True
                       
        except:
            print("Une erreur est survenue lors de la reception d'un message.")
            
            
        if msg.upper() == "EXIT":
            print("Un joueur est parti.")

def send_to_player(tab):
    global th_R
    try:
        data = pickle.dumps(tab) # IL FAUT SUPP LES IMAGES DE CHESSBOARD AVANT
        th_R.connection_client.send(data)
        print("send to client : ",tab)
    except:
        print("Une erreur est survenue lors de l'envoie d'un message.")
        pass

def start_game(url_save=None,p=0):
    global chess_board, th_R, msg_recv
    player = p
    allow = True
    loop = 1
    click = 0
    last = [99,99,99]
    check = [0,0]
    colorOf = ""

    pygame.init()
    pygame.display.set_caption("Checkmate_!")
    window = pygame.display.set_mode((596,656))  
    window.fill((255,255,255))

    if msg_recv is False:
        chess_board = setup_game(url_save)
        try:
            chess_board.supp_all_img() # 
            th_R.connection_client.send(b"GO") # On envoie le signal de lancement a l'autre joueur.
            while chess_board.img_setup is False:
                continue
        except:
            pass
        finally:
            chess_board.load_all_img()
    else:                                   
        chess_board.load_all_img()# LES CHARGER APRES LE LANCEMENT DE PYGAME !  

    chess_board.disp(window)
    
    if player== 1:
      chess_board.inverse_board()
      
    chess_board.paste(window)
    
    pygame.display.flip()

    while loop:

      for event in pygame.event.get():
    
        if event.type == QUIT:
          loop = 0
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_s:
            save_game(chess_board)
        elif event.type == pygame.MOUSEBUTTONDOWN:
          chess_board.disp(window)
          if event.button == 1:
              pos = pygame.mouse.get_pos()
              try:
                  last[0] = c
                  last[1] = l
                  chess_board.refresh_sqr(window,last[0],last[1])
              except:
                pass
    
              c = floor((pos[0]-10)/72)
              l = floor((pos[1]-70)/72)
              colorOf = wht_is_the_color(player)
              chess_board.refresh_sqr(window,c,l,1)
              temp = chess_board.test_coords(c,l)
              exchange = [0,0,0,0,0,99,99]
              
              if chess_board.check(window,player) == 0:
                  check[player] = 1
              
              if type(temp) is tuple and chess_board.sqr[temp[0]][temp[1]].typeOf == player:
                coor = chess_board.sqr[temp[0]][temp[1]].hilfe(window,chess_board,True) # False --> enlever l'aide
                last[2] = coor
        
              elif type(last[2]) is tuple:
    
                  for i,elt in enumerate(last[2]):
                      if (c,l) == elt:
                          temp = chess_board.test_coords(last[0],last[1])
                          old = [chess_board.sqr[temp[0]][temp[1]].c,chess_board.sqr[temp[0]][temp[1]].l]
                          chess_board.sqr[temp[0]][temp[1]].set_coord(c,l,chess_board)
                          if chess_board.check(window,player) == 0: # Si le joueur est en ECHEC
                              chess_board.sqr[temp[0]][temp[1]].set_coord(old[0],old[1],chess_board)
                              break
                          chess_board.sqr[temp[0]][temp[1]].set_coord(old[0],old[1],chess_board)
                          chess_board.refresh_sqr(window,c,l)
                          temp = chess_board.test_coords(elt[0],elt[1])
                          if type(temp) is tuple:
                              chess_board.sqr[temp[0]][temp[1]].delete()
                              exchange[5] = temp[0]
                              exchange[6] = temp[1]
                              
                          temp = chess_board.test_coords(last[0],last[1])###########AJOUTER DANS UNE LISTE QUE LE PION EST MORT,,,ET LES STATS DU Â¨PION ??
                          exchange[0] = temp[0]
                          exchange[1] = temp[1]
                          exchange[2] = c
                          exchange[3] = l
                          if chess_board.sqr[temp[0]][temp[1]].piece == "pawn" and l == 0:
                            chess_board.sqr[temp[0]][temp[1]].piece = "queen"
                            chess_board.sqr[temp[0]][temp[1]].imgSetup = False
                            chess_board.sqr[temp[0]][temp[1]].load_Img()
                            exchange[4] = 1
                          chess_board.sqr[temp[0]][temp[1]].set_coord(c,l,chess_board)
                          print("\n{} {} ({},{}) go to ({},{})".format(colorOf.capitalize(),
                                chess_board.sqr[temp[0]][temp[1]].piece.capitalize(),
                                old[0],old[1],c,l))
                          
                          send_to_player(exchange)
                          break
                  last[2] = tuple() # on reset les coordonnÃ©es de last[2]

          elif event.button == 3:
              if th_R == 0:
                chess_board.inverse_board()
                player = inverse_player(player)
          
          chess_board.paste(window)
          pygame.display.flip()
      
      if msg_recv == True:
          msg_recv = False
          chess_board.disp(window)
          chess_board.paste(window)
          pygame.display.flip()
      
    #th_R = 0
    pygame.display.quit()
    
    if th_R != 0:  
        print("connection closed.")
        try:
            th_R.connection_client.close()
            th_R.connection.close()
        except:
            pass
    
    switch_menu()

def tk_menu():
    global th_R, th_C, tk_window, menu, urlSave
    tk_window = tk.Tk()
    
    tk_window.title("Checkmate")
    tk_window.geometry("596x656")
    tk_window.minsize(596,656)
    tk_window.maxsize(1080,720)
    tk_window.config(background="#abcdef")

    bg_color = "#fff"
    
    frame = tk.Frame(tk_window, bg=bg_color)
    top_frame = tk.Frame(frame, bg=bg_color)
    middle_frame = tk.Frame(frame, bg=bg_color)
    bottom_frame = tk.Frame(frame, bg=bg_color)
    rlly_bottom_frame = tk.Frame(frame, bg=bg_color)
    
    widgets = [[],[],[]]
    
    ##### PAGE 1 :
    
    solo_button = tk.Button(frame, width=20, text="Solo", font=("Helvetica",25), 
    bg='#fff', fg='black',
    command=lambda who=1: switchWidgets(widgets,0,1))
    
    solo_button.grid(row=0,column=0)
    
    multi_button = tk.Button(frame, width=20, text="Multiplayer", 
    font=("Helvetica",25), bg='#fff', fg='black', 
    command=lambda who=1: switchWidgets(widgets,0,2))
    
    multi_button.grid(row=1,column=0)
    
    ##### PAGE 2 :
    
    IP_label = tk.Label(middle_frame, text="IP : ", font=("Helvetica",25), bg=bg_color, fg='#000')
    
    ip_var = tk.StringVar()
    ip_var.set(socket.gethostbyname(socket.gethostname()))
    IP_entry = tk.Entry(middle_frame, textvariable=ip_var, width=12, font=("Helvetica",25), bg=bg_color, fg='black')
    
    Port_label = tk.Label(middle_frame, text="Port : ", font=("Helvetica",25), bg=bg_color, fg='#000')
    
    port_var = tk.StringVar()
    port_var.set("12800")
    Port_entry = tk.Entry(middle_frame, textvariable=port_var, width=12, font=("Helvetica",25), bg=bg_color, fg='black')
    
    host_button = tk.Button(bottom_frame, width=8, text="Host", font=("Helvetica",25), 
    bg=bg_color, fg='black', command=lambda who=1: create_socket(ip_var.get(),
    int(port_var.get()),widgets))
    
    join_button = tk.Button(bottom_frame, width=8, text="Join", font=("Helvetica",25), 
    bg=bg_color, fg='black', command=lambda who=1: join_socket(ip_var.get(),
    int(port_var.get()),widgets))

    ##### BACK_BUTTON : 
    back_button = tk.Button(tk_window, width=8, text="Back", 
    font=("Helvetica",25), bg=bg_color, fg='black')

    ##### SUCESS MSG :
    sucess_msg = tk.Label(top_frame, text="The game is starting 2/2", 
    font=("Helvetica",25), bg=bg_color, fg='#2bf728')
    
    ##### WAITING FOR A PLAYER MSG :
    waiting_msg = tk.Label(top_frame, text="Waiting for a player 1/2", 
    font=("Helvetica",25), bg=bg_color, fg='#474747')
    
    ##### ENTRY + BUTTON --> OPEN A SAVED GAME :
    openSave_var = tk.StringVar()
    openSave_var.set("")
    openSave_entry = tk.Entry(bottom_frame, textvariable=openSave_var, width=12, 
    font=("Helvetica",25), bg=bg_color, fg='black')
    openSave_button = tk.Button(bottom_frame, width=8, text="Open save", 
    font=("Helvetica",25), bg=bg_color, fg='black', 
    command=lambda who=1: choose_file(openSave_var))

    ##### START BUTTON :
    start_button = tk.Button(rlly_bottom_frame, width=15, text="Start", 
    font=("Helvetica",25), bg=bg_color, fg='black',
    command=lambda who=1: switch_menu(urlSave))

    ##### WAITING... THE GAME IS STARTING... :
    wait_game_msg = tk.Label(middle_frame, text="Waiting...", 
    font=("Helvetica",45), bg=bg_color, fg='#474747')

    ## MENU :
    widgets[0].append(solo_button)
    widgets[0].append(multi_button)
    ## PAGE 1:
    widgets[1].append(openSave_entry)
    widgets[1].append(openSave_button)
    widgets[1].append(start_button)
    ## PAGE 2:
    widgets[2].append(IP_label)
    widgets[2].append(IP_entry)
    widgets[2].append(Port_label)
    widgets[2].append(Port_entry)
    widgets[2].append(host_button)
    widgets[2].append(join_button)
    widgets[2].append(waiting_msg)
    widgets[2].append(sucess_msg)
    widgets[2].append(openSave_entry)
    widgets[2].append(openSave_button)
    widgets[2].append(start_button)
    widgets[2].append(wait_game_msg)
    
    top_frame.grid(row=0,column=0)
    middle_frame.grid(row=1,column=0)
    bottom_frame.grid(row=2,column=0)
    rlly_bottom_frame.grid(row=3,column=0)
    
    frame.pack(expand=tk.YES)
    
    tk_window.after(50,test_if_tk_end)
    tk_window.mainloop()
    

def test_if_tk_end():
    global end, tk_window, msg_recv
    if end != 0:
        msg_recv = True
        end = 0
        switch_menu(player = 1)
        return
    tk_window.after(10,test_if_tk_end)

def choose_file(name_file):
    global urlSave
    urlSave = os.path.split(filedialog.askopenfile().name)
    name_file.set(urlSave[1])
    urlSave = str(urlSave[0] + "/" + urlSave[1])

def create_socket(hote,port,widgets):
    global th_C
    print(hote,port)
    
    th_C = ThreadCreateSocket(hote,port,widgets)
    th_C.start()

def join_socket(hote,port,widgets):
    global th_R
    print(hote,port)
    try:
        connection_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_server.connect((hote, port))
    except:
        print("Impossible de se connecter a l'hote distant")
    else:
        print("\nConnexion etablie avec le serveur sur le port {}".format(port))
        for i in range(11):
            if i != 6:
                widgets[2][i].grid_forget()
        widgets[2][11].grid(row=0,column=0)
        th_R = ThreadReception(None,connection_server)
        th_R.start()
        
def switchWidgets(widgets_list,last_page,page):

    if widgets_list != []:
        for (i, j) in enumerate(widgets_list[last_page]):
            j.grid_forget() 

    if page == 1:
        grid_list = [(1,0),(1,1),(0,0)]
    elif page == 2:
        grid_list = [(0,0),(0,1),(1,0),(1,1),(0,0),(0,1)]
        
    for i,elt in enumerate(grid_list):
        widgets_list[page][i].grid(row=elt[0],column=elt[1],pady=i)
    
    """ 
    for (i,elt) in enumerate(widgets_list[page]):   # erreur a cause de waiting , sucess msg etc.....
        elt.grid(row=grid_list[i][0],column=grid_list[i][1],pady=i)
        """
def switch_menu(url_save=None,player = 0):
    global menu, tk_window
    if menu == 0:
        menu = 1
        tk_window.destroy()
        print("The game is starting...")
        print("Game Url : ",url_save)
        start_game(url_save,player)
    else:
        menu = 0
        tk_menu()

# MAIN LOOP :
        
print("\n\nYou can take your IP in this list for multiplayer : \n")
os.system("ipconfig")
os.system("ifconfig")

tk_menu()
       
          
          
          
          
          
          
