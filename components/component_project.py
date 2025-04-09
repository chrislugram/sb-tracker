"""
This file contains all the components for showing projects
"""

import uuid

import streamlit as st

from definition.project import Project
from storage.storage import Storage, StorageCollection


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
    st.subheader("Project list")

    df = storage.get(StorageCollection.projects)

    if not df.empty:
        edited_df = st.data_editor(df, num_rows="dynamic")
        if edited_df is not None:
            storage.set(StorageCollection.projects, edited_df)
    else:
        st.info("No projects found")


def project_form(storage: Storage):
    """
    Show the project form

    Args:
        storage (Storage): Storage
    """

    # df_projects = storage.get

    with st.form("form_project"):
        # Input fields
        name = st.text_input("Project name", max_chars=100)
        description = st.text_area("Description", max_chars=1000)
        submitted = st.form_submit_button("Create project")

        # Save project
        if submitted:
            if name.strip() == "":
                st.warning("The project name cannot be empty.")
            else:
                new_project = Project(
                    id=str(uuid.uuid4()), name=name, description=description
                )

                # Save project
                storage.add_to_collection(StorageCollection.projects, new_project)

                st.success(f"Project '{name}' created.")
