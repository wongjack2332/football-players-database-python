import customtkinter as ctk
import pandas as pd
import parse
from PIL import Image
import pandastable
from webbrowser import open

import databaseutils
import guiutils

BACKARROW_IMG = ctk.CTkImage(
    light_image=Image.open("img/backward.png"),
    dark_image=Image.open("img/backward.png"),
    size=(40, 40),
)
SEARCH_IMG = ctk.CTkImage(
    light_image=Image.open("img/magnifying_glass.png"),
    dark_image=Image.open("img/search-light.png"),
    size=(20, 20),
)


def home_page():
    new_button = ctk.CTkButton(
        master=frame,
        text="New",
        command=new_entry,
        font=("Roboto", 36),
        fg_color="green",
        hover_color="#0E4732",
    )
    search_button = ctk.CTkButton(
        master=frame, text="Search", command=player_search, font=("Roboto", 36)
    )
    new_button.pack(padx=50, pady=60, fill="both", expand=True)
    search_button.pack(padx=50, pady=60, fill="both", expand=True)
    rick_roll = ctk.CTkButton(
        master=frame,
        text="don't click me",
        command=lambda: open("https://wallpapercave.com/wp/wp9414303.jpg"),
        fg_color="red",
    )
    rick_roll.pack(pady=20)


def new_entry():
    guiutils.clear_frame(frame)
    create_entry_form()


def return_to_homepage():
    guiutils.clear_frame(frame)
    home_page()


def get_form_values(error_label, *args):
    attributes = []
    for i in args:
        val = i.get()
        if val == "" or val == "select card type":
            error_label.configure(text="empty attribute(s)", text_color="red")
            return
        attributes.append(val)

    error = databaseutils.player_entry(players_dict, *attributes)
    if error is not None:
        error_label.configure(text=error, text_color="red")
        return
    parse.dict_to_csv(players_dict, fields)
    error_label.configure(text="player created", text_color="green")


def reset_form(label, *args):
    label.configure(text="")
    args[0].set("select card type")
    for i in args[1:]:
        i.delete(0, "end")


def create_entry_form():
    """fields: card_type,lastname,firstname,team,speed,pass,shooting,tackling,control,GK,physical,heading"""
    back_arrow = ctk.CTkButton(
        master=frame, image=BACKARROW_IMG, text="", command=return_to_homepage
    )
    back_arrow.pack(side="top", anchor="w", padx=10, pady=10, fill="none")

    card_type_options = df.card_type.unique()
    combobox_card_type = ctk.CTkComboBox(master=frame, values=card_type_options)
    combobox_card_type.set("select card type")
    combobox_card_type.pack(padx=10, pady=10)

    entry_fields = []
    for i in fields[2:]:
        field = ctk.CTkEntry(master=frame, placeholder_text=i)
        field.pack(padx=10, pady=10)
        entry_fields.append(field)

    error_message = ctk.CTkLabel(master=frame, text="", text_color="red", font=("", 16))
    create_button = ctk.CTkButton(
        master=frame,
        text="Create",
        command=lambda: get_form_values(
            error_message, combobox_card_type, *entry_fields
        ),
        fg_color="green",
    )

    back_button = ctk.CTkButton(
        master=frame,
        text="Back",
        command=return_to_homepage,
        fg_color="grey",
        hover_color="black",
    )
    reset_button = ctk.CTkButton(
        master=frame,
        text="Reset",
        command=lambda: reset_form(error_message, combobox_card_type, *entry_fields),
        fg_color="red",
    )
    create_button.pack(padx=20, pady=5)
    back_button.pack(padx=20, pady=5)
    reset_button.pack(padx=20, pady=5)
    error_message.pack(padx=20, pady=20)


def search_for_player(entry, label):
    command = entry.get()
    string_dict = databaseutils.parse_search_command(command)

    result_df = databaseutils.player_search(df, True, **string_dict)
    label.configure(text=f"{str(result_df)}")


def player_search():
    guiutils.clear_frame(frame)
    searchbar_entry = ctk.CTkEntry(
        master=frame, placeholder_text="type name to search..."
    )
    search_icon = ctk.CTkButton(
        master=frame,
        text="Search",
        image=SEARCH_IMG,
        command=lambda: search_for_player(searchbar_entry, table_label),
    )
    searchbar_entry.place(relx=0.03, rely=0.01, relwidth=0.8)
    search_icon.place(relx=0.84, rely=0.01)

    scrollable_frame = ctk.CTkScrollableFrame(master=frame)
    table_label = ctk.CTkLabel(
        master=scrollable_frame,
        text=f"{str(df)}",
        justify="left",
        font=("courier new", 16),
    )
    scrollable_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)
    table_label.pack()

    get_search_value()


def get_search_value():
    pass


ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("system")

fields, players_dict = parse.csv_to_dict()
df = pd.DataFrame.from_dict(players_dict, columns=fields[1:], orient="index")

pd.set_option("display.max_column", 12)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

root = ctk.CTk()
root.geometry("1000x800")

frame = ctk.CTkFrame(master=root)
frame.pack(fill="both", expand=True)

home_page()

root.mainloop()
