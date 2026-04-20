import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import ttk

from db import *
# --- CONSTANTS
WINDOW_SIZE="900x600"
BG_COLOR="#ecf1f6"
TAB_FONT=("Arial",11)
class AnalyticsWindow(tk.Toplevel):
    def __init__(self,parent:tk.Tk) -> None: 
        super().__init__(parent)
        self.title="Analytics Window"
        self.geometry(WINDOW_SIZE)
        self.config(bg=BG_COLOR)

        # self.habits: list = load_habits()
        # test data till the issu with backend doesnt gets fixed
        self.habits=[{
                "_id":"69e36c2a5bcbc073021a0a7f",
                "name":"something somethng",
                "days":64,
                "start_date":"2026-04-18",
                "logs":{},
                'current_streak':0,
                "longest_streak":0,}]
        self.df: pd.DataFrame = self._prepare_data()

        self._build_notebook()
    def _prepare_data(self) -> pd.DataFrame:
        '''Converts raw mongo data into pandas DataFrame
        makes data in rows format like
        habitname| date | checked |weekday | streak
        '''
        rows=[]
        for habit in self.habits:
            for date_str,checked in (habit.get('logs')).items():
                rows.append({
                    "habit_name":habit['name'],
                    "date":pd.to_datetime(date_str),
                    "checked":checked,
                    "weekday":pd.to_datetime(date_str).strftime("%A"),
                    "longest_streak":habit.get('longest_streak',0)
                })
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows)
    def _build_notebook(self) -> None:
        notebook=ttk.Notebook(self)
        notebook.pack(fill='x',expand=True,padx=10,pady=10)

        # tabs for notebook 
        tabs=[
            ("HeatMap",self._build_heatmap),
            ("Trend",self._build_trend),
            ("Streak",self._build_streak_comparision),
            ("Day of the week",self._build_day_of_the_week),
        ]

        # building the tabs

        for label,builder in tabs:
            frame=tk.Frame(notebook,bg=BG_COLOR)
            notebook.add(frame,text=label)
            if self.df.empty:
                self._build_empty_state(frame)
            else:
                builder(frame)

    def _build_empty_state(self,parent: tk.Frame):
        """Shows a friendly message when no data exists."""
        tk.Label(parent, text="No habit data yet.\nStart checking off some days!",
                 font=("Arial", 14), bg=BG_COLOR, fg="#9ca3af").pack(expand=True)

        
    def _build_heatmap(self,parent: tk.Frame):
        """Github style heatmap"""
        
        pass

    def _build_trend(self,parent: tk.Frame):
        """Line chart showing completion trends overtime"""
        pass

    def _build_streak_comparision(self,parent: tk.Frame):
        """Bar chart comparing longest streaks across habits"""
        pass

    def _build_day_of_the_week(self,parent: tk.Frame):
        """Bar chart showing on which days you do most habits"""
        pass