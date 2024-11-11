import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import ttk
import tkinter as tk
import os
from fetch_games import fetch_lichess_games
import requests
import re
import time
from PIL import Image,ImageTk
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,String,Column,create_engine
from sqlalchemy.orm import sessionmaker
from fetch_from_fide import get_fide_player_info,get_rating



root = ctk.CTk()
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# Get the screen width and height
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# screen_width= 600
# screen_height= 400
# Set the window size to full screen
# root.geometry(f"{screen_width}x{screen_height}")
root.geometry("800x600+100+100")  # Correct

root.title("chess kef")



#==================DATABASE===========================
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DB_URI = os.path.join(ROOT_PATH,'my_db.db')
engine = create_engine(f'sqlite:///{DB_URI}',echo=True)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

#=====================================================
#==================CREATE TABLES=======================
class User(Base):
    __tablename__ ='users'
    user_id = Column(Integer,primary_key=True)
    fide_id  = Column(Integer)
    name = Column(String,nullable=False,unique=True)
    world_rank= Column(String)
    federation = Column(String,nullable=False)
    birthday = Column(String,nullable=False)
    sex = Column(String,nullable=False)
    fide_title = Column(String)
    phone = Column(String)
    email = Column(String)
    std = Column(String)
    rapid = Column(String)
    blitz =Column(String)






Base.metadata.create_all(bind=engine)
session =sessionmaker()(bind=engine)
session.commit()
#=====================================================












file_path = os.path.dirname(os.path.realpath(__file__))
image_1 = ctk.CTkImage(Image.open(file_path+"/images/knight.png"),size=(30,30))





# Create a customized toggle switch
def on_toggle():
    if toggle_switch.get() == 1:
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
    else:
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# Create a frame to hold the toggle switch and place it at the very top

top_frame4 = ctk.CTkFrame(master=root)
top_frame4.pack(side='top', fill='both',expand=True)
toggle_switch = ctk.CTkSwitch(
    master=top_frame4, 
    text="", 
    text_color ="white",
    command=on_toggle,
    fg_color="#9fb4b6",
    hover=True,
)

toggle_switch.pack(side='top', anchor='ne', pady=0, padx=0)
# Create a tab view
tabview = ctk.CTkTabview(root,width=700,height=500)
tabview.pack(side='top', fill='both', expand=True, pady=(10, 0), padx=10)






tab_login = tabview.add("Login")
tab_login_label = ctk.CTkLabel(tab_login, text="Login",font=('helvetica',24))
tab_login_label.pack(pady=20,padx=20)

my_entry_username = ctk.CTkEntry(tab_login,placeholder_text="Username")
my_entry_username.pack(pady = 10)
my_entry_password = ctk.CTkEntry(tab_login,placeholder_text="Password",show='*')
my_entry_password.pack(pady = 10)
def log():
    if my_entry_username.get() == "admin" and my_entry_password.get() =="1234":
        tabview.delete("Login")
        print("logged in!suucess")
        create_tab_add_player()
        create_tab_view_players()
        create_tab_fetch_games()
        return messagebox.showinfo("Login", "Your logged In!")
    else:
        
        return messagebox.showwarning("Login", "There is something wrong!")
tab1_button = ctk.CTkButton(tab_login, text="Submit", command=log)
tab1_button.pack(pady=20)


