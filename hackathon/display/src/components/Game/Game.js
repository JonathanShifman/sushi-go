import React, {Fragment, useState} from 'react';
import './Game.css';

function Game(props) {
    let [status, setStatus] = useState(getInitialStatus());

    return (
        <div id={'game-w'}>
            { getStatusDiv(status) }
            <div id={'game-grid-w'}>
                <div className={'game-grid-header-cell'}>Player</div>
                <div className={'game-grid-header-cell'}>Cards</div>
                <div className={'game-grid-header-cell'}>Score</div>
                <div className={'game-grid-header-cell'}>Pudding Count</div>
                <div className={'game-grid-header-cell'}>Pudding Score</div>
                <div className={'game-grid-header-cell'}>Final Score</div>
                { getPlayerCells(props.gameData) }
            </div>
        </div>
    )
}

function getInitialStatus() {
    return {
        isGameOver: false,
        currentRound: 0,
        isRoundOver: false,
        currentMove: 0,
        currentStageWithinMove: 0
    }
}

function getStatusDiv(status) {
    return (
        <div id={'game-status-w'}>
            { getStatusString(status)}
        </div>
    );
}

function getStatusString(status) {
    if (status.isGameOver) return 'Game End';
    let stringRoundNumber = status.currentRound + 1;
    if (status.isRoundOver) return 'Round ' + stringRoundNumber + ' End';
    let stringMoveNumber = status.currentMove + 1;
    return 'Round ' + stringRoundNumber + ', Move ' + stringMoveNumber;
}

function getPlayerCells(gameData) {
    let numOfPlayers = gameData.players.length;
    let res = [];
    for (let i = 0; i < numOfPlayers; i++) {
        let row = (
            <Fragment key={'player' + i + 'Row'}>
                <div>{ gameData.players[i] }</div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </Fragment>
        );
        res.push(row);
    }
    return res;
}

export default Game;
