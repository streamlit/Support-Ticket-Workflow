import streamlit as st
import numpy as np
import pandas as pd

st.title('🎫 Support Ticket Workflow')
st.info('To write a ticket, fill out the form below. Check status or review ticketing analytics using the tabs below.')

# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

</style>
""", unsafe_allow_html=True)

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
        "Collaboration tool not sending notifications"
    ]
    return np.random.choice(issues)

## Generate 100 rows of data
data = {
    'ID': ['TICKET-{}'.format(i) for i in range(1000, 1100)],
    'Issue': [generate_issue() for _ in range(100)],
    'Status': np.random.choice(['Open', 'In Progress', 'Resolved', 'Closed'], size=100),
    'Priority': np.random.choice(['High', 'Medium', 'Low'], size=100)
}

## Create DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(data)

# Tabs for app layout
tabs = st.tabs(['Write a ticket', 'Ticket Status and Analytics'])

recent_ticket_number = int(max(st.session_state.df.ID).split('-')[1])

with tabs[0]:
  st.write('File a new ticket')

  with st.form('addition'):
    issue = st.text_area('Description of issue')
    priority = st.selectbox('Priority', ['High', 'Medium', 'Low'])
    submit = st.form_submit_button('Submit')

  if submit:
      df2 = pd.DataFrame([{'ID': f'TICKET-{recent_ticket_number+1}',
                           'Issue': issue,
                           'Status': 'Open',
                           'Priority': priority}])
      st.write('Ticket submitted!')
      st.dataframe(df2, use_container_width=True, hide_index=True)
      st.session_state.df = pd.concat([st.session_state.df, df2], axis=0)

with tabs[1]:
  st.write('Check the status of your ticket')
  st.data_editor(st.session_state.df, use_container_width=True, hide_index=True, height=385,
                column_config={'Status': st.column_config.SelectboxColumn(
                                    'Status',
                                    help='Ticket status',
                                    width='medium',
                                    options=[
                                        'Open',
                                        'In Progress',
                                        'Resolved',
                                        'Closed'
                                    ],
                                    required=True,
                                 )
                             })
  st.write(f'Number of tickets: `{len(df)}`')
