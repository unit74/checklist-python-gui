from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functools import partial


def load_tasks():
    tasks = []
    try:
        with open("checklist.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                status, task = line.strip().split(':', 1)
                tasks.append((task, status))
    except FileNotFoundError:
        pass
    return tasks


def save_tasks():
    with open("checklist.txt", "w") as file:
        for task, check_var, _, _, _ in todos:
            status = "checked" if check_var.get() == 1 else "unchecked"
            file.write(f"{status}:{task}\n")


def toggle_topmost():
    global topmost_flag
    topmost_flag = not topmost_flag
    win.attributes('-topmost', topmost_flag)

    if topmost_flag:
        topmost_button.config(image=unpin)
    else:
        topmost_button.config(image=pin)


def add(task=None, checked=False):
    global row
    label_text = todo.get() if task is None else task
    if not label_text:
        messagebox.showinfo("알림", "내용이 없습니다.")
        return

    label = Label(win, text=label_text, fg="black", bg="white")
    label.grid(column=col, row=row, sticky='w', padx=5, pady=2)

    check = IntVar(value=1 if checked else 0)
    cb = Checkbutton(win, image=unchecked, selectimage=checked_image, indicatoron=False,
                     onvalue=1, offvalue=0, variable=check)
    cb.grid(column=col + 1, row=row)

    del_button = Button(win, image=delete_image)  # changed from text to image
    del_button.grid(column=col + 2, row=row)
    del_button['command'] = partial(delete, label_text, check, label, cb, del_button)

    if task is None:
        todo.set("")

    todos.append((label_text, check, label, cb, del_button))
    row += 1


def delete(task_text, check, label, checkbtn, delbtn):
    # 위젯 파괴
    label.destroy()
    checkbtn.destroy()
    delbtn.destroy()

    # 리스트에서 작업 제거
    global todos
    todos = [(task, check_var, lbl, cb, btn) for task, check_var, lbl, cb, btn in todos if task != task_text]

    # 다음 작업들의 위치를 업데이트
    global row
    for idx, (_, _, lbl, cb, btn) in enumerate(todos):
        lbl.grid(row=2 + idx)
        cb.grid(row=2 + idx)
        btn.grid(row=2 + idx)

    # 다음 작업의 위치를 업데이트
    row = 2 + len(todos)


def adjust_transparency(value):
    win.attributes('-alpha', float(value))


def on_drag(event):
    x, y = win.winfo_pointerxy()
    win.geometry(f"+{x - offset_x}+{y - offset_y}")


def on_click(event):
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y


win = Tk()
win.configure(bg='white')  # Fixed the color name here

win.resizable(False, False)
win.overrideredirect(True)

col = 0
row = 2
todos = []
topmost_flag = False

checked_image = PhotoImage(file="images/checked.png").subsample(18, 18)
unchecked = PhotoImage(file="images/unchecked.png").subsample(18, 18)
delete_image = PhotoImage(file="images/delete.png").subsample(18, 18)
pin = PhotoImage(file="images/pin.png").subsample(18, 18)
unpin = PhotoImage(file="images/unpin.png").subsample(18, 18)

todo = StringVar()

titlebar = Frame(win, bg="#e0e0e0", relief=SOLID, bd=2)
titlebar.grid(row=0, columnspan=4, sticky="ew")

titlebar.bind("<Button-1>", on_click)
titlebar.bind("<B1-Motion>", on_drag)

title_label = Label(titlebar, text="Checklist for KKR", bg="#e0e0e0", fg="black", font=("Arial", 12, "bold"))
title_label.pack(pady=5)

close_btn = Button(titlebar, text="X", bg="#e0e0e0", fg="black", relief=FLAT, padx=10,
                   command=lambda: [save_tasks(), win.destroy()])
close_btn.pack(side=RIGHT, pady=5, padx=5)

for task, status in load_tasks():
    add(task, status == "checked")

textbox = ttk.Entry(win, width=20, textvariable=todo)
textbox.grid(column=0, row=1, sticky='w', padx=5, pady=5)
button = ttk.Button(win, text="Add todo", command=add)
button.grid(column=1, row=1)

transparency_slider = Scale(win, from_=0.1, to=1, resolution=0.01, orient=HORIZONTAL, command=adjust_transparency,
                            bg="white")
transparency_slider.set(1)
transparency_slider.grid(column=2, row=1, padx=10, sticky='se')


topmost_button = Button(win, image=pin, command=toggle_topmost, bg='white')
topmost_button.grid(column=3, row=1, sticky='w')

win.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), win.destroy()])

win.mainloop()
