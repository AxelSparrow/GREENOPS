import { useEffect, useState } from "react";

function Dashboard() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8001/metrics")
      .then((res) => res.json())
      .then((data) => setMetrics(data));
  }, []);

  return (
    <div>
      <h1>GreenOps Dashboard</h1>

      {metrics && (
        <>
          <p>Energy : {metrics.energy}</p>
          <p>CO2 : {metrics.co2}</p>
          <p>Consumption : {metrics.consumption}</p>
        </>
      )}
    </div>
  );
}

export default Dashboard;