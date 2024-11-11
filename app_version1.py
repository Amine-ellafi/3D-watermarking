import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import os
# import requests
# import re
import time
from PIL import Image,ImageTk
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,String,Column,create_engine,DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from sqlalchemy.orm import relationship
import dct2 as dct
import off_to_obj as oto
import try5 as lsb
import numpy as np
import colorama
from colorama import Fore, Style
import hashlib

# Initialize colorama (important for Windows)
colorama.init(autoreset=True)

# Create the main window

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x400")
app.title("Watermark 3D images")

#=================================================================================

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
    user_id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False,unique=True)
    email = Column(String)
    password = Column(String,nullable=False)

    # Relationship to the images table (One-to-Many)
    images = relationship("Image", back_populates="user")

class Image(Base):
    __tablename__ ='images'
    image_id = Column(Integer,primary_key=True,autoincrement=True)
    len_watermark = Column(Integer)
    alpha = Column(Integer,nullable=False)
    hashed_text = Column(String,nullable=False)
    timestamp = Column(DateTime, default=datetime.now)


    # Foreign key linking to the User table
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    # Relationship to the User table (Many-to-One)
    user = relationship("User", back_populates="images")




Base.metadata.create_all(bind=engine)
session =sessionmaker()(bind=engine)
session.commit()

# Delete the image where image_id = 1
# x = session.query(Image).filter_by(image_id=1).delete()
# session.commit()
#AUTOINCREMENT
# session.query(Image).filter_by(image_id=2).update({Image.image_id: 1})
# session.commit()



#=====================================================
global watermarked_vertices

# Create a customized toggle switch
def on_toggle():
    if toggle_switch.get() == 1:
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
    else:
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green



top_frame4 = ctk.CTkFrame(master=app)
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

#=====================================================
# Create a tab view
tabview = ctk.CTkTabview(app,width=700,height=500)
tabview.pack(side='top', fill='both', expand=True, pady=(10, 0), padx=10)



tab_login = tabview.add("Login")
tab_login_label = ctk.CTkLabel(tab_login, text="Login",font=('helvetica',24))
tab_login_label.pack(pady=20,padx=20)

my_entry_username = ctk.CTkEntry(tab_login,placeholder_text="Username")
my_entry_username.pack(pady = 10)
my_entry_password = ctk.CTkEntry(tab_login,placeholder_text="Password",show='*')
my_entry_password.pack(pady = 10)
def log():
    user = session.query(User).filter_by(name=my_entry_username.get()).first()
    if user:
       
        if user.password == my_entry_password.get():
            tabview.delete("Login")
            tabview.delete("Register")
            print(Fore.GREEN +"logged in! Successfully")
            create_tab_embbed(user)
            create_tab_extract(user)
        else:
            return messagebox.showwarning("Login", "Wrong password!")

        
        return messagebox.showinfo("Login", "Your logged In!")
    else: 
        return messagebox.showwarning("Login", "This user doesn't exsit!")
tab1_button = ctk.CTkButton(tab_login, text="Submit", command=log)
tab1_button.pack(pady=20)

#=====================================================
tab_register = tabview.add("Register")
tab_register_label = ctk.CTkLabel(tab_register, text="Register",font=('helvetica',24))
tab_register_label.pack(pady=20,padx=20)

my_entry_username1 = ctk.CTkEntry(tab_register,placeholder_text="Username")
my_entry_username1.pack(pady = 10)
my_entry_email = ctk.CTkEntry(tab_register,placeholder_text="Email")
my_entry_email.pack(pady = 10)
my_entry_password1 = ctk.CTkEntry(tab_register,placeholder_text="Password",show='*')
my_entry_password1.pack(pady = 10)

def register():
    if my_entry_username1 != "" and my_entry_password1 != "":
        the_name = my_entry_username1.get()
        the_email = my_entry_email.get()
        the_password = my_entry_password1.get()
        print(f"the name {the_name} the email {the_email}  the password {the_password}")
        try:
            new_user = User(name=the_name,email=the_email,password=the_password)
            session.add(new_user)
            session.commit()
            return messagebox.showinfo("Register", "User Added Successfully!")
        except Exception as e:
            messagebox.showwarning("Problem", "there is a  problem") 

    else:
        messagebox.showwarning("Register", "There is something wrong!")

