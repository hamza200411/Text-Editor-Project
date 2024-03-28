import tkinter as tk
from tkinter import Tk
import customtkinter as ctk
from tkinter import messagebox
import tkinter.filedialog
import os
from tkinter import ttk
#--------------------------------------------------------------------------------
root = ctk.CTk()
root.title("Text Editor")
root.geometry("600x400")
f= font=("Poppins",15)
root.iconbitmap('icons/icon.ico')

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
#--------------------------------------------------------------------------------
new_file_icon = tk.PhotoImage(file='icons/new-file-48.png')
open_file_icon = tk.PhotoImage(file='icons/folder-48.png')
save_file_icon = tk.PhotoImage(file='icons/save-48.png')
save_as_file_icon = tk.PhotoImage(file='icons/save-as-48.png')
exit_file_icon = tk.PhotoImage(file='icons/exit-48.png')
undo_icon = tk.PhotoImage(file='icons/undo-48.png')
redo_icon = tk.PhotoImage(file='icons/redo-48.png')
cut_icon = tk.PhotoImage(file='icons/cut-48.png')
copy_icon = tk.PhotoImage(file='icons/copy-48.png')
paste_icon = tk.PhotoImage(file='icons/paste-48.png')
find_icon = tk.PhotoImage(file='icons/find-48.png')
select_all_icon = tk.PhotoImage(file='icons/select-all-48.png')
about_icon = tk.PhotoImage(file='icons/about-48.png')
help_icon = tk.PhotoImage(file='icons/help-48.png')
delete_icon = tk.PhotoImage(file='icons/clear-symbol-48.png')
font_icon = tk.PhotoImage(file='icons/font-48.png')

#--------------------------------------------------------------------------------
def about(event=None):
    messagebox.showinfo("About", "Text Editor Created at Networks Department \n Version 1.0")

def help(event=None):
    lst = [
            '<Ctrl+N> - New File', 
            '<Ctrl+O> - Open file',
            '<Ctrl-S> - Save file',
            '<Ctrl-Shift-S> - Save As',
            '', '<Ctrl-Z> - Undo',
            '<Ctrl-Y> - Redo', 
            '<Ctrl-X> - Cut text',
            '<Ctrl-C> - Copy text',
            '<Ctrl-V> - Paste text',
            '<Del> - Delete selected text',
            '<Ctrl-A> - Select all text',
            '', '<F1> - View shortcuts'
        ]
    messagebox.showinfo('Shortcut List', '\n'.join(lst))
        
def new_file(event=None):
  root.title("Untitled")
  global file_name
  file_name	= None
  content_text.delete(1.0,tk.END)	

def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w', encoding='utf-8') as the_file:
            the_file.write(content)
    except IOError:
        pass

def save_file(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"
            
def open_file(event=None):
    input_file_name = tk.filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), "Text Editor"))
        content_text.delete(1.0, tk.END)
        with open(file_name, encoding='utf-8') as _file:
            content_text.insert(1.0, _file.read())
               
