import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.express as px

DATA_SRC = 'recorded_data'


@st.cache(show_spinner=False)
def load_action():
    data = pd.read_csv('actions.csv')
    return data


@st.cache(show_spinner=False)
def load_all_data():

    all_files = os.listdir(DATA_SRC)
    all_data = {}

    for f in all_files:
        data = pd.read_csv('{}/{}'.format(DATA_SRC, f))
        all_data[f.split('.')[0]] = data

    # Dict {file-name: data}
    return all_data


def process_df(df, file_name, action_id):
    new_df = df[file_name]
    new_df = new_df.loc[new_df['action_id'] == action_id]
    new_df['file'] = file_name
    return new_df


def filter_data_by_action(all_data, action_id):
    data = []
    for fn, df in all_data.items():
        data.append(process_df(all_data, fn, action_id))

    return pd.concat(data)


def main():
    actions = load_action()
    all_data = load_all_data()

    action_opt = st.sidebar.selectbox(
        label="Select action to display",
        options=actions['id'],
        format_func=lambda id: actions['action'].iloc[int(id) - 1]
    )

    print(action_opt)

    # Get data by action
    hist_data = filter_data_by_action(all_data, action_opt)

    # Draw
    fig = px.histogram(hist_data, x="time", color="file",
                       barmode="group", nbins=20)
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        yaxis=dict(
            tickmode='linear',
            dtick=1
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    st.text('Histogram of {}'.format(actions['action'].iloc[int(action_opt) - 1]))


if __name__ == "__main__":
    main()
