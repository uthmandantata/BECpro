document.addEventListener("DOMContentLoaded", function () {
    // Sample data for the chart (you can replace this with your own data)
    const chartData = {
      labels: ["January", "February", "March", "April", "May", "June"],
      datasets: [
        {
          label: "Sales",
          data: [3000, 4500, 2500, 3800, 5200, 4800],
          backgroundColor: "rgba(54, 162, 235, 0.5)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
        },
      ],
    };
  
    // Initialize the chart with the default data
    const ctx = document.getElementById("myChart").getContext("2d");
    const myChart = new Chart(ctx, {
      type: "bar",
      data: chartData,
    });
  
    // Get the dropdowns and apply filter button
    const monthDropdown = document.getElementById("month");
    const yearDropdown = document.getElementById("year");
    const applyFilterBtn = document.getElementById("apply-filter");
  
    // Handle applying the filter when the button is clicked
    applyFilterBtn.addEventListener("click", () => {
      const selectedMonth = monthDropdown.value;
      const selectedYear = yearDropdown.value;
      const filteredData = getFilteredData(selectedMonth, selectedYear);
      updateChart(filteredData);
    });
  
    // Function to get filtered data based on selected month and year
    function getFilteredData(month, year) {
      // Sample data for demonstration purposes
      // You should replace this with your own data retrieval logic
      // e.g., fetch data from an API based on selectedMonth and selectedYear
      return [1000, 1500, 2000, 2500, 3000, 3500];
    }
  
    // Function to update the chart with new data
    function updateChart(data) {
      myChart.data.datasets[0].data = data;
      myChart.update();
    }
  });
  