def save_as_file(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(initialfile='Untitled',defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
    root.title('{} - {}'.format(os.path.basename(file_name), "Text Editor"))
    return "break"

def exit_file(event=None):
    if tk.messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def undo(event=None):
    content_text.event_generate("<<Undo>>")
    return 'break'

def	redo(event=None):
    content_text.event_generate("<<Redo>>")
    return	'break'
    
def cut(event=None):
    content_text.event_generate("<<Cut>>")
    return 'break'

def paste(event=None):
    content_text.event_generate("<<Paste>>")
    return 'break'

def copy(event=None):
    content_text.event_generate("<<Copy>>")
    return 'break'

def delete(event=None):
    content_text.event_generate("<Delete>")
    return 'break'

#--------------------------Find Text Toplevel------------------------------------------------------
def find_text(event=None):
    search_toplevel = tk.Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.iconbitmap("icons/icon.ico")
    
    def find():
        search_term = search_entry_widget.get()
        content_text.tag_remove('match', '1.0', tk.END)
        matches_found = 0
        if search_term:
            start_pos = '1.0'
            while True:
                start_pos = content_text.search(search_term, start_pos, stopindex=tk.END, nocase=ignore_case_value.get(), count=matches_found)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(search_term)}c'
                content_text.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
        content_text.tag_config('match', background='yellow',foreground="red")

    def close_search_window():
        content_text.tag_remove('match', '1.0', tk.END)
        search_toplevel.destroy()
        
    tk.Label(search_toplevel, text="Find All:",font=(f,15),width=4).grid(row=0, column=0, sticky='we')
    search_entry_widget = tk.Entry(search_toplevel, width=37,font=(f,14))
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='w')
    search_entry_widget.focus_set()
    ignore_case_value = tk.IntVar()
    search_button = tk.Button(search_toplevel, text="Find", command=find,font=(f,14),width=50,bg="#00ab6b")
    search_button.grid(row=2, column=0, padx=2, pady=2, sticky='w',columnspan=2)
    cancel_button = tk.Button(search_toplevel, text="Cancel", command=close_search_window,font=(f,14),width=50,bg="#f7786b")
    cancel_button.grid(row=3, column=0, padx=2, pady=2, sticky='w',columnspan=2)
    ignore_checkbtn = tk.Checkbutton(search_toplevel,text="ignore Case",variable=ignore_case_value,font=(f,14))
    ignore_checkbtn.grid(row=1,column=0, padx=6, pady=6, sticky='w')
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)

    
#--------------------------------------------------------------------------------
def select_all(event=None):
    content_text.tag_add('sel','1.0','end')
    return "break"
#--------------------------------Line Number-----------------------------------------------
def	update_line_numbers(event=None):
 line_numbers = get_line_numbers()
 line_number_bar.config(state='normal')
 line_number_bar.delete('1.0',	'end')
 line_number_bar.insert('1.0',	line_numbers)
 line_number_bar.config(state='disabled')
 
def on_content_changed(event=None):
   update_line_numbers()
   update_cursor_info_bar()
  
  
def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output

#----------------------------Highlight The Text------------------------------------------------------

def	highlight_line(interval=100):
 content_text.tag_remove("active_line",	1.0,"end")
 content_text.tag_add("active_line","insert	linestart",	"insert	lineend+1c")																																					
 content_text.after(interval, toggle_highlight)

def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")

def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()
      
#---------------------------------Show Cursor info-----------------------------------------------

def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()

def update_cursor_info_bar(event=None):
    row, col = content_text.index(tk.INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col)+1)
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)

#---------------------------Color Themes-----------------------------------------------------
color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}

def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.config(background=background_color, fg=foreground_color)
#----------------------------------------------------------------------------------
def	show_popup_menu(event):
 popup_menu.tk_popup(event.x_root,event.y_root)
#----------------------------------------------------------------------------------

def open_font_window():
    font_window = tk.Toplevel(root)
    font_window.title("Font")
    font_window.geometry("600x250")
    font_window.resizable(False, False)  # Disable window resizing
    font_window.configure(bg="#034f84")
    font_window.iconbitmap('icons/icon.ico')
    
    fonts = tk.font.families()
    
    font_scrollbar = tk.Scrollbar(font_window)
    font_scrollbar.pack(side='right', fill='y')
    
    font_listbox = tk.Listbox(font_window, font=("Poppins", 18), width=18, yscrollcommand=font_scrollbar.set)
    font_listbox.pack(side='left', fill='both', expand=True)
    
    font_scrollbar.config(command=font_listbox.yview)
    
    for font in fonts:
        font_listbox.insert(tk.END, font)
    
    def select_font():
        selected_font = font_listbox.get(font_listbox.curselection())
        content_text.config(font=(selected_font, font_size.get()))  # Apply the selected font and size to content_text
        
    select_button = tk.Button(font_window, text="Select", command=select_font, font=("Poppins", 15), width=6,bg="#c94c4c",fg="#fff")
    select_button.pack(side='left', pady=10, padx=8)
    
    font_size_label = tk.Label(font_window, text="Font Size:", font=("Poppins", 18),fg="#c94c4c")
    font_size_label.pack(side='left', pady=10, padx=5)
    
    font_size = tk.IntVar()
    font_size.set(18)
    
    font_size_spinbox = tk.Spinbox(font_window, from_=16, to=100, textvariable=font_size, width=15, font=("Poppins", 18))
    font_size_spinbox.pack(side='left', pady=10, padx=5)

