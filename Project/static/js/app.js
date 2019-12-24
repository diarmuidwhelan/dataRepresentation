// Create the county variable and set it equal to "Clare". This variable will be changed by various functions in the code
var county = "Clare";
// Create the chart_color variable and set it equal to the colorhex for a shade of purple. This variable is used to identify the primary color used in numerous charts. This variable will be changed by various functions in the code
var chart_color = "#3D2B56";
// Create the pie_colors variable and set it equal to a list of colorhexs and rgbs for shades of purple and grey. This list of colors is used to identify the colors used in This variable will be changed by various functions in the code
var pie_colors = ['#3D2B56','#A26769', '#D5B9B2', '#ECE2D0', '#CEBEBE', 'rgb(102, 102, 102)','rgb(76, 76, 76)','rgb(153, 153, 153)','rgb(204, 204, 204)','rgb(229, 229, 229)'];
// Create the bg_color variable and set it equal to a colorhex for a shade of purple. This variable will be changed by various functions in the code
var bg_color ="#dcd2e9";

// Define a price summary function that depends on a variable county. This function will display the keys and values from the scoresummary information that has been queried in the Python app
function scoresummaryData(county) {
    // Define the path to the scoresummary data
    var url = `/scoresummary/${county}`;
    // Use `d3.json` to fetch the price summary data and turn it into the JSON format
    d3.json(url).then(function(county){
      // Use d3 to select the panel with id of `#price-summary`
      var scoresummary = d3.select("#score-summary");
      // Use `.html("") to clear any existing metadata
      scoresummary.html("");
      // Use `Object.entries` to add each key and value pair to the panel
      Object.entries(county).forEach(function ([key, value]) {
        var row = scoresummary.append("p");
        row.text(`${key}: ${value}`);
      });
    }
  );
  }


// Define a buildHistogram function that depends on a variable county. This function will generate a histogram out of the information from the list of prices that has been queried in the Python app
function buildHistogram(county) {
  // Define the path to the list of listing prices
  var url_4 = `/scoreslist/${county}`;
  // Use `d3.json` to fetch the numerical reviews data and turn it into the JSON format
  d3.json(url_4).then(function(county) {
    // Set prices variable equal to the list of prices
    var team_summary = county;
    //  Create a trace and declare is as the trace1 variable
    var trace1 = {
      // Define x values as the list of prices
      x: team_summary,
      // Define chart type as histogram
      type: "histogram",
      
    };
    // Set the chart data equal to the trace
    var data = [trace1];
    // Add chart title, x axis, and y axis labels
    var layout = {
      title: "Distribution of Listing Prices", 
      xaxis: {title: "Listing Prices (USD)"}, 
      yaxis: {title: "Frequency"}
    };
    //  Create the bubble chart
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
    // Trigger all formulas so that the charts and colors all populate
    scoreSummaryData(firstCounty);
    buildHistogram(firstCounty);
    
    county = firstCounty;
    setBackgroundColor();
  });
}

// Create optionChanged formula that defines what happens when the selector option is changed
function optionChanged(newCounty) {
    // Trigger all formulas so that the charts and colors all populate
   scoreSummaryData(newCounty);
   buildHistogram(newCounty);
   
    county = newCounty;
    setBackgroundColor();
  }



// Function thhat sets the background color
function setBackgroundColor() {
  document.body.style.backgroundColor = bg_color;
};

// Initialize the dashboard
init();