#=====================================================================================
def create_tab_add_player():


    tab_add_player = tabview.add("Add Player")
    tab_add_player_label = ctk.CTkLabel(tab_add_player, text="Add new player",font=('helvetica',24))
    tab_add_player_label.pack(pady=20)
    top_frame = ctk.CTkFrame(master=tab_add_player)
    top_frame.pack(side='top')


    def check_the_checkbox():
        if with_fide_id.get() == 'yes':
            name_entry.configure(state="disabled")
            birthday_entry.configure(state='disabled')
            radio_button1.configure(state='disabled')
            radio_button2.configure(state='disabled')
            fide_id_entry.configure(state="normal")
        else:
            name_entry.configure(state="normal")
            birthday_entry.configure(state='normal')
            radio_button1.configure(state='normal')
            radio_button2.configure(state='normal')
            fide_id_entry.configure(state="disabled")

        

    my_var = ctk.StringVar(value="no")
    with_fide_id = ctk.CTkCheckBox(top_frame,text='Fide ID',onvalue='yes',offvalue='no',command=check_the_checkbox)
    with_fide_id.pack(side='top')



    fide_id_entry = ctk.CTkEntry(top_frame,placeholder_text="Fide ID",state='readonly')
    fide_id_entry.pack(side='top',fill="x",pady=10,padx=10)
   
    email_entry =  ctk.CTkEntry(top_frame,placeholder_text="Email")
    email_entry.pack(side='right',fill="x",pady=10,padx=10)
    phone_entry = ctk.CTkEntry(top_frame,placeholder_text="Phone number")
    phone_entry.pack(side='left',fill="x",pady=10,padx=10)

    

    bottom_frame = ctk.CTkFrame(master=tab_add_player)
    bottom_frame.pack(side='top')

    name_entry = ctk.CTkEntry(bottom_frame,placeholder_text="Name")
    name_entry.pack(side='right',pady=10,padx=10)


    birthday_entry = ctk.CTkEntry(bottom_frame,placeholder_text="Birthday-year")
    birthday_entry.pack(side='left',pady=10,padx=10)

    bottom_frame2 = ctk.CTkFrame(master=tab_add_player)
    bottom_frame2.pack(side='top')



    def show_selected():
        print(f"Selected option: {selected_option.get()}")


    # Create a variable to hold the selected value
    selected_option = ctk.StringVar(value="")
    # Create radio buttons and place them in the window
    radio_button1 = ctk.CTkRadioButton(
        master=bottom_frame2, 
        text="Male", 
        variable=selected_option, 
        value="Male",
        command=show_selected
    )
    radio_button1.pack(side="right",pady=10, padx=30)

    radio_button2 = ctk.CTkRadioButton(
        master=bottom_frame2, 
        text="Female", 
        variable=selected_option, 
        value="Female",
        command=show_selected
    )
    radio_button2.pack(side="left",pady=10, padx=30)


    def add_player():
        if with_fide_id.get() == 'yes' :
            if fide_id_entry.get() == '' :
                messagebox.showwarning("Fide Id", "the Fide Id is wrong!!!")
            else :
                my_id = int(fide_id_entry.get())
                print(f"the id type is {type(my_id)}")
                if (my_id > 999999999) or (my_id< 100000):
                    messagebox.showwarning("Fide Id", "the Fide Id is wrong!!!")
                else:
                    try:
                        my_doc = get_fide_player_info(my_id)

                        fide_id = int(my_id)
                        print(fide_id)
                        name = my_doc['name']
                        infos = my_doc['all_infos']
                        
                        world_rank = infos['World Rank']
                        print(world_rank)
                        federation = infos['Federation']
                        birthday = infos['Birthday_year']
                        print(birthday)
                        sex = infos['Sex']
                        fide_title = infos['Fide_title']
                        phone = phone_entry.get()
                        email = email_entry.get()
                        my_rat = get_rating(my_id)
                        std= my_rat['STANDARD']
                        rapid= my_rat['RAPID']
                        blitz= my_rat['BLITZ']
                        
                        new_user = User(fide_id=fide_id,name=name,world_rank=world_rank,federation=federation
                            ,birthday=birthday,sex=sex,fide_title=fide_title,phone=phone,email=email,std=std,rapid=rapid,blitz=blitz)
                        session.add(new_user)
                        session.commit()
                      


                        
                        messagebox.showinfo("Players", "Player added successfully")
                        fide_id_entry.delete(0,tk.END)
                        phone_entry.delete(0,tk.END)
                        email_entry.delete(0,tk.END)



                    except Exception as e:
                        messagebox.showwarning("Problem", "there is a  problem") 

            
        else :
            name = name_entry.get()
            birthday = birthday_entry.get()
            sex = selected_option.get()
            phone = phone_entry.get()
            email = email_entry.get()
            if name != '' and birthday != "" and sex !="":
                new_user =  User(fide_id=None,name=name,world_rank=None,federation='Tunisia',birthday=birthday,sex=sex,fide_title=None
                    ,phone=phone,email=email)
                session.add(new_user)
                session.commit()
                messagebox.showinfo("Players", "Player added successfully")
            else:
                messagebox.showwarning("Add Player", "there is a missing value")  

     
            
            name_entry.delete(0,tk.END)
            birthday_entry.delete(0,tk.END)
            selected_option.set(None)
            phone_entry.delete(0,tk.END)
            email_entry.delete(0,tk.END)

        return print('added success')

    submit_button = ctk.CTkButton(tab_add_player, text="Submit", command=add_player)
    submit_button.pack(side='top',pady=20)

