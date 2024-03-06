import React, { useState, useEffect } from 'react';

function simplifyKey(key) {
  return key.split('.').pop().charAt(0).toUpperCase() + key.slice(1).split('.').pop().slice(1);
}

function getColor(value) {
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

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('https://show-image-ro735h6uvq-pd.a.run.app/');
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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h1>Basil Metrics</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', justifyContent: 'center' }}>
        {Object.keys(data).map(key => (
          <div key={key} style={{ width: '100px', height: '100px', textAlign: 'center', backgroundColor: getColor(data[key]), color: 'white', display: 'flex', flexDirection: 'column', justifyContent: 'center', borderRadius: '10px' }}>
            <div style={{ fontSize: '40px' }}>{data[key]}%</div>
            <div style={{ fontSize: '14px' }}>{simplifyKey(key)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
