const options = {method: 'GET', headers: {accept: 'application/json'}};

fetch('https://api.tomorrow.io/v4/weather/forecast?location=sein%C3%A4joki&timesteps=daily&apikey=xb7VrP408EHvGOk4iSYy0iZhK1e7gAhW', options)
  .then(response => response.json())
  .then(response => console.log(response))
  .catch(err => console.error(err));