#-----------------------Menu Bar---------------------------------------------------------
themes_menu = tk.Menu(menu_bar, tearoff=0, font=f, background="#fff", activebackground="#bfd7ea", activeforeground="black")
file_menu = tk.Menu(menu_bar, tearoff=0, font=f, background="#fff", activebackground="#bfd7ea", activeforeground="black")
edit_menu = tk.Menu(menu_bar, tearoff=0,font=f,background="#fff",activebackground="#bfd7ea",activeforeground="black")
view_menu = tk.Menu(menu_bar, tearoff=0,font=f,background="#fff",activebackground="#bfd7ea",activeforeground="black")
about_menu = tk.Menu(menu_bar, tearoff=0,font=f,background="#fff",activebackground="#bfd7ea",activeforeground="black")

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
menu_bar.add_cascade(label='View', menu=view_menu)
menu_bar.add_cascade(label='About', menu=about_menu)

file_menu.add_command(label='New', accelerator='Ctrl+N',command=new_file, image=new_file_icon, compound='left', underline=0)
file_menu.add_separator()
file_menu.add_command(label='Open', accelerator='Ctrl+O',command=open_file,image=open_file_icon,compound='left', underline=0)
file_menu.add_command(label='Save', accelerator='Ctrl+S',command=save_file,image=save_file_icon,compound='left', underline=0)
file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S',command=save_as_file,image=save_as_file_icon,compound='left', underline=0)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='AlT+F4',command=exit_file,image=exit_file_icon,compound='left', underline=0)

edit_menu.add_command(label='Undo', accelerator='Ctrl+Z',command=undo,image=undo_icon,compound='left', underline=0)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y',command=redo,image=redo_icon,compound='left', underline=0)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X',image=cut_icon,compound='left', underline=0)
edit_menu.add_command(label='Copy', accelerator='Ctrl+C',image=copy_icon,compound='left', underline=0)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V',image=paste_icon,compound='left', underline=0)
edit_menu.add_separator()
edit_menu.add_command(label='Find', accelerator='Ctrl+F',command=find_text,image=find_icon,compound='left', underline=0)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', accelerator='Ctrl+A',command=select_all,image=select_all_icon,compound='left', underline=0)
edit_menu.add_separator()
edit_menu.add_command(label="Change Font", image=font_icon, command=open_font_window,compound='left')

show_line_number = tk.IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_number)

show_cursor_info = tk.BooleanVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label="Show Cursor Location at Bottom",command=show_cursor_info_bar,variable=show_cursor_info, onvalue=1, offvalue=0)

to_highlight_line = tk.BooleanVar()
view_menu.add_checkbutton(label="Highlight Current Line",command=highlight_line,variable=to_highlight_line, onvalue=1, offvalue=0)

view_menu.add_cascade(label="Themes", menu=themes_menu)
theme_choice = tk.StringVar()
themes_menu.add_radiobutton(label="Default", variable=theme_choice, command=change_theme)
themes_menu.add_radiobutton(label="Greygarious", variable=theme_choice, command=change_theme)
themes_menu.add_radiobutton(label="Aquamarine", variable=theme_choice, command=change_theme)
themes_menu.add_radiobutton(label="Bold Beige", variable=theme_choice, command=change_theme)
themes_menu.add_radiobutton(label="Cobalt Blue", variable=theme_choice, command=change_theme)
themes_menu.add_radiobutton(label="Olive Green", variable=theme_choice, command=change_theme)
themes_menu.add_radiobutton(label="Night Mode", variable=theme_choice, command=change_theme)

about_menu.add_command(label='About',command=about,image=about_icon,compound='left', underline=0)
about_menu.add_separator()
about_menu.add_command(label='Help',command=help,image=help_icon,compound='left', underline=0)
#-----------------------Shortcut Bar---------------------------------------------------------
shortcut_bar = tk.Frame(root, height=45, background='#fff')
shortcut_bar.pack(expand='no', fill='x')

