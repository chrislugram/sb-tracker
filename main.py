"""
This file contains the main function for the app
"""

# import pandas as pd
# import streamlit as st

from config.app_config import AppConfig
from logger import get_logger

# from storage.storage import Storage

# Create and configure logger
log = get_logger("main")

# Load app configuration
app_config = AppConfig("config.ini")

# # Load storage
# storage = Storage(config=app_config)
# storage.load_all()

# # Save storage
# storage.save_all()

################################################
# df_projects = pd.DataFrame(columns=["id", "name", "created_at", "description"])
# df_timetracks = pd.DataFrame(
#     columns=["id", "project_id", "created_at", "duration", "name", "description"]
# )
# df_tasks = pd.DataFrame(columns=["id", "task_name", "status", "project_id"])

# st.title("SB Tracker")

# # Creamos tres tabs
# tabs = st.tabs(["Proyectos", "Time Tracking", "Tareas"])

# # Pestaña Proyectos
# with tabs[0]:
#     project_form()

# # Pestaña Time Tracking
# with tabs[1]:
#     st.header("Time Tracking")
#     st.dataframe(df_timetracks)
#     # Aquí puedes añadir lógica para registrar tiempo

# # Pestaña Tareas
# with tabs[2]:
#     st.header("Tareas")
#     st.dataframe(df_tasks)
#     # Aquí puedes manejar tus tareas
