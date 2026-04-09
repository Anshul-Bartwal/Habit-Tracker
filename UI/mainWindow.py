import tkinter as tk
# for storing all tasks till i dont have backend
habitsArray=[]
# primitve method

class Habit:
    def __init__(self, parent, text):
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
def handleAddHabit():
    val = textInput.get("1.0", "end-1c")  # get text properly
    
    if val.strip() != "":
        habitsArray.append(Habit(root,val))
        habitsArray[-1].pack()

    textInput.delete("1.0", "end")  # clear input

root=tk.Tk()
root.geometry('400x400')
streak_btn=tk.Button(root,text="Streaks",width=6,height=1)
streak_btn.pack()
textInput=tk.Text(root,height=10)
textInput.pack()
add=tk.Button(root,text="Add Habit",command=handleAddHabit, width=8, height=2, font=('Arial', 14))
add.pack()


root.mainloop()