register_button = ctk.CTkButton(tab_register, text="Submit", command=register)
register_button.pack(pady=20)



#=====================================================
#=====================================================
def create_tab_embbed(user):


    tab_embbed = tabview.add("Embedd Watermark")
    tab_embbed_label = ctk.CTkLabel(tab_embbed, text=f"Hello {user.name}",font=('helvetica',24))
    tab_embbed_label.pack(pady=20)
    top_frame = ctk.CTkFrame(master=tab_embbed,width=160)
    top_frame.pack(side='top')






    watermark_entry = ctk.CTkEntry(top_frame,placeholder_text="The Watermark",width=160)
    watermark_entry.pack(side='top',pady=10,padx=10)

    
    # Function to open file explorer and get file/folder path
    def open_file_dialog():
        # Open a dialog to select a file
        file_path = filedialog.askopenfilename(title="Select a file", 
                                               filetypes=(("Image files", "*.obj;*.off"), ("All files", "*.*")))
        if file_path:
            # Display the selected file path
            
            label.configure(text=f"{file_path}")
            


    # Button to open file dialog
    file_button = ctk.CTkButton(top_frame, text="Select File", command=open_file_dialog,width=160)
    file_button.pack(side="top",pady=20,padx=10)




    
    # Label to display the selected path
    label = ctk.CTkLabel(top_frame, text="")
    label.pack(pady=10)
    def watermark_now():
        alpha = 0.1
        my_file_path = label.cget("text")
        watermark_text = watermark_entry.get()
        
        
        
        output_dct = "output/dct_embed_output.off"
        if my_file_path.endswith('.off'):
            print("off file")
            vertices, faces = dct.load_off_file(my_file_path)
            print(f"{Fore.GREEN}vertices and faces loaded Successfully")
        elif my_file_path.endswith('.obj'):
            print("obj file")
            output_transfer1 = "output/from_obj_to_off.off"
            oto.obj_to_off(my_file_path,output_transfer1)
            print(f"{Fore.GREEN}file transformed to off")
            vertices, faces = dct.load_off_file(output_transfer1)
            print(f"{Fore.GREEN}vertices and faces loaded Successfully")
        else:
            print('error')

        


        watermark = np.array([ord(char) / 255.0 for char in watermark_text])  # Normalize ASCII values
        # Embed watermark
        watermarked_vertices = dct.embed_watermark(vertices, watermark,alpha)
        dct.save_obj(watermarked_vertices, faces, output_dct)
        print(f"{Fore.GREEN}Watermark applied and saved to: {Fore.YELLOW}{output_dct}")
        # Extract watermark from the watermarked model
        extracted_watermark = dct.extract_watermark(watermarked_vertices, vertices,alpha,len(watermark_text))
        
        # Convert extracted watermark to characters
        extracted_watermark_text = ''.join([chr(int(value * 255)) for value in extracted_watermark])
        while (extracted_watermark_text != watermark_text):
            alpha += 0.1
            watermarked_vertices = dct.embed_watermark(vertices, watermark,alpha)
            dct.save_obj(watermarked_vertices, faces, output_dct)
            extracted_watermark = dct.extract_watermark(watermarked_vertices, vertices,alpha,len(watermark_text))
        
            # Convert extracted watermark to characters
            extracted_watermark_text = ''.join([chr(int(value * 255)) for value in extracted_watermark])
            print(f"alpha: {alpha} => {extracted_watermark_text}")

        print("Extracted Watermark:", extracted_watermark_text)
        alpha2 = round(alpha,1)
        pre_hash = str(alpha2)
        print(f"alpha is :{Fore.BLUE} {alpha2}")
        def hash_text(text):
            # Create a SHA-256 hash object
            sha256_hash = hashlib.sha256()
            
            # Encode the text to bytes and update the hash object
            sha256_hash.update(text.encode('utf-8'))
            
            # Get the hexadecimal representation of the hash
            hashed_text = sha256_hash.hexdigest()
            
            return hashed_text

        hashed_text = hash_text(pre_hash)
        the_len_of_watermark = len(watermark_text)
        try:
            new_image = Image(len_watermark=the_len_of_watermark,alpha=alpha2,hashed_text=hashed_text,user_id=user.user_id)
            session.add(new_image)
            session.commit()
            print(f"{Fore.GREEN}Image watermark for dct completed Successfully and saved")
        except Exception as e:
            print(f"{Fore.RED} {e}")
            return messagebox.showwarning("Register", "There is something wrong!")

        input_lsb ="output/this_the_output_after_dct.obj"
        the_result ="output/result.obj"
        oto.off_to_obj(output_dct,input_lsb)
        #accept obj only
        lsb.embed_watermark(input_lsb,the_result,hashed_text)
        
        messagebox.showinfo("Watermark", "watermark embedded Successfully!")

    # Button to open file dialog
    watermark_button = ctk.CTkButton(top_frame, text="Submit", command=watermark_now,width=160)
    watermark_button.pack(side="top",pady=20,padx=10)

    
    return print(f"{Fore.GREEN}Watermark Finished")



