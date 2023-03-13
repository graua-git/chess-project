import React from 'react';
import square_image_dark from './images/empty_dark.png';
import square_image_light from './images/empty_light.png'

export default function Square({row, col}) {

    const square_id = (row)*10 + col;
    let img;
    if ((row + col) % 2 === 0) {
        img = square_image_dark
    } else {
        img = square_image_light
    }

    const handleClick = (e) => {
        e.preventDefault();
        console.log(`${row}, ${col}`)
    }

    return (
        <img src={img} id={square_id} alt="square" onClick={handleClick}/>
    );
}