import streamlit as st
import streamlit.components.v1 as components

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import os
from json import loads

plotly_custom_component = components.declare_component(
    'plotly_custom_component', url='http://localhost:3001'
)

DATA_SRC = 'recorded_data'
BIN_SIZE = 4

#################### Utils ####################


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


def load_video():
    video_file = open('sample_video/sample.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

###############################################

################## Streamlit ##################


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


def parse_plotly(
    plot_fig,
    click_event=True,
    select_event=False,
    hover_event=False,
    override_height=450,
    override_width="100%",
    key=None,
):
    """Create a new instance of "plotly_events".
    Parameters
    ----------
    plot_fig: Plotly Figure
        Plotly figure that we want to render in Streamlit
    click_event: boolean, default: True
        Watch for click events on plot and return point data when triggered
    select_event: boolean, default: False
        Watch for select events on plot and return point data when triggered
    hover_event: boolean, default: False
        Watch for hover events on plot and return point data when triggered
    override_height: int, default: 450
        Integer to override component height.  Defaults to 450 (px)
    override_width: string, default: '100%'
        String (or integer) to override width.  Defaults to 100% (whole width of iframe)
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    """
    # kwargs will be exposed to frontend in "args"
    component_value = plotly_custom_component(
        plot_obj=plot_fig.to_json(),
        override_height=override_height,
        override_width=override_width,
        key=key,
        click_event=click_event,
        select_event=select_event,
        hover_event=hover_event,
        default="[]",  # Default return empty JSON list
    )

    # Parse component_value since it's JSON and return to Streamlit
    return loads(component_value)

###############################################


def main():
    actions = load_action()
    all_data = load_all_data()

    # Sidebar
    action_opt = st.sidebar.selectbox(
        label='Select action to display',
        options=actions['id'],
        format_func=lambda id: actions['action'].iloc[int(id) - 1]
    )

    # Get data by action
    hist_data = filter_data_by_action(all_data, action_opt)

    # Graph
    fig = px.histogram(hist_data, x='time', color='file',
                       barmode='stack')

    fig.update_traces(xbins=dict(
        size=BIN_SIZE
    ))

    _selected_point = parse_plotly(fig)

    if _selected_point:
        selected_point = {
            'range': (_selected_point['x'] - (BIN_SIZE-1)/2, _selected_point['x'] + (BIN_SIZE-1)/2),
            'count': _selected_point['y'],
            'file': _selected_point['group']
        }

        st.write("Selected data:")
        st.write(selected_point)
        load_video()


if __name__ == '__main__':
    main()
