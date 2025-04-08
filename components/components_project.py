"""
This file contains all the components for showing projects
"""

import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

from definition.project import Project
from storage.storage import Storage


def tab_projects(storage: Storage):
    """
    Create tab for projects

    Args:
        storage (Storage): Storage
    """
    st.subheader("Add new project")
    project_form(storage)

    # st.subheader("List of projects")
    # project_list(storage)


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
        submitted = st.form_submit_button("Save project")

        # Save project
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

                if "df_projects" not in st.session_state:
                    st.session_state.df_projects = pd.DataFrame(
                        columns=["id", "name", "created_at", "description"]
                    )

                st.session_state.df_projects = pd.concat(
                    [st.session_state.df_projects, pd.DataFrame([new_project])],
                    ignore_index=True,
                )

                st.success(f"Proyecto '{name}' añadido correctamente.")

    st.subheader("Lista de proyectos")

    if "df_projects" in st.session_state and not st.session_state.df_projects.empty:
        st.dataframe(
            st.session_state.df_projects.sort_values(by="created_at", ascending=False),
            use_container_width=True,
        )
    else:
        st.info("No hay proyectos creados aún.")
