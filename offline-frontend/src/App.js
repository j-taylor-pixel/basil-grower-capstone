import React, { useState, useEffect } from 'react';

function simplifyKey(key) {
  const parts = key.split('_');
  return parts.map(part => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
}

function getColor(key, value) {
  if (key === 'temperature') {
    if ( value > 38 || value < 20){
      return 'red'
    } else if (value > 35 || value < 23){
      return 'orange'
    } else if ( value > 32 || value < 26){
      return 'yellow'
    } else { // 26 - 32 is ideal
      return 'green'
    }
  } else {
    if (value <= 25) {
      return 'red';
    } else if (value <= 50) {
      return 'orange';
    } else if (value <= 75) {
      return 'yellow';
    } else {
      return 'green';
    }
  }
}


function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('data.json');
        const json = await response.json();
        setData(json);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Fetch data initially
    fetchData();

    // Fetch data every 10 seconds
    const interval = setInterval(fetchData, 10000);

    // Clean up interval on unmount
    return () => clearInterval(interval);
  }, []);

  // Filter out the max_temp key
  const filteredData = Object.fromEntries(
    Object.entries(data).filter(([key, value]) => key !== 'max_temp')
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h1>Basil Metrics</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', justifyContent: 'center' }}>
        {Object.keys(filteredData).map(key => (
          <div key={key} style={{ width: '100px', height: '100px', textAlign: 'center', backgroundColor: getColor(key, filteredData[key]), color: 'white', display: 'flex', flexDirection: 'column', justifyContent: 'center', borderRadius: '10px' }}>
            <div style={{ fontSize: '40px' }}>{key === 'temperature' ? filteredData[key] + '°C' : filteredData[key] + '%'}</div>
            <div style={{ fontSize: '14px' }}>{simplifyKey(key)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
