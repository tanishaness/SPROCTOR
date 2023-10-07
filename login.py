import tkinter as tk
from tkinter import PhotoImage
def login():
    print("Login button clicked")
def signup():
    print("Signup button clicked")

root = tk.Tk()
root.title("SPROCTOR")


photo=PhotoImage(file="C:\\Users\\words\\Downloads\\sodapdf-converted.png")
photo=photo.zoom(2)
label=tk.Label(root,image=photo)
label.pack()

w=tk.Label(root,text="S-PROCTOR",font=("Arial",70))
w.pack()
login_button = tk.Button(root, text="Login", command=login,width=10,height=1,bg="light blue",font=("Arial",30))
login_button.place(x=500,y=600)

signup_button = tk.Button(root, text="Signup", command=signup,width=10,height=1,bg="light blue",font=("Arial",30))
signup_button.place(x=1000,y=600)


root.mainloop()