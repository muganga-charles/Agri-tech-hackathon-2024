import { useState, useEffect } from 'react';
import GaugeComponent from 'react-gauge-component';
import './App.css'; // Import your CSS file

interface IData {
  N: number; // Nitrogen
  P: number; // Phosphorus
  K: number; // Potassium
  pH: number; // Acidity
}

function App() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);
  const [data, setData] = useState<IData | null>(null);

  // Update gauge values upon successful data fetch
  const updateGaugeValues = (fetchedData: IData) => {
    setData(fetchedData);
  };

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch('https://your-server.com/api/data');

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const fetchedData: IData = await response.json();
        updateGaugeValues(fetchedData);
      } catch (error) {
        setError(error as Error);
      } finally {
        setIsLoading(false);
      }
    };

    const interval = setInterval(fetchData, 5000); // Fetch data every 5 seconds

    return () => clearInterval(interval); // Cleanup function to clear interval

  }, []);

  const arcs = {
    subArcs: [
      { limit: 3, label: "High acidity", color: "#FF0000" },
      { limit: 6, label: "Medium acidity", color: "#FFA500" },
      { limit: 7, label: "Normal acidity", color: "#00FF00" },
      { limit: 10, label: "Low acidity", color: "#0000FF" },
      { label: "Very low acidity", color: "#800080" },
    ],
  };

  const arcsN = {
    subArcs: [
      { limit: 10, label: "Low Nitrogen", color: "#FF0000" }, // Adjust labels and limits based on your data
      { limit: 50, label: "Medium Nitrogen", color: "#FFA500" },
      { limit: 100, label: "Optimal Nitrogen", color: "#00FF00" },
      { limit: 200, label: "High Nitrogen", color: "#0000FF" },
    ],
  };

  const arcsK = {
    // Define arcs for Potassium gauge (similar to arcsN)
  };

  const arcsP = {
    // Define arcs for Phosphorus gauge (similar to arcsN)
  };

  return (
    <div className="App">
      <div className="title">
        <h5>Soil Monitor</h5>
      </div>
      <div className="gauges">
        <div className="gaugeContainer">
          <h4>pH</h4>
          <GaugeComponent
            minValue={0}
            maxValue={14}
            value={data?.pH || 9} // Use data?.pH or a default value
            arc={arcs}
            pointer={{
              type: "blob",
              color: "#464A4F",
              baseColor: "#464A4F",
              length: 0.70,
              animate: true,
              elastic: false,
              animationDuration: 3000,
              animationDelay: 100,
              width: 20,
            }}
          />
        </div>
        <div className="gaugeContainer">
          <h4>Nitrogen</h4>
          <GaugeComponent
            minValue={0}
            maxValue={200} // Adjust based on your data range
            value={data?.N || 90} // Use data?.N or a default value
            arc={arcsN}
          />
        </div>
        <div className='gaugeContainer'>
          <h4>Potassium</h4>
          <GaugeComponent />
        </div>
        <div className='gaugeContainer'>
          <h4>Phosphorus</h4>
          <GaugeComponent />
        </div>
      </div>

      <div className='predict'>
        <button>Generate Prediction</button>
        <div className='prediction'>
          <p>james</p>
        </div>
      </div>
    </div>

  );
}

export default App;
