import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.habits: list = load_habits()
        # test data till the issu with backend doesnt gets fixed
    #     self.habits=[
    #     {
    #         "name": "Morning Run",
    #         "days": 30,
    #         "start_date": "2026-03-22",
    #         "logs": {
    #             "2026-03-22": True,  "2026-03-23": True,  "2026-03-24": False,
    #             "2026-03-25": True,  "2026-03-26": True,  "2026-03-27": True,
    #             "2026-03-28": False, "2026-03-29": True,  "2026-03-30": True,
    #             "2026-03-31": True,  "2026-04-01": False, "2026-04-02": True,
    #             "2026-04-03": True,  "2026-04-04": True,  "2026-04-05": False,
    #             "2026-04-06": True,  "2026-04-07": True,  "2026-04-08": True,
    #             "2026-04-09": True,  "2026-04-10": False, "2026-04-11": True,
    #         },
    #         "current_streak": 4, "longest_streak": 5,
    #         "total_done": 16, "completion_rate": 76.0
    #     },
    #     {
    #         "name": "Read 20 pages",
    #         "days": 30,
    #         "start_date": "2026-03-22",
    #         "logs": {
    #             "2026-03-22": False, "2026-03-23": True,  "2026-03-24": True,
    #             "2026-03-25": False, "2026-03-26": True,  "2026-03-27": False,
    #             "2026-03-28": True,  "2026-03-29": False, "2026-03-30": True,
    #             "2026-03-31": True,  "2026-04-01": True,  "2026-04-02": False,
    #             "2026-04-03": True,  "2026-04-04": False, "2026-04-05": True,
    #             "2026-04-06": False, "2026-04-07": True,  "2026-04-08": True,
    #             "2026-04-09": False, "2026-04-10": True,  "2026-04-11": True,
    #         },
    #         "current_streak": 2, "longest_streak": 3,
    #         "total_done": 13, "completion_rate": 61.0
    #     },
    #     {
    #         "name": "Meditate",
    #         "days": 30,
    #         "start_date": "2026-03-22",
    #         "logs": {
    #             "2026-03-22": True,  "2026-03-23": True,  "2026-03-24": True,
    #             "2026-03-25": True,  "2026-03-26": False, "2026-03-27": True,
    #             "2026-03-28": True,  "2026-03-29": True,  "2026-03-30": False,
    #             "2026-03-31": True,  "2026-04-01": True,  "2026-04-02": True,
    #             "2026-04-03": False, "2026-04-04": True,  "2026-04-05": True,
    #             "2026-04-06": True,  "2026-04-07": False, "2026-04-08": True,
    #             "2026-04-09": True,  "2026-04-10": True,  "2026-04-11": True,
    #         },
    #         "current_streak": 4, "longest_streak": 6,
    #         "total_done": 17, "completion_rate": 80.0
    #     }
    # ]
        
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
            ("Streak",self._build_streak_comparison),
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
        daily = (self.df[self.df["checked"] == True]
                    .groupby("date")
                    .size()
                    .reset_index(name="count"))
        daily["date"] = pd.to_datetime(daily["date"])

        # build a full date range
        min_date = daily["date"].min()
        max_date = daily["date"].max()
        all_dates = pd.date_range(min_date, max_date)

        daily = daily.set_index("date").reindex(all_dates, fill_value=0)

        # build week x weekday grid
        weeks = []
        week = []
        start_dow = all_dates[0].weekday()  # monday=0

        # pad start
        for _ in range(start_dow):
            week.append(0)

        for val in daily["count"].values:
            week.append(val)
            if len(week) == 7:
                weeks.append(week)
                week = []

        if week:
            week += [0] * (7 - len(week))
            weeks.append(week)

        grid = np.array(weeks).T  # shape: (7, num_weeks)

        # ── draw chart ─────────────────────────────────────
        fig, ax = plt.subplots(figsize=(8, 3))
        fig.patch.set_facecolor(BG_COLOR)
        ax.set_facecolor(BG_COLOR)

        cmap = plt.cm.get_cmap("Greens")
        ax.imshow(grid, aspect="auto", cmap=cmap,
                interpolation="nearest", vmin=0, vmax=len(self.habits))

        ax.set_yticks(range(7))
        ax.set_yticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                            fontsize=9, color="#6b7280")
        ax.set_xticks([])
        ax.set_title("Daily Check-in Heatmap", fontsize=13,
                    pad=12, color="#111827")
        ax.tick_params(colors="#6b7280")
        for spine in ax.spines.values():
            spine.set_visible(False)

        # colorbar
        sm = plt.cm.ScalarMappable(cmap=cmap,
                                    norm=plt.Normalize(0, len(self.habits)))
        cbar = fig.colorbar(sm, ax=ax, orientation="horizontal",
                            pad=0.15, fraction=0.03)
        cbar.set_label("Habits completed", fontsize=9, color="#6b7280")
        cbar.ax.tick_params(colors="#6b7280", labelsize=8)

        # ── embed into tkinter ─────────────────────────────
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)
        


    def _build_trend(self,parent: tk.Frame):
        """Line chart showing completion trends overtime"""
         # ── data processing ────────────────────────────────
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor(BG_COLOR)
        ax.set_facecolor(BG_COLOR)

        colors = ["#6ee7b7", "#818cf8", "#fca5a5", "#fcd34d"]

        for idx, habit in enumerate(self.habits):
            habit_df = self.df[self.df["habit_name"] == habit["name"]].copy()
            habit_df = habit_df.sort_values("date")

            # rolling 7 day completion rate
            habit_df["rolling"] = (habit_df["checked"]
                                .astype(int)
                                .rolling(window=7, min_periods=1)
                                .mean() * 100)

            ax.plot(habit_df["date"], habit_df["rolling"],
                    label=habit["name"],
                    color=colors[idx % len(colors)],
                    linewidth=2, marker="o", markersize=3)

        ax.set_title("7-Day Rolling Completion Rate", fontsize=13,
                    pad=12, color="#111827")
        ax.set_ylabel("Completion %", color="#6b7280")
        ax.set_xlabel("Date", color="#6b7280")
        ax.set_ylim(0, 110)
        ax.tick_params(colors="#6b7280")
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(fontsize=10)
        fig.autofmt_xdate()

        # ── embed into tkinter ─────────────────────────────
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

    def _build_streak_comparison(self, parent: tk.Frame) -> None:
        """Bar chart comparing longest streaks across all habits."""

        # ── data processing ────────────────────────────────
        names = [h["name"] for h in self.habits]
        longest = [h.get("longest_streak", 0) for h in self.habits]
        current = [h.get("current_streak", 0) for h in self.habits]

        x = np.arange(len(names))
        width = 0.35

        # ── draw chart ─────────────────────────────────────
        fig, ax = plt.subplots(figsize=(8, 4),)
        fig.patch.set_facecolor(BG_COLOR)
        ax.set_facecolor(BG_COLOR)

        bars1 = ax.bar(x - width/2, longest, width,
                    label="Longest streak", color="#6ee7b7", edgecolor="#d1fae5")
        bars2 = ax.bar(x + width/2, current, width,
                    label="Current streak", color="#818cf8", edgecolor="#e0e7ff")

        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=10)
        ax.set_title("Streak Comparison", fontsize=13, pad=12, color="#111827")
        ax.set_ylabel("Days", color="#6b7280")
        ax.tick_params(colors="#6b7280")
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(fontsize=10)

        # ── embed into tkinter ─────────────────────────────
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

    def _build_day_of_the_week(self,parent: tk.Frame):
        """Bar chart showing on which days you do most habits"""
        #--- day processing
        day_order = ["Monday", "Tuesday", "Wednesday", 
                 "Thursday", "Friday", "Saturday", "Sunday"]
        
        day_counts=self.df[self.df["checked"]==True].groupby('weekday').size().reindex(day_order,fill_value=0)
        '''This line:

        Filters the DataFrame self.df to rows where checked is True.
        Groups the filtered data by the weekday column. 
        Counts the number of rows in each weekday group with .size(). 
        Reorders and fills the resulting Series to match the index order defined in day_order, inserting 0 for any weekday that is missing in the data using fill_value=0.
        '''

        # plotting
        fig,ax = plt.subplots(figsize=(8,4))  
        # makes a plot and retruns it into fig and also returns the axes so that we can plot using axes 
        # like if we want to add two subplots i can just do fig,(ax1,ax2) = ... ; ax1.bar() and ax2.bar() 
        bars=ax.bar(day_order,day_counts.values,color="#6ee7b7",edgecolor="#d1fae5", width=0.6)
        ax.set_facecolor(BG_COLOR)

        #highlight best day
        best_day=day_counts.values.argmax()
        bars[best_day].set_color("#059669")
        ax.set_title("Completions by Day of Week", 
                 fontsize=13, pad=12, color="#111827")
        ax.set_xlabel("Day", color="#6b7280")
        ax.set_ylabel("Completions", color="#6b7280")
        ax.tick_params(colors="#6b7280")
        ax.spines[["top", "right"]].set_visible(False)

        # ── embed into tkinter ─────────────────────────────
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

                                                         