import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Plot from 'react-plotly.js';

interface ClickEventDataInterface {
  x: number
  y: number
  group: any
}

class StreamlitPlotlyEventsComponent extends StreamlitComponentBase {
  public render = (): ReactNode => {
    // Pull Plotly object from args and parse
    const plot_obj = JSON.parse(this.props.args["plot_obj"]);
    const override_height = this.props.args["override_height"];
    const override_width = this.props.args["override_width"];

    // Event booleans
    const click_event = this.props.args["click_event"];
    const select_event = this.props.args["select_event"];
    const hover_event = this.props.args["hover_event"];

    Streamlit.setFrameHeight(override_height);
    return (
      <Plot
        data={plot_obj.data}
        layout={plot_obj.layout}
        config={plot_obj.config}
        frames={plot_obj.frames}
        onClick={click_event ? this.plotlyClickHandler : function () { }}
        style={{ width: override_width, height: override_height }}
        className="stPlotlyChart"
      />
    )
  }

  /** Click handler for plot. */
  private plotlyClickHandler = (data: any) => {
    // Build array of points to return
    let clickedPoints: ClickEventDataInterface = {
      x: data.points[0].x,
      y: data.points[0].y,
      group: data.points[0].fullData.legendgroup
    };

    // Return array as JSON to Streamlit
    Streamlit.setComponentValue(JSON.stringify(clickedPoints))
  }
}

export default withStreamlitConnection(StreamlitPlotlyEventsComponent)
