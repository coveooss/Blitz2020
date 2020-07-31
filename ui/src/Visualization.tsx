import * as React from 'react';
import {Background, Board, Players, Tails} from './Game/';

export const Visualization: React.FunctionComponent = () => {
    return (
        <>
            <Background />
            <Board />
            <Tails />
            <Players />
        </>
    );
};
