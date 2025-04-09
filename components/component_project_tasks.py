"""
This file contains the form taht display the task/time spend in projects
"""

from datetime import datetime

import streamlit as st

from config.app_config import AppConfig
from definition.project import Project
from definition.timetrack import Timetrack
from logger import get_logger
from storage.storage import Storage, StorageCollection

log = get_logger("project-tasks")


def tab_project_tasks(
    storage: Storage, app_config: AppConfig, selected_project: Project
):
    """
    Create tab for project tasks

    Args:
        storage (Storage): app storage
        app_config (AppConfig): app config
        selected_project (Project): Project selected for the tab
    """
    st.markdown("---")

    add_task(storage, selected_project)

    st.markdown("---")

    show_project_track(storage, selected_project)


def add_task(storage: Storage, project: Project):
    """
    Add task to the project's timetrack

    Args:
        storage (Storage): Storage
        project (Project): Project
    """
    st.subheader("Add task")

    with st.form("form_task"):
        name = st.text_input("Task", max_chars=100)
        description = st.text_input("Description", max_chars=1000)
        duration = st.number_input("Duration", min_value=0)
        submitted = st.form_submit_button("Add task")

        if submitted:
            if name.strip() == "":
                st.warning("The task need minimum a name.")
            elif duration <= 0:
                st.warning("The duration must be greater than 0.")
            else:
                new_timetrack = Timetrack(
                    project=project.id,
                    name=name,
                    description=description,
                    duration=duration,
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

                # Save timetrack
                storage.add_to_collection(StorageCollection.timetrack, new_timetrack)
                st.success("Task tracked added.")
                st.rerun()


def show_project_track(storage: Storage, project: Project):
    """
    Show timetrack for this project

    Args:
        storage (Storage): Storage
        project (Project): Project
    """
    st.subheader("Timetrack")

    timetrack_df = storage.get(StorageCollection.timetrack)

    if timetrack_df.empty:
        st.info("No tasks in this project.")
    else:
        timetrack_df = timetrack_df[timetrack_df["project"] == project.id]

        # show timetrack
        if timetrack_df.empty:
            st.info("No tasks in this project")
        else:
            columns_name = Timetrack.get_column_names()
            columns_name.remove("project")
            st.dataframe(timetrack_df[columns_name], use_container_width=True)
