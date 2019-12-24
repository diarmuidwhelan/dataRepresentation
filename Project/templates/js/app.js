// Create the county variable and set it equal to "Clare". This variable will be changed by various functions in the code
var county = "Clare";




// Define a buildHistogram function that depends on a variable county. This function will generate a histogram out of the information from the list of scores that has been queried in the Python app
function buildHistogram(county) {
  // Define the path to the list of scores
  var url_4 = `/scoreslist/${county}`;
  // Grab a reference to the dropdown select element
  // Use `d3.json` to fetch the data and turn it into the JSON format
  d3.json(url_4).then(function(county) {
    // Set prices variable equal to the list of scores
    var team_summary = county;
    //  Create a trace and declare is as the trace1 variable
    var trace1 = {
      // Define x values as the list of scores
      x: team_summary,
      // Define chart type as histogram
      type: "histogram",
      
    };
    // Set the chart data equal to the trace
    var data = [trace1];
    // Add chart title, x axis, and y axis labels
    var layout = {
      title: "Distribution of Scores", 
      xaxis: {title: "Scores"}, 
      yaxis: {title: "Frequency"}
    };
    //  Create the  chart
    Plotly.newPlot('histogram', data, layout);
  });
}


// Create init function
function init() {
  
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selCounty");

  // Use the list of countys to populate the select options
  d3.json("/counties").then((counties) => {
    counties.forEach((county) => {
      selector
        .append("option")
        .text(county)
        .property("value", county);
    });

    // Use the first county from the list to build the initial plots
    const firstCounty = counties[0];
    // Trigger all formulas so that the charts  all populate
    buildHistogram(firstCounty);
    
    county = firstCounty;
  });
}

// Create optionChanged formula that defines what happens when the selector option is changed
function optionChanged(newCounty) {
    // Trigger all formulas so that the charts all populate
   buildHistogram(newCounty);
   
    county = newCounty;
  }



// Initialize the dashboard
init();
