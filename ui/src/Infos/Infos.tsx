import * as React from 'react';
import {GameState} from './GameState';
import {Scores} from './Scores';

export interface InfosProps {
    speed?: number;
}

export const Infos: React.FunctionComponent<InfosProps> = ({speed}) => {
    return (
        <>
            <Scores />
            <GameState speed={speed} />
        </>
    );
};
