"""
This file contains the commons functions used by several components
"""

import streamlit as st

from definition.project import Project
from logger import get_logger
from storage.storage import Storage, StorageCollection

log = get_logger("commons")


def select_project(storage: Storage, key: str) -> Project:
    """
    Select project

    Args:
        storage (Storage): Storage

    Returns:
        Project: Project
    """
    st.subheader("Select project")

    project_df = storage.get(StorageCollection.projects)

    if project_df.empty:
        st.info("No projects found")
        return

    # Create selector of project
    project_selector = st.selectbox(
        "Select project", project_df["name"].values, key=key
    )

    # Get project
    row = project_df[project_df["name"] == project_selector].iloc[0]
    if row is not None:
        return Project(**row.to_dict())
    else:
        return None
