import React from 'react';

export const Channel = ({data})=> {
    return(
        <div>
            <h1>{data.Station}</h1>
            <h2>{data.NextTrain} min</h2>
        </div>
    )
}