#=============================================================================================
def create_tab_view_players():
    tab_view_player = tabview.add("Players Informations")
    tab_view_player_label = ctk.CTkLabel(tab_view_player, text="List of players",font=('helvetica',24))
    tab_view_player_label.pack(pady=20)

    
    session = sessionmaker()(bind=engine) 
    
    def call():
        toplevel = tk.Toplevel(tab_view_player)
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        toplevel.geometry(f"{screen_width-300}x{screen_height-300}")
        custom_style = ttk.Style(toplevel)
        toplevel.configure(bg='#37383f')
        # Customize the theme for the Toplevel window
        custom_style.configure('Custom.TButton', background='blue', foreground='gray')
        custom_style = ttk.Style(toplevel)
        custom_style.map("Treeview", background=[('!selected', 'gray'),('selected', 'darkblue')])

        def update_item():
            selected_item = treeview.focus()
           
            
            if selected_item:
                item_values = treeview.item(selected_item, "values")
                print("Selected Item:", item_values[1])
                update_user = session.query(User).filter(User.name==item_values[1]).first()
                tab_update_player = tabview.add("update player")
                root.focus_force()
                #==============================
                top_frame = ctk.CTkFrame(master=tab_update_player)
                top_frame.pack(side='top')
                


                def check_the_checkbox():
                    if with_fide_id.get() == 'yes':
                        name_entry.configure(state="disabled")
                        birthday_entry.configure(state='disabled')
                        radio_button1.configure(state='disabled')
                        radio_button2.configure(state='disabled')
                        fide_id_entry.configure(state="normal")
                    else:
                        name_entry.configure(state="normal")
                        birthday_entry.configure(state='normal')
                        radio_button1.configure(state='normal')
                        radio_button2.configure(state='normal')
                        fide_id_entry.configure(state="disabled")

                    

                my_var = ctk.StringVar(value="no")
                with_fide_id = ctk.CTkCheckBox(top_frame,text='Fide ID',onvalue='yes',offvalue='no',command=check_the_checkbox)
                with_fide_id.pack(side='top')
                




                fide_id_entry = ctk.CTkEntry(top_frame,placeholder_text="Fide ID",state='readonly')
                fide_id_entry.pack(side='top',fill="x",pady=10,padx=10)
               
                email_entry =  ctk.CTkEntry(top_frame,placeholder_text="Email")
                email_entry.pack(side='right',fill="x",pady=10,padx=10)
                phone_entry = ctk.CTkEntry(top_frame,placeholder_text="Phone number")
                phone_entry.pack(side='left',fill="x",pady=10,padx=10)

                

                bottom_frame = ctk.CTkFrame(master=tab_update_player)
                bottom_frame.pack(side='top')

                name_entry = ctk.CTkEntry(bottom_frame,placeholder_text="Name")
                name_entry.pack(side='right',pady=10,padx=10)


                birthday_entry = ctk.CTkEntry(bottom_frame,placeholder_text="Birthday-year")
                birthday_entry.pack(side='left',pady=10,padx=10)

                bottom_frame2 = ctk.CTkFrame(master=tab_update_player)
                bottom_frame2.pack(side='top')



                def show_selected():
                    print(f"Selected option: {selected_option.get()}")


                # Create a variable to hold the selected value
                selected_option = ctk.StringVar(value="")
                # Create radio buttons and place them in the window
                radio_button1 = ctk.CTkRadioButton(
                    master=bottom_frame2, 
                    text="Male", 
                    variable=selected_option, 
                    value="Male",
                    command=show_selected
                )
                radio_button1.pack(side="right",pady=10, padx=30)

                radio_button2 = ctk.CTkRadioButton(
                    master=bottom_frame2, 
                    text="Female", 
                    variable=selected_option, 
                    value="Female",
                    command=show_selected
                )
                radio_button2.pack(side="left",pady=10, padx=30)
                print(update_user.fide_id)
                print(type(update_user.fide_id))
                if update_user.fide_id != None  :
                    with_fide_id.toggle()
                    fide_id_entry.insert(0,str(update_user.fide_id))
                    email_entry.insert(0,update_user.email)
                    phone_entry.insert(0,update_user.phone)
                else:
                    with_fide_id.deselect()
                    email_entry.insert(0,update_user.email)
                    phone_entry.insert(0,update_user.phone)
                    name_entry.insert(0,update_user.name)
                    birthday_entry.insert(0,update_user.birthday)
                    selected_option.set(update_user.sex)

                def update_them():
                    if update_user.fide_id != None :
                        update_user.fide_id = fide_id_entry.get()
                        update_user.email = email_entry.get()
                        update_user.phone = phone_entry.get()
                        
                        session.commit()
                        messagebox.showinfo("Players", "Player Updated successfully")
                        fide_id_entry.delete(0,tk.END)
                        phone_entry.delete(0,tk.END)
                        email_entry.delete(0,tk.END)
                        valeur=(update_user.fide_id,update_user.name,update_user.world_rank,update_user.federation,update_user.birthday,update_user.sex,update_user.fide_title
                            ,update_user.phone,update_user.email)
                        # If an item is selected
                        treeview.item(selected_item, values=valeur)
                    else:
                        update_user.email = email_entry.get()
                        update_user.phone = phone_entry.get()
                        update_user.birthday = birthday_entry.get()
                        update_user.sex = selected_option.get()
                        update_user.name = name_entry.get()
                        session.commit()
                        messagebox.showinfo("Players", "Player Updated successfully")
                        name_entry.delete(0,tk.END)
                        birthday_entry.delete(0,tk.END)
                        selected_option.set(None)
                        phone_entry.delete(0,tk.END)
                        email_entry.delete(0,tk.END)
                        valeur=(update_user.fide_id,update_user.name,update_user.world_rank,update_user.federation,update_user.birthday,update_user.sex,update_user.fide_title
                            ,update_user.phone,update_user.email)
                        # If an item is selected
                        treeview.item(selected_item, values=valeur)


            else:
                print("No item selected.")

            update_button = ctk.CTkButton(tab_update_player,text='Update',hover_color='#5dba34', fg_color='#358314',command=update_them)
            update_button.pack()

        vsb = ttk.Scrollbar(toplevel, orient="vertical")
        # Create a Treeview
        columns=( "fide_id","name","world_rank","federation","birthday","sex","fide_title","phone","email")
        treeview = ttk.Treeview(toplevel, style='Custom.Treeview',yscrollcommand=vsb.set)
         # Configure the style of the Treeview widget
        tree_style = ttk.Style()
        tree_style.configure("Custom.Treeview", background="red")
        treeview ['columns'] = columns
        vsb.config(command=treeview.yview)
        treeview.pack(side='top',fill="both", expand=True)
        vsb.pack(side="left", fill="y")
        
        # Define column headings
        treeview.heading("fide_id",text="FIDE ID")
        treeview.heading("name",text="Name")
        treeview.heading("world_rank",text="World Rank")
        treeview.heading("federation",text="Federation")
        treeview.heading("birthday",text="Birthday")
        treeview.heading("sex",text="Sex")
        treeview.heading("fide_title",text="FIDE Title")
        treeview.heading("phone",text="Phone")
        treeview.heading("email",text="Email")
        


        treeview.column("#0",width=20,anchor=tk.CENTER)
        treeview.column("fide_id",width=50,anchor=tk.CENTER)
        treeview.column("name",width=50,anchor=tk.CENTER)
        treeview.column("world_rank",width=40,anchor=tk.CENTER)
        treeview.column("federation",width=50,anchor=tk.CENTER)
        treeview.column("birthday",width=30,anchor=tk.CENTER)
        treeview.column("sex",width=30,anchor=tk.CENTER)
        treeview.column("fide_title",width=50,anchor=tk.CENTER)
        treeview.column("phone",width=50,anchor=tk.CENTER)
        treeview.column("email",width=70,anchor=tk.CENTER)


        def make_tree():
            i=0
            all_users = session.query(User).all()
            for user in all_users:
                i=i+1
                valeur=(user.fide_id,user.name,user.world_rank,user.federation,user.birthday,user.sex,user.fide_title
                    ,user.phone,user.email)
                treeview.insert("", "end", text=f"{i}", values=valeur)

        make_tree()

        def delete_user():
            selected_item = treeview.focus()
            if selected_item:
                item_values = treeview.item(selected_item, "values")
                print("Selected Item:", item_values[1])
                deleted_user = session.query(User).filter(User.name==item_values[1]).first()
                
                response =messagebox.askokcancel("OK Cancel", f"Do you want to delete {deleted_user.name}?")
                if response :
                    treeview.delete(selected_item)
                    session.delete(deleted_user)
                    session.commit()
                    messagebox.showinfo("Deleted", "User delete successfully!")
                    
                    
                else:
                    deleted_user =''
            else:
                print("No item selected.")

        # Insert some sample data
        # treeview.insert("", "end", text="1", values=show())
        # treeview.insert("", "end", text="2", values=show())
        # treeview.insert("", "end", text="3", values=show())

        # Create a button to get the selected item
        down_frame = ctk.CTkFrame(master=toplevel)
        down_frame.pack(side='bottom',fill='both')
        button = ctk.CTkButton(down_frame, text="update",hover_color='#5dba34', fg_color='#358314',command=update_item)
        button.pack(side='left',padx=30)
        delete_buuton = ctk.CTkButton(down_frame, text="delete",fg_color='#d72020', hover_color='#e74a4a',command=delete_user)
        delete_buuton.pack(side='right',padx=30)


    submit_button = ctk.CTkButton(tab_view_player, text="View All Players", command=call)
    submit_button.pack(side='top',pady=20)


