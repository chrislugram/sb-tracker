"""
This file contains the main function for the app
"""

import streamlit as st

from components.components_project import tab_projects
from components.components_project_status import tab_project_status
from config.app_config import AppConfig
from logger import get_logger
from storage.storage import Storage

# Create and configure logger
log = get_logger("main")

# Load app configuration
app_config = AppConfig("config.ini")

# Load storage
storage = Storage(config=app_config)
storage.load_all()

################################################

st.title("SB Tracker")

tabs = st.tabs(["Projects", "Project status"])

# Project
with tabs[0]:
    tab_projects(storage)

with tabs[1]:
    tab_project_status(storage, app_config)

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
