import tkinter as tk
# for storing all tasks till i dont have backend
tasksArray=[]
# primitve method
def addTask(newTask):
    task = tk.Frame(root,bg="lightgray")

    taskName=tk.Label(task,text=newTask)
    taskName.pack(side="left",padx=5)

    doneBtn=tk.Button(task,text="done")
    upBtn=tk.Button(task,text="up")
    downBtn=tk.Button(task,text="down")
    delBtn=tk.Button(task,text="del")

    doneBtn.pack(side="left",padx=3,pady=2)
    upBtn.pack(side="left",padx=3,pady=2)
    downBtn.pack(side="left",padx=3,pady=2)
    delBtn.pack(side="left",padx=3,pady=2) 
    return task
    
class Task:
    def __init__(self, parent, text):
        self.frame = tk.Frame(parent)

        self.label = tk.Label(self.frame, text=text)
        self.label.pack(side="left")

        self.delete_btn = tk.Button(self.frame, text="X", command=self.delete)
        self.delete_btn.pack(side="right")

        self.details_btn=tk.Button(self.frame,text="details",command=self.details)

    def pack(self):
        self.frame.pack(fill="x")

    def delete(self):
        self.frame.destroy()
    def details(self):
        pass
#when addTask btn is clicked this func runs which adds the task to tasks section 
def handleAddTask():
    val = textInput.get("1.0", "end-1c")  # get text properly
    
    if val.strip() != "":
        tasksArray.append(Task(root,val))
        tasksArray[-1].pack()

    textInput.delete("1.0", "end")  # clear input

root=tk.Tk()
root.geometry('400x400')
textInput=tk.Text(root,height=10)
textInput.pack()
add=tk.Button(root,text="Add Task",command=handleAddTask, width=8, height=2, font=('Arial', 14))
add.pack()


root.mainloop()