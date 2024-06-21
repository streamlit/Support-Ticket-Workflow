from datetime import datetime

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Page title
st.set_page_config(page_title="Support ticket workflow", page_icon="🎫")
st.title("🎫 Support ticket workflow")
st.write(
    "This app shows an internal tool. The user can create support tickets at the top "
    "and check the status and statistics of tickets below."
)


# Generate data
## Set seed for reproducibility
np.random.seed(42)


## Function to generate a random issue description
def generate_issue():
    issues = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications",
    ]
    return np.random.choice(issues)


## Function to generate random dates
start_date = datetime(2023, 6, 1)
end_date = datetime(2023, 12, 20)
id_values = ["TICKET-{}".format(i) for i in range(1000, 1100)]
issue_list = [generate_issue() for _ in range(100)]


def generate_random_dates(start_date, end_date, id_values):
    date_range = pd.date_range(start_date, end_date).strftime("%m-%d-%Y")
    return np.random.choice(date_range, size=len(id_values), replace=False)


## Generate 100 rows of data
data = {
    "Issue": issue_list,
    "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
    "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
    "Date Submitted": generate_random_dates(start_date, end_date, id_values),
}
df = pd.DataFrame(data)
df.insert(0, "ID", id_values)
df = df.sort_values(by=["Status", "ID"], ascending=[False, False])

## Create DataFrame
if "df" not in st.session_state:
    st.session_state.df = df


# Sort dataframe
def sort_df():
    st.session_state.df = edited_df.copy().sort_values(
        by=["Status", "ID"], ascending=[False, False]
    )


# Tabs for app layout

recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])

st.header("Add a ticket")
with st.form("addition"):
    issue = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submit = st.form_submit_button("Submit")

if submit:
    today_date = datetime.now().strftime("%m-%d-%Y")
    df2 = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Issue": issue,
                "Status": "Open",
                "Priority": priority,
                "Date Submitted": today_date,
            }
        ]
    )
    st.write("Ticket submitted!")
    st.dataframe(df2, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([st.session_state.df, df2], axis=0).sort_values(
        by=["Status", "ID"], ascending=[False, False]
    )

st.header("Existing tickets")
st.write(f"Number of tickets: `{len(st.session_state.df)}`")

st.info(
    "You can edit the tickets by double clicking on a cell. Note how the plots below "
    "update automatically! You can also sort the table by clicking on the column headers.",
    icon="✍️",
)

edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,
        ),
    },
)
st.button("🔄 Sort DataFrame by the Status column", on_click=sort_df)

# Status plot
st.header("Statistics")
col1, col2, col3 = st.columns(3)


n_tickets_queue = len(st.session_state.df[st.session_state.df.Status == "Open"])

col1.metric(label="First response time (hr)", value=5.2, delta=-1.5)
col2.metric(label="No. of tickets in the queue", value=n_tickets_queue, delta=10)
col3.metric(label="Avg. ticket resolution time (hr)", value=16, delta=-2)

st.write("")
st.write("##### Ticket status per month")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### Current ticket priorities")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
