import React, {useEffect} from "react";
import { RadarOptions } from "./RadarConfig";
import { Radar } from "react-chartjs-2";
import { Chart as ChartJS } from 'chart.js/auto';


export class RadarChart extends React.Component {
  constructor(props) {
    super(props);
    this.chartRef = React.createRef();
  }

  componentDidMount() {
    // console.log(this.chartRef);
  }


  render() {

    const RadarData = {
      labels: ["독창성", "연관성", "난이도", "구체성", "타당성", "실행가능성"],
      datasets: [
        {
          backgroundColor: "rgba(44, 84, 242, .7)",
          // borderColor: "#2C54F2",
          // pointBackgroundColor: "#2C54F2",
          // pointBorderColor: "#fff",
          // pointHoverBackgroundColor: "#fff",
          // pointHoverBorderColor: "#2C54F2",
          data: this.props.evalPoint,
          pointRadius: 0, // Set point radius to 0 to hide the points
          pointHitRadius: 0
        }
      ]
    };

    return (
      <Radar ref={this.chartRef} data={RadarData} options={RadarOptions} />
    );
  }
}
