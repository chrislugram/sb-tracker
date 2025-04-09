"""
This file contains the form that displays the project status
and allow add invoices and expenses
"""

from datetime import datetime

import streamlit as st

from config.app_config import AppConfig
from definition.expenses import Expense
from definition.invoice import Invoice
from definition.project import Project
from logger import get_logger
from storage.storage import Storage, StorageCollection

log = get_logger("project-status")


def tab_project_status(storage: Storage, app_config: AppConfig):
    """
    Create tab for project status

    Args:
        storage (Storage): Storage
    """
    st.subheader("Project status")

    selected_project = select_project(storage)

    st.markdown("---")

    if selected_project is not None:
        show_expenses(storage, selected_project)
        show_invoices(storage, selected_project)

        st.markdown("---")

        add_expense(storage, selected_project, app_config)
        add_invoice(storage, selected_project, app_config)


def select_project(storage: Storage) -> Project:
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
    project_selector = st.selectbox("Select project", project_df["name"].values)

    # Get project
    row = project_df[project_df["name"] == project_selector].iloc[0]
    if row is not None:
        log.info(f"Selected project {row}")
        return Project(**row.to_dict())
    else:
        return None


def show_expenses(storage: Storage, project: Project):
    """
    Show expenses for project

    Args:
        storage (Storage): Storage
        project (Project): Project
    """
    st.subheader("Expenses")

    # Get expenses
    expenses_df = storage.get(StorageCollection.expenses)

    # Filter expenses by project
    if expenses_df.empty:
        st.info("No expenses found")
    else:
        expenses_df = expenses_df[expenses_df["project"] == project.id]
        if expenses_df.empty:
            st.info("No expenses found")
        else:
            columns_name = Expense.get_column_names()
            columns_name.remove("project")
            st.dataframe(expenses_df[columns_name], use_container_width=True)


def show_invoices(storage: Storage, project: Project):
    """
    Show invoices for project

    Args:
        storage (Storage): Storage
        project (Project): Project
    """
    st.subheader("Invoices")

    # Get invoices
    invoices_df = storage.get(StorageCollection.invoices)

    # Filter invoices by project
    if invoices_df.empty:
        st.info("No invoices found")
    else:
        invoices_df = invoices_df[invoices_df["project"] == project.id]

        # Show invoices
        if invoices_df.empty:
            st.info("No expenses found")
        else:
            columns_name = Invoice.get_column_names()
            columns_name.remove("project")
            st.dataframe(invoices_df[columns_name], use_container_width=True)


def add_expense(storage: Storage, project: Project, app_config: AppConfig):
    """
    Add expense to project

    Args:
        storage (Storage): Storage
        project (Project): Project
        app_config (AppConfig): App config
    """
    st.subheader("Add expense")

    expense_types = [
        s.strip() for s in app_config.get("APPCONFIG", "expenses_types").split(",")
    ]

    with st.form("form_expense"):
        detail = st.text_input("Expense detail", max_chars=100)
        amount = st.number_input("Amount", min_value=0.0)
        type = st.selectbox("Expense type", options=expense_types)
        submitted = st.form_submit_button("Add expense")

        if submitted:
            if detail.strip() == "":
                st.warning("The expense name cannot be empty.")
            elif amount <= 0:
                st.warning("The expense amount must be greater than 0.")
            else:
                new_expense = Expense(
                    project=project.id,
                    type=type,
                    detail=detail,
                    amount=amount,
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

                # Save expense
                storage.add_to_collection(StorageCollection.expenses, new_expense)
                st.success(f"Expense '{detail}' created.")
                st.rerun()


def add_invoice(storage: Storage, project: Project, app_config: AppConfig):
    """
    Add invoice to project

    Args:
        storage (Storage): Storage
        project (Project): Project
        app_config (AppConfig): App config
    """
    st.subheader("Add invoice")

    invoice_platforms = [
        s.strip() for s in app_config.get("APPCONFIG", "invoices_platforms").split(",")
    ]

    with st.form("form_invoice"):
        platform = st.selectbox("Platform", options=invoice_platforms)
        sales = st.number_input("Sales", value=1)
        price = st.number_input("Price (€)", min_value=0.0)
        commision = st.slider("Commision", min_value=0, max_value=100, value=30)
        submitted = st.form_submit_button("Add invoice")

        if submitted:
            if sales <= 0:
                st.warning("The sales amount must be greater than 0.")
            elif price <= 0:
                st.warning("The price must be greater than 0.")
            else:
                new_invoice = Invoice(
                    project=project.id,
                    platform=platform,
                    sales=sales,
                    price=price,
                    commission=commision,
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

                # Save invoice
                storage.add_to_collection(StorageCollection.invoices, new_invoice)
                st.success("Invoice created.")
                st.rerun()
