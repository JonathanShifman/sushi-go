import React, {Fragment, useState, useEffect} from 'react';
import './Game.css';
import cardImages from '../../utils/cards';

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
                <div className={'game-grid-cell game-grid-header-cell'}>Player</div>
                <div className={'game-grid-cell game-grid-header-cell'}>Cards</div>
                <div className={'game-grid-cell game-grid-header-cell'}>Score</div>
                <div className={'game-grid-cell game-grid-header-cell'}>Pudding Count</div>
                <div className={'game-grid-cell game-grid-header-cell'}>Pudding Score</div>
                <div className={'game-grid-cell game-grid-header-cell'}>Final Score</div>
                { getPlayerCells(props.gameData, status) }
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

function getPlayerCells(gameData, gameStatus) {
    let numOfPlayers = gameData.players.length;
    let res = [];
    for (let i = 0; i < numOfPlayers; i++) {
        let row = (
            <Fragment key={'player' + i + 'Row'}>
                <div className={'game-grid-cell'}>{ gameData.players[i] }</div>
                <div className={'game-grid-cell'}>{ getPlayerCards(gameData, gameStatus, i) }</div>
                <div className={'game-grid-cell'}>{ getPlayerScore(gameData, gameStatus, i) }</div>
                <div className={'game-grid-cell'}>{ getPlayerPuddingCount(gameData, gameStatus, i) }</div>
                <div className={'game-grid-cell'}>{ getPlayerPuddingScore(gameData, gameStatus, i) }</div>
                <div className={'game-grid-cell'}>{ getPlayerFinalScore(gameData, gameStatus, i) }</div>
            </Fragment>
        );
        res.push(row);
    }
    return res;
}

function getPlayerCards(gameData, gameStatus, playerIndex) {
    if (gameStatus.isGameOver || gameStatus.isRoundOver) return <div className={'player-cards-w'}></div>;
    let playerMove = gameData.rounds[gameStatus.currentRound].roundMoves[gameStatus.currentMove][playerIndex];
    let correctHandAndPlate = gameStatus.currentStageWithinMove < 2 ? playerMove.before : playerMove.after;
    let selectedIndices = new Set();
    if (gameStatus.currentStageWithinMove == 1) selectedIndices = new Set(playerMove.chosenCardIndices);
    return (
        <div className={'player-cards-w'}>
            { getCardList(correctHandAndPlate.hand, selectedIndices) }
            { getCardList(correctHandAndPlate.plate, new Set()) }
        </div>
    );
}

function getCardList(cards, selectedIndices) {
    return (
        <div className={'card-list-w'}>{ getCardImages(cards, selectedIndices) }</div>
    );
}

function getCardImages(cards, selectedIndices) {
    let res = [];
    for (let cardIndex = 0; cardIndex < cards.length; cardIndex++) {
        let card = cards[cardIndex];
        let className = selectedIndices.has(cardIndex) ? 'card-w selected-card-w' : 'card-w';
        res.push(
            <div className={className}>
                <img src={cardImages[card]} className={'card'} key={'card' + cardIndex} />
            </div>
        );
    }
    return res;
}

function getPlayerScore(gameData, gameStatus, playerIndex) {
    let numOfCompletedRounds = getNumOfCompletedRounds(gameStatus);
    if (numOfCompletedRounds == 0) return 0;
    return gameData.rounds[numOfCompletedRounds - 1].totalScores[playerIndex];
}

function getPlayerPuddingCount(gameData, gameStatus, playerIndex) {
    let numOfCompletedRounds = getNumOfCompletedRounds(gameStatus);
    if (numOfCompletedRounds == 0) return 0;
    return gameData.rounds[numOfCompletedRounds - 1].puddingCounts[playerIndex];
}

function getPlayerPuddingScore(gameData, gameStatus, playerIndex) {
    if (!gameStatus.isGameOver) return null;
    return gameData.puddingScores[playerIndex];
}

function getPlayerFinalScore(gameData, gameStatus, playerIndex) {
    if (!gameStatus.isGameOver) return null;
    return gameData.finalScores[playerIndex];
}

function getNumOfCompletedRounds(gameStatus) {
    if (gameStatus.isGameOver) return 3;
    if (gameStatus.isRoundOver) return  gameStatus.currentRound + 1;
    return gameStatus.currentRound;
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
        updatedStatus.currentRound = 2;
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
        return updatedStatus;
    }
    updatedStatus.currentStageWithinMove--;
    return updatedStatus;
}

export default Game;
