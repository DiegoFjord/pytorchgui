import tkinter as tk
import customtkinter as ctk

# this is a comment


def button_conf(butt: ctk.CTkButton):
    border_color = "#3d3d3d"
    fg_color = "#2c2c2c"
    hover_color = "#2d2d2d"

    butt.configure(
        border_width=2,
        border_color=border_color,
        fg_color=fg_color,
        hover_color=hover_color)


def radio_conf(rad: ctk.CTkRadioButton):
    rad.configure(
        fg_color="#3d3d3d",
        bg_color="#2c2c2c"
    )
