import tkinter as tk
from tkinter import ttk
import time
# for storing all tasks till i dont have backend
habitsArray=[]
# primitve method

class Habit:
    def __init__(self, parent, text):
        self.text=text
        self.frame = tk.Frame(parent)

        self.label = tk.Label(self.frame, text=text)
        self.label.pack(side="left")

        self.delete_btn = tk.Button(self.frame, text="X", command=self.delete)
        self.delete_btn.pack(side="right")

        self.details_btn=tk.Button(self.frame,text="details",command=self.open_details)
        self.details_btn.pack(side='right')

    def pack(self):
        self.frame.pack(fill="x")

    def delete(self):
        self.frame.destroy()
    def open_details(self):
        details=tk.Toplevel(root)
        details.title(f"Habit: {self.text}")
        details.geometry('300x200')

        tk.Label(details, text="Details go here").pack(pady=20)
        # new details with graphs and all to come later till that time it is placeholder here

        details.grab_set() # make it so that input connects to this window and other windows go out of pur input scope
        details.transient(root) # appear above root
#when addHabit btn is clicked this func runs which adds the habit to habits section 
class Streak(Habit):
    def __init__(self, parent, text):
        super().__init__(parent, text)
class HabitCard(tk.Frame):
    def __init__(self,parent,text,days):
        super().__init__(parent,background="#ffffff",bd=1,relief='solid',padx=10,pady=8)
        self.text=text
        self.days=days
        self._build_header()
        self._build_progress_bar()
        self._build_checkboxes()
    def _build_header(self):
        header=tk.Frame(self,bg="#ffffff")
        header.pack(pady=(10,3))

        self.name_label=tk.Label(header,text=self.text, font=("Arial", 13, "bold"),
                                   bg="#f2e3e3", anchor="w")
        self.name_label.pack(side='left')
        # delete btn

        del_btn=tk.Button(header,text="×", font=("Arial", 12),
                            bg="#ffffff", relief="flat", cursor="hand2",
                            command=self.on_delete)
        del_btn.pack(side="right")

        # streak label
        self.streak_label=tk.Label(header,text="",font=("Arial", 10),
                                     fg="#b45309", bg="#fef3c7")
        self.streak_label.pack(side="right", padx=6)
    def _build_progress_bar(self):
        prog_frame=tk.Frame(self,bg="#fffff0")
        prog_frame.pack(fill='x',pady=(0,6))
        # for progress bar
        # we did self.progress bar and label so we can change ts anywhere inside the calss
        self.progress_bar=ttk.Progressbar(prog_frame,maximum=self.days,mode='determinate',length=300)
        self.progress_bar.pack(side='left',fill='x',expand=True)
        # for 0/10 days etc thing
        self.progress_label = tk.Label(prog_frame, text=f"0/{self.days}",
                                       font=("Arial", 10), fg="#6b7280", bg="#ffffff")
        self.progress_label.pack(side="left", padx=(8, 0))
    def _build_checkboxes(self):
        label=tk.Label(self,text=f"Day hi {self.days} Days :)")
        label.pack(fill='x')

        container=tk.Frame(self,bg="#ffffff")
        container.pack(fill='x')

        canvas=tk.Canvas(container,height=60)
        scrollbar= ttk.Scrollbar(container,orient="horizontal",command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side='bottom',fill='x')
        canvas.pack(side='top',fill='x')
        inner = tk.Frame(canvas, bg="#ffffff")
        canvas.create_window((0, 0), window=inner, anchor="nw")

        cols=20
        for i in range (self.days):
            row,col=divmod(i,cols)
            cb=tk.Checkbutton(inner,selectcolor="#51ff32")
            cb.grid(row=row,column=col)


    

    def on_delete(self):
        print("buh bye")
class HabitTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("500x500")
        self.minsize(400,400)
        self._build_input_bar()
        self._build_Habits_Container()
    
    def _build_input_bar (self):
        bar = tk.Frame(self, bg="#ffffff",bd=1, relief="solid",
                       padx=12, pady=10)
        bar.pack(fill="x", padx=12, pady=(12, 6))


        tk.Label(bar,text="Add a Habit",background="#ffffff").pack(anchor="w",pady=(0,8)) # pady=(top,bottom)
        input_row=tk.Label(bar,bg="#ffffff")
        input_row.pack(fill='x')
        # cuz we dont need inputrows in the child we didnt do it as self.input_row
        # -----------------------------we are inside input row---------------------------------
        #  
        self.name_entry=tk.Entry(input_row,bd=1,relief='solid')
        self.name_entry.pack(side='left',fill='x',expand=True,ipady=4)
        self.bind("<Return>",lambda e: self._handle_add())

        tk.Button(input_row,text="Add Habit",command=self._handle_add,cursor="hand2").pack(padx=(10,2))
        #slider :)
        days_row=tk.Frame(bar,background="#ffffff")
        days_row.pack(fill="x",pady=(6,3))
        
        tk.Label(days_row,text="Commitment",background="#ffffff",fg="#000000").pack()
        self.days_var=tk.IntVar(value=10)
        self.days_label=tk.Label(days_row,text="10-Days")
        self.days_label.pack()


        # scale/slider 1-100 doesnt show value changes the daysLabel according to days 
        self.day_scale=tk.Scale(days_row,orient="horizontal",from_=1,to=100,variable=self.days_var,showvalue="False",command=lambda v: self.days_label.config(text=f"{v} Days"))#,background=lambda v:self.handle_gradient(v)
        self.day_scale.pack(fill='x')
    def _build_Habits_Container(self): #scroll area
        # -----scroll section and canvas for all the habits section 
        wrapper=tk.Frame(self,bg="#d9fdff") 
        wrapper.pack(fill="both",expand=True,padx=12,pady=10)

        canvas=tk.Canvas(wrapper,bg="#f9f9f9")
        scrollBar=ttk.Scrollbar(wrapper,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=scrollBar.set)
        scrollBar.pack(side='right',fill='y')
        canvas.pack(side="left",fill='both',expand=True)
        # -----till here------
        # inside the canvas we will add a habit card container ie parent to habit card
        self.card_container=tk.Frame(canvas,bg="#f9f9f9")
 

        self._canvas_window = canvas.create_window(
                (0, 0), window=self.card_container, anchor="nw")

        self.card_container.bind("<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(
                self._canvas_window, width=e.width))

        self._canvas=canvas
    def _handle_add(self):
        habitText=self.name_entry.get()
        try:
            days=int(self.day_scale.get())
        except ValueError :
            days=10
        self.name_entry.delete(0,'end')
        if(habitText.strip() != ""):
            HabitCard(self.card_container,habitText,days).pack(fill='x')
            print(habitText)
    def handle_gradient(value,min_val=1,max_val=100):
        value=int(value)
        t = (value - min_val) / (max_val - min_val)  # 0.0 to 1.0
        r = int(234 * (1 - t) + 22 * t)
        g = int(179 * (1 - t) + 163 * t)
        b = int(8 * (1 - t) + 74 * t)
        return f"#{r:02x}{g:02x}{b:02x}"
def handleAddHabit():
    val = textInput.get("1.0", "end-1c")  # get text properly
    
    if val.strip() != "":
        habitsArray.append(Habit(root,val))
        habitsArray[-1].pack()

    textInput.delete("1.0", "end")  # clear input
def handleClickStreak():
    streakWindow=tk.Toplevel(root)
    streakWindow.title("Streaks")
    # was adding streak window lol
# a json type dict : 
'''for Habit object
    {taskName:{
        commitedTime:"time till which user has asked to commit the habit",
        timeElapsed:[days user has done the habit] #usefull for the checkboxes,
        streak:{
            currentStreak:currentStreak,
            longestStreak:longestStreak
            }
        },
        priority:updated using the btns (num and pri are directly proportional)



    }
'''
# root=tk.Tk()
# root.geometry('400x400')
# streak_btn=tk.Button(root,text="Streaks",width=6,height=1,command=handleClickStreak)
# streak_btn.pack()
# textInput=tk.Text(root,height=10)
# textInput.pack()
# add=tk.Button(root,text="Add Habit",command=handleAddHabit, width=8, height=2, font=('Arial', 14))
# add.pack()
app=HabitTracker()
app.mainloop()

