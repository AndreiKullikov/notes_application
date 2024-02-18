from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import subprocess

def choose_notes_folder():
    global notes_folder_path
    notes_folder_path = filedialog.askdirectory(title='Выберите папку для сохранения заметок')
    if not notes_folder_path:
        notes_folder_path = r"\notes_application\документы\заметки"  # Путь по умолчанию
    else:
        notes_folder_path = os.path.join(notes_folder_path, 'заметки')
        os.makedirs(notes_folder_path, exist_ok=True)

def chenge_theme(theme):
    text_fild['bg'] = view_colors[theme]['text_bg']
    text_fild['fg'] = view_colors[theme]['text_fg']
    text_fild['insertbackground'] = view_colors[theme]['cursor']
    text_fild['selectbackground'] = view_colors[theme]['select_bg']


def notepad_exit():
    answr = messagebox.askokcancel("выход", "Вы точно хотите выйти?")
    if answr:
        root.destroy()


def delete_note():
    file_path = filedialog.askopenfilename(
        initialdir=notes_folder_path,
        title='Выбор файла для удаления',
        filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*'))
    )

    if file_path:
        try:
            os.remove(file_path)
            messagebox.showinfo("Успех", "Заметка успешно удалена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить заметку: {str(e)}")


def open_file():
    file_path = filedialog.askopenfilename(title='Выбор файла', filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
    if file_path:
        text_fild.delete('1.0', END)
        text_fild.insert('1.0', open(file_path, encoding='utf-8').read())





def save_file():
    if not os.path.exists(notes_folder_path):
        os.makedirs(notes_folder_path)

    file_path = filedialog.asksaveasfilename(
        initialdir=notes_folder_path,
        filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*'))
    )

    if file_path:
        if not file_path.endswith('.txt'):
            file_path += '.txt'

        with open(file_path, 'w', encoding='utf-8') as file:
            text = text_fild.get('1.0', 'end-1c')
            file.write(text)

def show_all_notes():
    full_path = os.path.abspath(notes_folder_path)
    if os.path.exists(full_path):
        subprocess.Popen(["explorer", full_path])  # Открывает папку в стандартном файловом менеджере
    else:
        messagebox.showinfo("Ошибка", "Папка с заметками не найдена.")


root = Tk()
root.title("Notes")
root.geometry("500x500")
root.resizable(0,0)
root.iconbitmap("icon.ico")

main_menu = Menu(root)

# Файл
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Открыть', command=open_file)
file_menu.add_separator() # Полоска в меню
file_menu.add_command(label='Сохранить', command=save_file)
file_menu.add_separator() # Полоска в меню
file_menu.add_command(label='Закрыть', command=notepad_exit)
root.config(menu=file_menu)

# Вид

view_menu = Menu(main_menu, tearoff=0)
view_menu_sub = Menu(view_menu, tearoff=0)
font_menu_sub = Menu(view_menu, tearoff=0)
view_menu.add_cascade(label='Тёмная', command=lambda: chenge_theme("dark"))
view_menu.add_separator() # Полоска в меню
view_menu.add_cascade(label='Светлая', command=lambda: chenge_theme("light"))
root.config(menu=view_menu)

# Добавление списков меню
main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Тема', menu=view_menu)
main_menu.add_cascade(label='Показать все заметки', command=show_all_notes)
main_menu.add_cascade(label='Удалить заметку', command=delete_note)
root.config(menu=main_menu)

f_text = Frame(root)
f_text.pack(fill=BOTH, expand=1)

view_colors = {
     "dark":{
         'text_bg':"gray", "text_fg":"white","cursor":"violet", "select_bg":"blue"
     },
     'light': {
        'text_bg': 'white', 'text_fg': 'black', 'cursor': '#A5A5A5', 'select_bg': '#FAEEDD'
    }
}

text_fild = Text(f_text,
                 bg="gray",
                 fg="white",
                 padx=20,
                 pady=10,
                 wrap=WORD,
                 insertbackground="violet",
                 selectbackground="blue",
                 spacing3=10,
                 width=30)

text_fild.pack(expand=1,fill=BOTH, side=LEFT)

scroll=Scrollbar(f_text,command=text_fild.yview)
scroll.pack(side=LEFT, fill=Y)
text_fild.config(yscrollcommand=scroll.set)

choose_notes_folder()
root.mainloop()