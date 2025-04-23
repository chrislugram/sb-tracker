"""
This file contains all the components for showing projects
"""

import uuid
from datetime import datetime

import streamlit as st

from definition.project import Project
from logger import get_logger
from storage.storage import Storage, StorageCollection

log = get_logger("project")


def tab_projects(storage: Storage):
    """
    Create tab for projects

    Args:
        storage (Storage): Storage
    """
    st.subheader("Add new project")
    project_form(storage)

    st.subheader("List of projects")
    project_list(storage)


def project_list(storage: Storage):
    """
    Show the project list

    Args:
        storage (Storage): Storage
    """
    project_df = storage.get(StorageCollection.projects)

    if project_df.empty:
        st.info("No projects found")
    else:
        st.dataframe(project_df, use_container_width=True)


def project_form(storage: Storage):
    """
    Show the project form

    Args:
        storage (Storage): Storage
    """
    with st.form("form_project"):
        # Input fields
        name = st.text_input("Project name", max_chars=100)
        description = st.text_area("Description", max_chars=1000)
        submitted = st.form_submit_button("Create project")

        if submitted:
            if name.strip() == "":
                st.warning("The project name cannot be empty.")
            else:
                new_project = Project(
                    id=str(uuid.uuid4()),
                    name=name,
                    description=description,
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

                # Save project
                storage.add_to_collection(StorageCollection.projects, new_project)

                st.success(f"Project '{name}' created.")
