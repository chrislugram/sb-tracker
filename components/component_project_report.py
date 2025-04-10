"""
This file contains the report for each project
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from config.app_config import AppConfig
from definition.project import Project
from logger import get_logger
from storage.storage import Storage, StorageCollection

log = get_logger("project-report")


def tab_project_report(
    storage: Storage, app_config: AppConfig, selected_project: Project
):
    """
    Create a report based on the info of the project
    """
    st.markdown("---")

    if selected_project is not None:
        # Prepare dataframes
        invoices_df = storage.get(StorageCollection.invoices)
        invoices = invoices_df[invoices_df["project"] == selected_project.id].copy()
        invoices["amount"] = (invoices["price"] * invoices["sales"]) * (
            1 - (invoices["commission"] / 100)
        )

        expenses_df = storage.get(StorageCollection.expenses)
        expenses = expenses_df[expenses_df["project"] == selected_project.id].copy()
        timetrack_df = storage.get(StorageCollection.timetrack)
        timetrack = timetrack_df[timetrack_df["project"] == selected_project.id].copy()

        all_expenses = unify_expenses(expenses, timetrack, app_config)

        # Ensure datetime
        invoices["created_at"] = pd.to_datetime(invoices["created_at"])
        all_expenses["created_at"] = pd.to_datetime(all_expenses["created_at"])

        # KPIs
        show_kpi(invoices, all_expenses)

        # Monthly trend
        show_monthly_trend(invoices, all_expenses)

        col1, col2 = st.columns(2)

        # Platform chart
        with col1:
            show_platform_chart(invoices)

        # Expenses by category
        with col2:
            show_expense_category(all_expenses)


def show_expense_category(expenses: pd.DataFrame):
    """
    Show barplot based in category expense

    Args:
        expenses (pd.DataFrame): expenses of the project
    """
    if "type" in expenses.columns:
        st.subheader("Expenses by Category")
        category_chart = expenses.groupby("type")["amount"].sum().reset_index()
        fig2 = px.pie(
            category_chart,
            names="type",
            values="amount",
            title="Expenses by Category",
        )
        st.plotly_chart(fig2, use_container_width=True)


def show_platform_chart(invoices: pd.DataFrame):
    """
    Show chart based in the platform

    Args:
        invoices (pd.DataFrame): All the invoices of the project
    """
    if "platform" in invoices.columns:
        st.subheader("Invoices by Platform")
        platform_chart = invoices.groupby("platform")["amount"].sum().reset_index()
        fig = px.pie(
            platform_chart,
            names="platform",
            values="amount",
            title="Revenue by Platform",
        )
        st.plotly_chart(fig, use_container_width=True)


# def show_expense_category(expenses: pd.DataFrame):
#     """
#     Show barplot based in category expense

#     Args:
#         expenses (pd.DataFrame): expenses of the project
#     """
#     if "type" in expenses.columns:
#         st.subheader("Expenses by Category")
#         category_chart = expenses.groupby("type")["amount"].sum().reset_index()
#         fig2 = px.bar(
#             category_chart, x="type", y="amount", title="Expenses by Category"
#         )
#         st.plotly_chart(fig2, use_container_width=True)


def show_monthly_trend(invoices: pd.DataFrame, expenses: pd.DataFrame):
    """
    Show monthly trend in the project

    Args:
        invoices (pd.DataFrame): All the invoices of the project
        expenses (pd.DataFrame): All the expenses of the project
    """
    st.subheader("Monthly Income and Expenses")
    income_by_month = invoices.groupby(invoices["created_at"].dt.to_period("M"))[
        "amount"
    ].sum()
    expense_by_month = expenses.groupby(expenses["created_at"].dt.to_period("M"))[
        "amount"
    ].sum()
    monthly_df = (
        pd.DataFrame({"Income": income_by_month, "Expenses": expense_by_month})
        .fillna(0)
        .sort_index()
    )
    st.line_chart(monthly_df)


def show_kpi(invoices: pd.DataFrame, expenses: pd.DataFrame):
    """
    Show general KPIs of the project

    Args:
        invoices (pd.DataFrame): All the invoices of the project
        expenses (pd.DataFrame): All the expenses of the project
    """
    st.subheader("KPIs")

    total_income = invoices["amount"].sum()
    total_expense = expenses["amount"].sum()
    net_profit = total_income - total_expense
    ticket_avg = invoices["amount"].mean() if not invoices.empty else 0
    roi = (net_profit / total_expense * 100) if total_expense > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"{total_income:.2f}")
    col2.metric("Total Expenses", f"{total_expense:.2f}")
    col3.metric("Net Profit", f"{net_profit:.2f}")

    col4, col5 = st.columns(2)
    col4.metric("Ticket Average", f"{ticket_avg:.2f}")
    col5.metric("ROI", f"{roi:.2f} %")

    st.markdown("---")


def unify_expenses(
    expenses: pd.DataFrame, timetrack: pd.DataFrame, app_config: AppConfig
) -> pd.DataFrame:
    """
    Unify in one dataframe (base in expenses)

    Args:
        expenses (pd.DataFrame): Expenses of the project
        timetrack (pd.DataFrame): Time expend in tasks of the project
        app_config (AppConfig): App config
    """

    # Prepare timetrack
    cost_per_hour = int(app_config.get(section="APPCONFIG", key="cost_per_hour"))
    timetrack_variation = pd.DataFrame(
        {
            "project": timetrack["project"],
            "type": timetrack["type"],
            "detail": timetrack["name"] + " - " + timetrack["description"],
            "amount": timetrack["duration"] * cost_per_hour,
        }
    )

    unified_df = pd.concat([expenses, timetrack_variation], ignore_index=True)
    print(f"unified_df.columns {unified_df.columns}")
    unified_df = unified_df[["type", "detail", "amount", "created_at"]].copy()
    return unified_df
