import React, {useState} from 'react';
import './App.css';
import Input from "../Input/Input";
import Game from "../Game/Game";

function App() {
    let [gameData, setGameData] = useState(null);
    let state = {
        gameData, setGameData
    };

    return (
        <div id={'app-w'}>
            { getAppropriateView(state) }
        </div>
    );
}

function getAppropriateView(state) {
    return state.gameData == null ? getInputView(state) : getGameView(state);
}

function getInputView(state) {
    return <Input onGameDataLoaded={gameData => state.setGameData(gameData)}/>;
}

function getGameView(state) {
    return <Game gameData={state.gameData} />
}

export default App;
