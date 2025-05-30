async function getPrediction() {
  const symbol = document.getElementById("symbol").value;

  if (!symbol) {
    alert("Please enter a stock symbol!");
    return;
  }

  const response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symbol: symbol.toUpperCase() })
  });

  const data = await response.json();

  if (data.error) {
    alert(data.error);
    return;
  }

  const labels = Array.from({ length: 7 }, (_, i) => `Day ${i + 1}`);
  const open = data.map((d) => d.open);
  const high = data.map((d) => d.high);
  const low = data.map((d) => d.low);
  const close = data.map((d) => d.close);

  if (window.myChart) window.myChart.destroy();

  const ctx = document.getElementById("ohlcChart").getContext("2d");
  window.myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        { label: "Open", data: open, borderColor: "blue", fill: false },
        { label: "High", data: high, borderColor: "green", fill: false },
        { label: "Low", data: low, borderColor: "orange", fill: false },
        { label: "Close", data: close, borderColor: "red", fill: false }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "top" } },
      scales: {
        y: { title: { display: true, text: "Price (USD)" } },
        x: { title: { display: true, text: "Next 7 Days" } }
      }
    }
  });
}
