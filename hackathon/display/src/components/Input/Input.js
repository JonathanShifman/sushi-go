import React from 'react';
import './Input.css';
import logo from '../../assets/logo.png';

function Input(props) {
    return (
        <div id={'input-w'}>
            {/*<img src={logo} id={'input-logo'} />*/}
            <input type={'file'} onChange={e => onFileSelected(e.target.files[0], props.onGameDataLoaded)} />
        </div>
    );
}

function onFileSelected(file, onGameDataLoaded) {
    let reader = new FileReader();
    reader.onload = e => {
        let gameData = JSON.parse(e.target.result);
        console.log(gameData);
        onGameDataLoaded(gameData);
    };
    reader.readAsText(file);
}

export default Input;
