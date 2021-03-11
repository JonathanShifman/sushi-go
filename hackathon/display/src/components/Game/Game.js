import React, {Fragment, useState, useEffect} from 'react';
import './Game.css';

function Game(props) {
    let [status, setStatus] = useState(getInitialStatus(props.gameData));
    let state = {
        status, setStatus
    };

    let keyDownListener = e => onKeyDown(e, state);
    useEffect(() => {
        document.addEventListener('keydown', keyDownListener);
        return () => document.removeEventListener('keydown', keyDownListener);
    });

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

function getInitialStatus(gameData) {
    return {
        isGameOver: false,
        currentRound: 0,
        isRoundOver: false,
        currentMove: 0,
        currentStageWithinMove: 0,
        movesPerRound: getMovesPerRound(gameData)
    }
}

function getMovesPerRound(gameData) {
    return gameData.rounds[0].roundMoves.length;
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
    let stringStageNumber = status.currentStageWithinMove + 1;
    return 'Round ' + stringRoundNumber + ', Move ' + stringMoveNumber + ', Stage ' + stringStageNumber;
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

function onKeyDown(e, state) {
    if (e.key == 'ArrowLeft') state.setStatus(decreaseStatus(state.status));
    if (e.key == 'ArrowRight') state.setStatus(increaseStatus(state.status));
}

function increaseStatus(status) {
    let updatedStatus = Object.assign({}, status);
    if (updatedStatus.isGameOver) return updatedStatus;
    if (updatedStatus.isRoundOver) {
        if (updatedStatus.currentRound == 2) {
            updatedStatus.isGameOver = true;
            return updatedStatus;
        }
        updatedStatus.isRoundOver = false;
        updatedStatus.currentRound++;
        updatedStatus.currentMove = 0;
        updatedStatus.currentStageWithinMove = 0;
        return updatedStatus;
    }
    if (updatedStatus.currentStageWithinMove == 2) {
        if (updatedStatus.currentMove == updatedStatus.movesPerRound - 1) {
            updatedStatus.isRoundOver = true;
            return updatedStatus;
        }
        updatedStatus.currentMove++;
        updatedStatus.currentStageWithinMove = 0;
        return updatedStatus;
    }
    updatedStatus.currentStageWithinMove++;
    return updatedStatus;
}

function decreaseStatus(status) {
    let updatedStatus = Object.assign({}, status);
    if (updatedStatus.isGameOver) {
        updatedStatus.isGameOver = false;
        updatedStatus.isRoundOver = true;
        updatedStatus.currentRound = 3;
        updatedStatus.currentMove = updatedStatus.movesPerRound - 1;
        updatedStatus.currentStageWithinMove = 2;
        return updatedStatus;
    }
    if (updatedStatus.isRoundOver) {
        updatedStatus.isRoundOver = false;
        updatedStatus.currentMove = updatedStatus.movesPerRound - 1;
        updatedStatus.currentStageWithinMove = 2;
        return updatedStatus;
    }
    if (updatedStatus.currentStageWithinMove == 0) {
        if (updatedStatus.currentMove == 0) {
            if (updatedStatus.currentRound == 0) return updatedStatus;
            updatedStatus.currentRound--;
            updatedStatus.isRoundOver = true;
            return updatedStatus;
        }
        updatedStatus.currentMove--;
        updatedStatus.currentStageWithinMove = 2;
    }
    updatedStatus.currentStageWithinMove--;
    return updatedStatus;
}

export default Game;
