// Result.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './result.css';

const Result = () => {
  const { id } = useParams();
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/testcase/${id}/stats/`);
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [id]);

  return (
    <div className="result">
      <h1>Incremental Data</h1>
      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>test_id</th>
            <th>RPS</th>
            <th>Failures_per_second</th>
            <th>avg_response_time</th>
            <th>number_of_users</th>
            <th>recorded_time</th>
          </tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row[0]}>
              <td>{row[0]}</td>
              <td>{row[1]}</td>
              <td>{row[2]}</td>
              <td>{row[3]}</td>
              <td>{row[4]}</td>
              <td>{row[5]}</td>
              <td>{new Date(row[6] * 1000).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Result;