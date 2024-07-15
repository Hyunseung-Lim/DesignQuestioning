export const RadarOptions = {
  plugins: {
    legend: {
        display: false,
    }
  },
  scales: {
    r: {
      min:0,
      max:7,
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