new_file_button = tk.Button(shortcut_bar, image=new_file_icon, command=new_file)
new_file_button.pack(side='left', padx=2, pady=2)
open_file_button = tk.Button(shortcut_bar, image=open_file_icon, command=open_file)
open_file_button.pack(side='left', padx=2, pady=2)
save_file_button = tk.Button(shortcut_bar, image=save_file_icon, command=save_file)
save_file_button.pack(side='left', padx=2, pady=2)
save_as_file_button = tk.Button(shortcut_bar, image=save_as_file_icon, command=save_as_file)
save_as_file_button.pack(side='left', padx=2, pady=2)
exit_file_button = tk.Button(shortcut_bar, image=exit_file_icon, command=exit_file)
exit_file_button.pack(side='left', padx=2, pady=2)
undo_button = tk.Button(shortcut_bar, image=undo_icon, command=undo)
undo_button.pack(side='left', padx=2, pady=2)
redo_button = tk.Button(shortcut_bar, image=redo_icon, command=redo)
redo_button.pack(side='left', padx=2, pady=2)
cut_button = tk.Button(shortcut_bar, image=cut_icon, command=cut)
cut_button.pack(side='left', padx=2, pady=2)
copy_button = tk.Button(shortcut_bar, image=copy_icon, command=copy)
copy_button.pack(side='left', padx=2, pady=2)
paste_button = tk.Button(shortcut_bar, image=paste_icon, command=paste)
paste_button.pack(side='left', padx=2, pady=2)
find_button = tk.Button(shortcut_bar, image=find_icon, command=find_text)
find_button.pack(side='left', padx=2, pady=2)
select_all_button = tk.Button(shortcut_bar, image=select_all_icon, command=select_all)
select_all_button.pack(side='left', padx=2, pady=2)
delete_button = tk.Button(shortcut_bar, image=delete_icon, command=delete)
delete_button.pack(side='left', padx=2, pady=2)

#--------------------------------------------------------------------------------

line_number_bar = tk.Text(root, width=3, padx=3, takefocus=0, border=0, background='#284b63', fg="#6fffe9", state='disabled', wrap='none',font=("tajawal",22))
line_number_bar.pack(side='left', fill='y')

content_text = tk.Text(root, wrap='word',undo=1, selectbackground='#3e5c76',font=("tajawal",23))
content_text.pack(expand='yes', fill='both')
scroll_bar = tk.Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')

content_text.tag_configure('active_line',background='ivory2')

cursor_info_bar	= tk.Label(content_text,text='Line:1|Column:1',font=(f,18))
cursor_info_bar.pack(expand='NO', fill=None, side='right', anchor='se')

#--------------------------------------------------------------------------------
popup_menu = tk.Menu(content_text)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd,font=(f))
popup_menu.add_separator() # يضيف خط فاصل
popup_menu.add_command(label='Select All', underline=1, command=select_all,font=(f))
#--------------------------------------------------------------------------------
# The following code lines are key bindings

content_text.bind('<Control-n>',new_file)
content_text.bind('<Control-N>',new_file)
content_text.bind('<Control-s>',save_file)
content_text.bind('<Control-S>',save_file)
content_text.bind('<Control-a>',select_all)
content_text.bind('<Control-o>',open_file)
content_text.bind('<Control-O>',open_file)
content_text.bind('<Control-y>',redo)
content_text.bind('<Control-Y>',redo)
content_text.bind('<Control-z>',undo)
content_text.bind('<Control-f>',find_text)
content_text.bind('<Control-F>',find_text)
content_text.bind('<Shift-Control-s>',save_as_file)
content_text.bind('<Shift-Control-S>',save_as_file)
content_text.bind('<Alt-F4>',exit_file)
content_text.bind('<Control-x>',cut)
content_text.bind('<Control-c>',copy)
content_text.bind('<Control-v>',paste)
content_text.bind('<Any-KeyPress>',	on_content_changed)
content_text.bind('<Button-3>',	show_popup_menu)	
content_text.bind('<F1>',help)
#--------------------------------------------------------------------------------
root.protocol('WM_DELETE_WINDOW',exit_file)  

root.mainloop()