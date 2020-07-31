import * as React from 'react';
import {Stage} from 'react-konva';
import {Size, VisualizationContext} from './Constants';
import {Infos} from './Infos/Infos';
import {IBlitzVisualization} from './IVisualization';
import {Visualization} from './Visualization';

export interface ILiveViewerProps {
    game: IBlitzVisualization;
    width: number;
    height: number;
    tick: number;
}

export const LiveViewer: React.FunctionComponent<ILiveViewerProps> = ({width, height, game, tick}) => {
    const numberOfTile: number = game.ticks[tick].game.map.length;
    const boardSize = Math.min(width, height) * 0.8;

    Size.Tile = boardSize / numberOfTile;

    return (
        <Stage width={width} height={height}>
            <VisualizationContext.Provider value={{tick, boardSize, game}}>
                <Visualization />
                <Infos />
            </VisualizationContext.Provider>
        </Stage>
    );
};
