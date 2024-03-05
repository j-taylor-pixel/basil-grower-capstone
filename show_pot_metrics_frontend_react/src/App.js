import React, { useState, useEffect } from 'react';

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
      <h1>Basil Metrics:</h1>
      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
        {Object.keys(data).slice(0, 2).map(key => (
          <div key={key} style={{ margin: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '24px' }}>{data[key]}</div>
            <div style={{ fontSize: '12px' }}>{key}</div>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
        {Object.keys(data).slice(2, 4).map(key => (
          <div key={key} style={{ margin: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '24px' }}>{data[key]}</div>
            <div style={{ fontSize: '12px' }}>{key}</div>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
        {Object.keys(data).slice(4, 6).map(key => (
          <div key={key} style={{ margin: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '24px' }}>{data[key]}</div>
            <div style={{ fontSize: '12px' }}>{key}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
export default App;