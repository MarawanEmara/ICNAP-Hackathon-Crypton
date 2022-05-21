import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/time")
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);

  return (<div>

    {(typeof data === "undefined") ? (<div>Loading...</div>) : (<div>{data.time}</div>)}

  </div>);
}

export default App;
