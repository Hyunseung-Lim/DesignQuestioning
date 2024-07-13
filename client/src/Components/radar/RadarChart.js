import React from "react";
import { RadarData, RadarOptions } from "./RadarConfig";
import { Radar } from "react-chartjs-2";
import { Chart as ChartJS } from 'chart.js/auto';

export class RadarChart extends React.Component {
  constructor(props) {
    super(props);
    this.chartRef = React.createRef();
  }

  componentDidMount() {
    console.log(this.chartRef);
  }

  render() {
    return (
      <Radar ref={this.chartRef} data={RadarData} options={RadarOptions} />
    );
  }
}
