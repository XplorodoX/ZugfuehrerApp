import React, { useState } from 'react';
import './DelaysTable.css';

const DelaysTable = ({ data }) => {
  const [expandedItem, setExpandedItem] = useState(null);
  const [subTableData, setSubTableData] = useState([]);

  const handleClick = async (index, lineId) => {
    if (expandedItem === index) {
      setExpandedItem(null);
    } else {
      setExpandedItem(index);
      await fetchSubTableData(lineId);
    }
  };

  const fetchSubTableData = async (lineId) => {
    try {
      const response = await fetch('/delays_submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          line_id: lineId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setSubTableData(data);
      console.log('Subtable Data:', data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (!Array.isArray(data)) {
    return <div>No data available!</div>;
  }

  return (
    <table className="delays-table">
      <thead>
        <tr>
          <th>Train Number</th>
          <th>Average Arrival Delay</th>
          <th>Average Departure Delay</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <React.Fragment key={index}>
            <tr
              className={`table-row ${expandedItem === index ? 'expanded' : ''}`}
              onClick={() => handleClick(index, item['n'])}
            >
              <td>{item['n']}</td>
              <td>{item['ar_time_diff'] || '-'}</td>
              <td>{item['dp_time_diff'] || '-'}</td>
            </tr>
            {expandedItem === index && (
              <tr className="expanded-content">
                <td colSpan="3">
                  <div>
                    <p>Additional Text</p>
                    <div>
                      <button>Button 1</button>
                      <button>Button 2</button>
                    </div>
                    <table className="sub-table">
                      <thead>
                        <tr>
                          <th>Train Number</th>
                          <th>Average Arrival Delay</th>
                          <th>Average Departure Delay</th>
                        </tr>
                      </thead>
                      <tbody>
                        {subTableData.map((subItem, subIndex) => (
                          <tr key={subIndex}>
                            <td>{subItem['n']}</td>
                            <td>{subItem['ar_time_diff'] || '-'}</td>
                            <td>{subItem['dp_time_diff'] || '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </td>
              </tr>
            )}
          </React.Fragment>
        ))}
      </tbody>
    </table>
  );
};

export default DelaysTable;
