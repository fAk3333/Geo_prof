import time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from ary_funcs import *
import ezdxf
import re
from ezdxf.math import ConstructionArc
from dxf_work_funcs import *
import tkinter as tk
import os
import wmi


def callback():
    global name_of_file
    name_of_file = fd.askopenfilename()

def activate_start_button():
    name = name_of_prof_str.get()
    # vert = vert_scale_str.get()
    # horiz = horiz_scale_str.get()
    # min_otmetka = min_otmetka_str.get()

    #Проверка корректности поданных данных
    try:
        len(name_of_file)
    except:
        messagebox.showerror('Error', 'Вы не подали файл')
    #Проверяем файл на его формат и получаем списки: ПК, отметок, названий, угодий
    if '.txt' in name_of_file:
        try:
            piketi, otmetki_old, nazvaniya, ugod = txt_to_ary(name_of_file)
        except:
            messagebox.showerror('Error', 'Неверный файл')
    elif '.xlsx' in name_of_file:
        try:
            piketi, otmetki_old, nazvaniya, ugod = xlsx_to_ary(name_of_file)
        except:
            messagebox.showerror('Error', 'Неверный файл')
    else:
        messagebox.showerror('Error', 'Неверный файл')
    #Начнём работу программы
    #Для начала получим подкоректированные отметки и пикеты
    otmetki = scaling_otmetok(otmetki_old)

    piketi = scaling_piketov(piketi)

    #Можно начинать рисовать dxf
    prof_writer(name, piketi, otmetki, otmetki_old, nazvaniya, ugod)
    messagebox.showinfo('УУУРРРРААААА', 'Ваш профиль создан')


#General
root = Tk()
root.title('geo_prof')
root.geometry("397x142+600+400")
root.iconbitmap(default="icon.ico")

#varaibles
vert_scale_str = StringVar(value='1:100')
horiz_scale_str = StringVar(value='1:500')
name_of_prof_str = StringVar(value='PROF')
min_otmetka_str = StringVar(value='60')

#Text_fields
entry_of_vert_scale = ttk.Entry(textvariable=vert_scale_str, state='disabled')
entry_of_horiz_scale = ttk.Entry(textvariable=horiz_scale_str, state='disabled')
entry_of_name = ttk.Entry(textvariable=name_of_prof_str)
entry_of_min_otmetka = ttk.Entry(textvariable=min_otmetka_str, state='disabled')

#init
entry_of_name.grid(row=0, column=1)
entry_of_horiz_scale.grid(row=1, column=1)
entry_of_vert_scale.grid(row=2, column=1)
entry_of_min_otmetka.grid(row=3, column=1)

#labels
name_of_prof_label = ttk.Label(text='Название профиля:', font=('Arial', 15))
name_of_prof_label.grid(row=0, column=0)

horiz_scale_label = ttk.Label(text='Горизонтальный масштаб:', font=('Arial', 15))
horiz_scale_label.grid(row=1, column=0)

vert_scale_label = ttk.Label(text='Вертикальный масштаб:', font=('Arial', 15))
vert_scale_label.grid(row=2, column=0)

min_otmetka_label = ttk.Label(text='Минимальная ордината:', font=('Arial', 15))
min_otmetka_label.grid(row=3, column=0)

#Buttons
start_button = ttk.Button(text="Построить профиль", command=activate_start_button)
start_button.grid(row=4, column=1)

file_button = fd.Button(text='Выберите файл', command=callback).grid(row=4, column=0)

c = wmi.WMI()
logical_disks = {}
list_with_serials = []
for drive in c.Win32_DiskDrive():
    for partition in drive.associators("Win32_DiskDriveToDiskPartition"):
        for disk in partition.associators("Win32_LogicalDiskToPartition"):
            logical_disks[disk.Caption] = {"model": drive.Model, "serial": drive.SerialNumber}
            list_with_serials.append(drive.SerialNumber)

ser_num = '4162851270336448139'

if ser_num in list_with_serials:
    flag = 1
else:
    flag = 0

if flag:
    root.mainloop()
else:
    messagebox.showerror('Error', 'КЛЮЧ!!!')
    root.destroy()