#=================================================================================
#=================================================================================





def create_tab_extract(user):


    tab_extract = tabview.add("Extract Watermark")
    tab_extract_label = ctk.CTkLabel(tab_extract, text=f"Hello {user.name}, wanna extract watermark?",font=('helvetica',18))
    tab_extract_label.pack(pady=5)
    # top_frame_extract = ctk.CTkFrame(master=tab_extract,width=160)
    # top_frame_extract.pack(side='top')

    # Create two frames
    frame1 = ctk.CTkFrame(tab_extract,fg_color="lightblue")
    frame1.pack(side="left", fill='both', expand=True, padx=10, pady=5)

    frame2 = ctk.CTkFrame(tab_extract, fg_color="lightgreen")
    frame2.pack(side="left", fill='both', expand=True, padx=10, pady=5)

    def open_file_dialog2():
    # Open a dialog to select a file
        file_path = filedialog.askopenfilename(title="Select a file", 
                                               filetypes=(("Image files", "*.obj;*.off"), ("All files", "*.*")))
        if file_path:
            # Display the selected file path
            
            label2.configure(text=f"{file_path}")
            
    def open_file_dialog3():
    # Open a dialog to select a file
        file_path = filedialog.askopenfilename(title="Select a file", 
                                               filetypes=(("Image files", "*.obj;*.off"), ("All files", "*.*")))
        if file_path:
            # Display the selected file path
            
            label3.configure(text=f"{file_path}")        

    # Button to open file dialog
    file_button2 = ctk.CTkButton(frame1, text="Suspected file", command=open_file_dialog2,width=160,fg_color="#4b4b4b")
    file_button2.pack(side="top",pady=10,padx=10)

    file_button_reference = ctk.CTkButton(frame1, text="Reference file", command=open_file_dialog3,width=160,fg_color="#4b4b4b" )
    file_button_reference.pack(side="top",pady=10,padx=10)


    
    # Label to display the selected path
    label2 = ctk.CTkLabel(frame1, text="")
    label2.pack(pady=0)

    label3 = ctk.CTkLabel(frame1, text="")
    label3.pack(pady=0)

    def extract_now():
        if label2.cget("text") == "":
            my_input_extraction = "output/result.obj"
        else:
            my_input_extraction = label2.cget("text")

        if label3.cget("text") == "":
            my_reference_extraction ="output/this_the_output_after_dct.obj"
        else:
            my_reference_extraction = label3.cget("text")
        extract_hash = lsb.extract_watermark(my_input_extraction,my_reference_extraction)
        image = session.query(Image).filter_by(hashed_text=extract_hash).first()
        if image :
            print(f"{Fore.YELLOW}image id => {image.image_id}\n userID => {image.user_id}")
            
            oto.obj_to_off(my_reference_extraction,'output/reference.off')
            vertices_normal, faces_normal = dct.load_off_file("output/reference.off")
            vertices_after, faces_after = dct.load_off_file("output/from_obj_to_off.off")
            my_length = int(image.len_watermark)
            alpha = image.alpha
            extract_result = dct.extract_watermark(vertices_normal,vertices_after,alpha,my_length)
            extracted_watermark_text = ''.join([chr(int(value * 255)) for value in extract_result])
            print(f"{Fore.RED} {extracted_watermark_text}")
            print(alpha,my_length)
    extract_button = ctk.CTkButton(frame1, text="Extract", command=extract_now,width=160,height=40,fg_color="#CC3333",hover_color="#5d1020")
    extract_button.pack(side="top",pady=20,padx=10)


    return print(f'hi')









#=================================================================================
#=================================================================================

# Start the application
app.mainloop()
