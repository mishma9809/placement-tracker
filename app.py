import streamlit as st
import pandas as pd
import altair as alt
from database import create_table, add_application, get_all_applications, delete_application, update_status, update_notes

create_table()

st.title("📋 Placement Application Tracker")

st.header("Add a new application")

with st.form("add_form"):
    company = st.text_input("Company")
    role = st.text_input("Role")
    location = st.text_input("Location")
    salary = st.text_input("Salary (e.g. £22,000)")
    date_applied = st.date_input("Date applied")
    status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add application")

    if submitted:
        add_application(company, role, location, salary, str(date_applied), status, notes)
        st.success(f"Added {role} at {company}!")
        st.rerun()

st.header("Dashboard")

rows = get_all_applications()

if rows:
    df = pd.DataFrame(rows, columns=["id", "company", "role", "location", "salary", "date_applied", "status", "notes"])

    status_counts = df["status"].value_counts()
    status_df = status_counts.reset_index()
    status_df.columns = ["status", "count"]

    color_map = {
        "Applied": "#1f77b4",
        "Interview": "#f1c40f",
        "Offer": "#2ecc71",
        "Rejected":"#e74c3c"
    }

    chart = alt.Chart(status_df).mark_bar().encode(
        x=alt.X("status", sort=None, title="Status"),
        y=alt.Y("count", title="Number of applications"),
        color=alt.Color("status", scale=alt.Scale(
            domain=list(color_map.keys()),
            range=list(color_map.values())
        ), legend=None)
    )

    st.altair_chart(chart, width="stretch")

    st.header("Your applications")

    filter_choice = st.selectbox("Filter by status", ["All", "Applied", "Interview", "Offer", "Rejected"])

    if filter_choice != "All":
        filtered_df = df[df["status"] == filter_choice]
    else:
        filtered_df = df

    for _, row in filtered_df.iterrows():
        with st.container(border=True):
            st.write(f"**{row['role']}** at **{row['company']}** ({row['location']})")
            if row['salary']:
                st.write(f" {row['salary']}")
            st.write(f"Applied: {row['date_applied']} | Status: {row['status']}")

            col1, col2 = st.columns(2)
            with col1:
                new_status = st.selectbox(
                    "Update status",
                    ["Applied", "Interview", "Offer", "Rejected"],
                    index=["Applied", "Interview", "Offer", "Rejected"].index(row['status']),
                    key=f"status_{row['id']}"
                )
                if new_status != row['status']:
                    update_status(row['id'], new_status)
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"delete_{row['id']}"):
                    delete_application(row['id'])
                    st.rerun()

            new_notes = st.text_area(
                "Notes",
                value=row['notes'] if row['notes'] else "",
                key=f"notes_{row['id']}"
            )
            if new_notes != row['notes']:
                if st.button("Save notes", key=f"save_notes_{row['id']}"):
                    update_notes(row['id'], new_notes)
                    st.rerun()
else:
    st.info("No applications yet. Add one above!")