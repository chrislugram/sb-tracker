"""
This file contains the main function for the app
"""

import streamlit as st

from components.commons import select_project
from components.component_project import tab_projects
from components.component_project_report import tab_project_report
from components.component_project_status import tab_project_status
from components.component_project_tasks import tab_project_tasks
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

tabs = st.tabs(["Projects", "Project status", "Project tasks", "Project report"])

# Project
with tabs[0]:
    tab_projects(storage)

with tabs[1]:
    st.subheader("Project status")
    selected_project = select_project(storage, "tab_1_select_project")
    tab_project_status(storage, app_config, selected_project)

with tabs[2]:
    st.subheader("Project time tracker")
    selected_project = select_project(storage, "tab_2_select_project")
    tab_project_tasks(storage, app_config, selected_project)

with tabs[3]:
    st.subheader("Project Report")
    selected_project = select_project(storage, "tab_3_select_project")
    tab_project_report(storage, app_config, selected_project)
