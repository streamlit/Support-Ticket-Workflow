import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# Page title
st.set_page_config(page_title='Support Ticket Workflow', page_icon='🎫', layout='wide')
st.title('🎫 Support Ticket Workflow')
st.info('To write a ticket, fill out the form below. Check status or review ticketing analytics using the tabs below.')

# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-top: 1.2rem;
    padding-bottom: 1.2rem;
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

## Function to generate random dates
start_date = datetime(2023, 6, 1)
end_date = datetime(2023, 12, 20)
id_values = ['TICKET-{}'.format(i) for i in range(1000, 1100)]
issue_list = [generate_issue() for _ in range(100)]

def generate_random_dates(start_date, end_date, id_values):
    date_range = pd.date_range(start_date, end_date).strftime('%m-%d-%Y')
    return np.random.choice(date_range, size=len(id_values), replace=False)

## Generate 100 rows of data
data = {'Issue': issue_list,
        'Status': np.random.choice(['Open', 'In Progress', 'Closed'], size=100),
        'Priority': np.random.choice(['High', 'Medium', 'Low'], size=100),
        'Date': generate_random_dates(start_date, end_date, id_values)
    }
df = pd.DataFrame(data)
df.insert(0, 'ID', id_values)
df = df.sort_values(by='ID', ascending=False)

## Create DataFrame
if 'df' not in st.session_state:
    st.session_state.df = df

# Tabs for app layout
tabs = st.tabs(['Write a ticket', 'Ticket Status and Analytics'])

recent_ticket_number = int(max(st.session_state.df.ID).split('-')[1])

with tabs[0]:
  #st.warning('File a new ticket')

  with st.form('addition'):
    issue = st.text_area('Description of issue')
    priority = st.selectbox('Priority', ['High', 'Medium', 'Low'])
    submit = st.form_submit_button('Submit')

  if submit:
      today_date = datetime.now().strftime('%m-%d-%Y')
      df2 = pd.DataFrame([{'ID': f'TICKET-{recent_ticket_number+1}',
                           'Issue': issue,
                           'Status': 'Open',
                           'Priority': priority,
                           'Date': today_date
                          }])
      st.write('Ticket submitted!')
      st.dataframe(df2, use_container_width=True, hide_index=True)
      st.session_state.df = pd.concat([st.session_state.df, df2], axis=0).sort_values(by='ID', ascending=False)

with tabs[1]:
  #st.warning('Check the status of your ticket')

  status_col = st.columns((5,1))
  with status_col[0]:
      st.subheader('Support Ticket Status')
  with status_col[1]:
      st.write(f'No. of tickets: `{len(st.session_state.df)}`')
      
  st.data_editor(st.session_state.df, use_container_width=True, hide_index=True, height=212,
                column_config={'Status': st.column_config.SelectboxColumn(
                                            'Status',
                                            help='Ticket status',
                                            options=[
                                                'Open',
                                                'In Progress',
                                                'Closed'
                                            ],
                                            required=True,
                                            ),
                               'Priority': st.column_config.SelectboxColumn(
                                           'Priority',
                                            help='Priority',
                                            options=[
                                                'High',
                                                'Medium',
                                                'Low'
                                            ],
                                            required=True,
                                            ),
                             })
    
  # Status plot
  st.subheader('Support Ticket Analytics')
  col = st.columns((1,3,1))
    
  with col[0]:
      st.metric(label='First response (hr)', value=5.2, delta=-1.5)
      st.metric(label='No. of tickets in queue', value=10, delta='')
      st.metric(label='Avg. ticket resolution time (hr)', value=16, delta='')
      
  with col[1]:
      status_plot = alt.Chart(st.session_state.df).mark_bar().encode(
          x='month(Date):O',
          y='count():Q',
          xOffset='Status:N',
          color = 'Status:N'
      ).properties(title='Ticket status in the past 6 months', height=300).configure_legend(orient='bottom', titleFontSize=14, labelFontSize=14, titlePadding=5)
      st.altair_chart(status_plot, use_container_width=True, theme='streamlit')
      
  with col[2]:
      priority_plot = alt.Chart(st.session_state.df).mark_arc().encode(
                          theta="count():Q",
                          color="Priority:N"
                      ).properties(height=300).configure_legend(orient='bottom', titleFontSize=14, labelFontSize=14, titlePadding=5)
      #priority_plot = alt.Chart(st.session_state.df).mark_bar().encode(
      #    x='month(Date):O',
      #    y='count():Q',
      #    xOffset='Priority:N',
      #    color='Priority:N'
      #).properties(height=200)
      st.altair_chart(priority_plot, use_container_width=True, theme='streamlit')
