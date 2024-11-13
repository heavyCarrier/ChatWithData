import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { format } from 'sql-formatter';
 
function App() {
  const [table_name, setTable_name] = useState('');
  const [user_input, setUser_input] = useState('');
  const [schema_string, setSchema_string] = useState('');
  const [sqlQuery, setSqlQuery] = useState('');
 
  // const generateSqlQuery = () => {
  //   // Simple example of query generation
  //   if (prompt.toLowerCase().includes('all users')) {
  //     setSqlQuery('SELECT * FROM users;');
  //   } else if (prompt.toLowerCase().includes('where account type')) {
  //     setSqlQuery('SELECT * from bank_customers WHERE account_type = "Saving";');//To get customers with account - savings
  //   } else if (prompt.toLowerCase().includes('user count')) {
  //     setSqlQuery('SELECT COUNT(*) FROM users;');
  //   } else {
  //     setSqlQuery('No SQL query generated for the given prompt.');
  //   }
  // };

  const fetchBackendResponse = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/sqlResponse', {
        user_input,
        table_name,
        schema_string
      });
      if (response.data.is_successfull) {
        const query = response.data.query;
        // const finalAnswerIndex = query.indexOf('Final answer:');
        setSqlQuery(query);
        // {
        //   setSqlQuery('No SQL query generated for the given prompt.');
        // }
      } else {
        setSqlQuery('Query generation was not successful.');
      }
      console.log(response);
    } catch (error) {
      console.error('Error fetching backend response:', error);
    }
  };
 

  return (
    <div className="App">
      <img src={require('./R.png')} alt="Logo" className="logo" />
      <h1>SQL Query Generator<span></span></h1>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Ask a question"
          value={user_input}
          onChange={(e) => setUser_input(e.target.value)}
        />
        <button onClick={fetchBackendResponse}>
          <span role="img" aria-label="search">🚀</span>
        </button>
      </div>
      <div className="container1">
      <div className="table_name">
        <input
          type="table_name"
          placeholder="Enter Table name here"
          value={table_name}
          onChange={(e) => setTable_name(e.target.value)}
        />
      </div>
      <div className="Schema_string">
        <input
          type="Schema_string"
          placeholder="Enter Schema string here"
          value={schema_string}
          onChange={(e) => setSchema_string(e.target.value)}
        />
      </div></div>
      <div className="output">
      <div className ="query">QUERY</div>
      <div dangerouslySetInnerHTML={{ __html: sqlQuery.replace(/\n/g, '<br />') }} />
      </div>
    </div>
  );
}
 
export default App;
 