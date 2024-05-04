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
        const response = await fetch('http://127.0.0.1:8000/data/soil_data');

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

    const interval = setInterval(fetchData, 5000); 

    return () => clearInterval(interval); 

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
      { limit: 10, label: "Low", color: "#FF0000" }, // Adjust labels and limits based on your data
      { limit: 50, label: "Medium", color: "#FFA500" },
      { limit: 100, label: "Optimal", color: "#00FF00" },
      { limit: 200, label: "High", color: "#0000FF" },
    ],
  };

  const arcsK = {
    // Define arcs for Potassium gauge (similar to arcsN)
    subArcs: [
      { limit: 10, label: "Low", color: "#FF0000" }, // Adjust labels and limits based on your data
      { limit: 50, label: "Medium", color: "#FFA500" },
      { limit: 100, label: "Optimal", color: "#00FF00" },
      { limit: 200, label: "High", color: "#0000FF" },
    ],
  };

  const arcsP = {
    // Define arcs for Phosphorus gauge (similar to arcsN)
    subArcs: [
      { limit: 10, label: "Low", color: "#FF0000" }, // Adjust labels and limits based on your data
      { limit: 50, label: "Medium", color: "#FFA500" },
      { limit: 100, label: "Optimal", color: "#00FF00" },
      { limit: 200, label: "High", color: "#0000FF" },
    ],
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
          <GaugeComponent 
            minValue={0}
            maxValue={200} // Adjust based on your data range
            value={data?.K || 90} // Use data?.N or a default value
            arc={arcsK}
          />
        </div>
        <div className='gaugeContainer'>
          <h4>Phosphorus</h4>
          <GaugeComponent 
            minValue={0}
            maxValue={200} // Adjust based on your data range
            value={data?.P || 90} // Use data?.N or a default value
            arc={arcsP}
          />
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
