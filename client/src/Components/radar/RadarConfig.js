export const RadarData = {
  labels: ["독창성", "연관성", "난이도", "구체성", "타당성", "실행가능성"],
  datasets: [
    {
      backgroundColor: "rgba(44, 84, 242, .7)",
      // borderColor: "#2C54F2",
      // pointBackgroundColor: "#2C54F2",
      // pointBorderColor: "#fff",
      // pointHoverBackgroundColor: "#fff",
      // pointHoverBorderColor: "#2C54F2",
      data: [7, 6, 5.1, 2.1, 6, 5],
      pointRadius: 0, // Set point radius to 0 to hide the points
      pointHitRadius: 0
    }
  ]
};

export const RadarOptions = {
  plugins: {
    legend: {
        display: false,
    }
  },
  scales: {
    r: {
      pointLabels: {
        font: {
          size: 13,  // Adjust the font size for the main labels
          weight: 800
        },
        // Optional: Add color and other font properties if needed
        // color: '#666'  // Sets the color of the point labels
      },
      ticks: {
        display: false,
        min:0,
        max:7,
        stepSize: 1.4
      }
    }
  }
};
