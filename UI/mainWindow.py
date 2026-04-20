import tkinter as tk
from tkinter import ttk
from datetime import date,timedelta
import threading 

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import save_habit,load_habits,update_check,delete_habit 
from analytics import AnalyticsWindow

class HabitCard(tk.Frame):
    def __init__(self,parent,text,days,habit_id):
        super().__init__(parent,background="#ffffff",bd=1,relief='solid',padx=10,pady=8)
        self.text=text
        self.days=days
        self.start_date=date.today()
        self.habit_id=habit_id

        self._on_delete=self._delete()



        self.checkVar={}
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

        cols=50

        today=date.today()
        for i in range (self.days):
            day=self.start_date+timedelta(days=i)
            key=day.isoformat()
            var=tk.BooleanVar()
            self.checkVar[key]=var
            row,col=divmod(i,cols)
            cb=tk.Checkbutton(inner,variable=var,
                              bg="#ffffff",
                              activebackground="#d1fae5",
                              selectcolor="#51ff32",command=lambda k=key,v=var:self._oncheck(k,v.get()))
            cb.grid(row=row,column=col)
            if day > today:
                cb.configure(state='disabled')
        inner.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    def _refresh_ui(self):
        done=sum(v.get() for v in self.checkVar.values())
        self.progress_bar["value"]=done
        self.progress_label.config(text=f"{done}/{self.days}")
        streak=self._calc_streak()
        self.streak_label.config(text=f' {streak} days Streak')

    def _oncheck(self,dateStr,checked):
        # datesr and checked are only used for saveing so if want to refresh the UI  we can just pass None None :)
        # so instead we can just transfer the refesh ui code into a new function
        self._refresh_ui()
        def save():
            if self.habit_id is None:
                return
            update_check(habit_id=self.habit_id,date_str=dateStr,checked=checked,days=self.days)
        threading.Thread(target=save,daemon=True).start()
    
    def _calc_streak(self):
        today = date.today()
        streak = 0
        for i in range(self.days):
            d = today - timedelta(days=i)
            key = d.isoformat()
            if self.checkVar.get(key) and self.checkVar[key].get():
                streak += 1
            else:
                break
        return streak
    def _delete(self):
        def remove():
            if self.habit_id:
                delete_habit(self.habit_id)
        threading.Thread(target=self._delete,daemon=True).start()
        self.destroy()
class HabitTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("500x500")
        self.minsize(400,400)
        self._build_input_bar()
        self._build_Habits_Container()
        # self._load_prev_habits()

    
    def _build_input_bar (self):
        bar = tk.Frame(self, bg="#ffffff",bd=1, relief="solid",
                       padx=12, pady=10)
        bar.pack(fill="x", padx=12, pady=(12, 6))


        tk.Label(bar,text="Add a Habit",background="#ffffff").pack(anchor="w",pady=(0,8)) # pady=(top,bottom)
        tk.Button(bar,text="Analytics",command=self._open_analytics,cursor='hand2',relief='solid',bd=1).pack(pady=(8,0))
        input_row=tk.Frame(bar,bg="#ffffff")
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
        self.day_scale = tk.Scale(
                        days_row, orient="horizontal", from_=1, to=100,
                        variable=self.days_var, showvalue=False,
                        command=lambda v: self.days_label.config(
                            text=f"{v} Days", bg=self.handle_gradient(v))
                    )
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
    
    def _load_prev_habits(self):
        habits=load_habits()
        for habit in habits:
            habit_card=HabitCard(self.card_container,
                                 text=habit.get('name'),
                                 days=habit.get('days'),
                                 habit_id=habit.get('_id'))
            habit_card.pack(fill="x",pady=4)

            # for checkboxes
            logs=habit.get('logs',{})

            for date_str,checked in logs.items():
                if date_str in habit_card.checkVar and checked: # check if date in our checkvar ie range it has range from start day to end day date and if its checked from db
                    habit_card.checkVar[date_str].set(True)

            habit_card._refresh_ui()

    def _handle_add(self):
        habitText=self.name_entry.get()
        try:
            days=int(self.day_scale.get())
        except ValueError :
            days=10
        self.name_entry.delete(0,'end')
        if(habitText.strip() == ""):
            return
        card=HabitCard(self.card_container,habitText,days,habit_id=None)
        print(habitText)
        card.pack(fill="x", pady=4)
        self.name_entry.delete(0, "end")
        def save_in_background():
            print("starting to save in database")
            habit_id=save_habit(name=habitText,days=days)
            card.habit_id=habit_id
            print("Added in database")
        
        
        thread=threading.Thread(target=save_in_background)
        thread.daemon=True #if window closes the thread dies too
        thread.start()
        
    def handle_gradient(self,value,min_val=1,max_val=100):
        value=int(value)
        t = (value - min_val) / (max_val - min_val)  # 0.0 to 1.0
        r = int(234 * (1 - t) + 22 * t)
        g = int(179 * (1 - t) + 163 * t)
        b = int(8 * (1 - t) + 74 * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _open_analytics(self):
        AnalyticsWindow(self)
app=HabitTracker()
app.mainloop()

