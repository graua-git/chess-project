import React from 'react';
import Square from './Square.js';

export default function Row({row}) {
    return (
        <div>
            <Square row={row} col={0} />
            <Square row={row} col={1} />
            <Square row={row} col={2} />
            <Square row={row} col={3} />
            <Square row={row} col={4} />
            <Square row={row} col={5} />
            <Square row={row} col={6} />
            <Square row={row} col={7} />
        </div>
    )
}