def create_tab_fetch_games():
    tab_fetch_games = tabview.add("Search Games")


    label= ctk.CTkLabel(tab_fetch_games,text='Lichess username :',font=('helvetica',18))
    label.pack(side='top')
    lichess_user_entry = ctk.CTkEntry(tab_fetch_games,height=30,width=160)
    lichess_user_entry.pack(side='top',padx=20,pady=10)



   

    my_progressbar = ctk.CTkProgressBar(tab_fetch_games,progress_color="red")
    my_progressbar.pack(side='top',pady=10)
    my_progressbar.set(0)
    value_of_progress = int(my_progressbar.get()*100)

    def clicker():
        username=lichess_user_entry.get()
        
        fetch_lichess_games(username,'lichess_games',4)
        for i in range(100):
            if i < 30 :
                my_progressbar.set(i)
            elif i > 30 and i < 66 :
                my_progressbar.configure(progress_color='blue')
                my_progressbar.set(i)
            else:
                my_progressbar.configure(progress_color='green')
                my_progressbar.set(i) 
                if i == 99 :
                    messagebox.showinfo("Download", "The games downloaded successfully!")
        my_progressbar.configure(progress_color='red')
        my_progressbar.set(0)

        lichess_user_entry.delete(0,tk.END)


    search_button = ctk.CTkButton(tab_fetch_games,text='Search',command=clicker)
    search_button.pack()






if __name__ =="__main__":
    root.mainloop()




