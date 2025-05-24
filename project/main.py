import pandas as pd
from tkinter import *
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card={}

try:
    file=pd.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_file=pd.read_csv("french_words.csv")
    list_of_words=original_file.to_dict(orient="records")
else:
    list_of_words=file.to_dict(orient="records")#this parameter is very important to get a dict like {col->val}

def next_card():
    global current_card,flip_timer
    window.after_cancel(flip_timer)#stoping the timer of previous card which was still running
    current_card = random.choice(list_of_words)
    canvas.itemconfig(card_title,text="French",fill="black")
    canvas.itemconfig(card_word,text=current_card["French"],fill="black")
    canvas.itemconfig(card, image=front_image)

    flip_timer=window.after(3000,func=flip_card)#new flip timer for 3 sec after the button press

def flip_card():
    canvas.itemconfig(card_title,text="English",fill="white")
    canvas.itemconfig(card_word,text=current_card["English"],fill="white")
    canvas.itemconfig(card, image=back_image)

def is_known():
    list_of_words.remove(current_card)
    data=pd.DataFrame(list_of_words)
    data.to_csv("words_to_learn.csv",index=False) #index number will not be added again and again in data frame
    next_card()



#settting the screen
window=Tk()#this is a class
window.title("Flashy")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
flip_timer=window.after(3000, func=flip_card) #to make the first card change the side

#setting the images and text
canvas=Canvas(width=800,height=526,bg=BACKGROUND_COLOR,highlightthickness=0)
front_image=PhotoImage(file="card_front.png")
back_image = PhotoImage(file="card_back.png")

card=canvas.create_image(400, 263, image=front_image)
card_title=canvas.create_text(400,150,text="",font=("Ariel",30,"italic"))
card_word=canvas.create_text(400,263,text="",font=("Ariel",50,"bold"))
canvas.grid(row=0,column=0,columnspan=2)

#yes button
right_image=PhotoImage(file="right.png")
unknown_button=Button(image=right_image, command=is_known, highlightthickness=0, bg=BACKGROUND_COLOR)
unknown_button.grid(column=1, row=1)

#no button
wrong_image=PhotoImage(file="wrong.png")
known_button=Button(image=wrong_image, highlightthickness=0, command=next_card , bg=BACKGROUND_COLOR)
known_button.grid(column=0,row=1)

next_card()

window.mainloop()
