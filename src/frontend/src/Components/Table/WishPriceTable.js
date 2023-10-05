import React, { useMemo } from 'react';
import { useTable, useSortBy } from 'react-table';

import "./WishPriceTable.css"

function WishPriceTable({data}) {
    const formattedData = useMemo(
        () => Object.entries(data).map(([info, price]) => ({ info, price })),
        [data]
    );

    const columns = useMemo(
        () => [
            {
                Header: 'Fahrtzeitpunkt',
                accessor: 'info', 
            },
            {
                Header: 'Preis',
                accessor: 'price',
                Cell: ({ value }) => `${value}€`,
            },
        ],
        []
    );

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
    } = useTable({ columns, data: formattedData }, useSortBy);

  return (
    // creates a table containing the time slot and the corresponding price for the asked connection
    <table {...getTableProps()} style={{ margin: 'auto', border: '2px solid black' }}>
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps(column.getSortByToggleProps())} style={{ borderBottom: '2px solid black' }} >
                {column.render('Header')}
                <span>
                  {column.isSorted
                    ? column.isSortedDesc
                      ? ' ↓'
                      : ' ↑'
                    : ''}
                </span>
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map(row => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()} style={{ borderBottom: '2px solid black' }} >
              {row.cells.map(cell => {
                return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default WishPriceTable;