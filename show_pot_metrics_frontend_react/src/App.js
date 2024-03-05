import React, { useState, useEffect } from 'react';

function simplifyKey(key) {
  return key.split('.').pop().charAt(0).toUpperCase() + key.slice(1).split('.').pop().slice(1);
}

function getColor(value) {
  return value > 50 ? 'green' : 'red';
}

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch('http://127.0.0.1:5000/')
      .then(response => response.json())
      .then(json => setData(json))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h1>Basil Metrics</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', justifyContent: 'center' }}>
        {Object.keys(data).map(key => (
          <div key={key} style={{ width: '100px', height: '100px', textAlign: 'center', backgroundColor: getColor(data[key]), color: 'white', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: '40px' }}>{data[key]}%</div>
            <div style={{ fontSize: '14px' }}>{simplifyKey(key)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
