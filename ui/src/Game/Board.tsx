import * as React from 'react';
import {FastLayer} from 'react-konva';

import {Size, VisualizationContext} from '../Constants';
import {Asteroid, BlackHole, Blitzium, Capture, Empty, ITileInterface, Planet, TilesUtils} from './Tiles';

export const Board: React.FunctionComponent = () => {
    const {game, tick} = React.useContext(VisualizationContext);
    const tiles = game.ticks[tick].game.map.map((row, y) =>
        row.map((col, x) => {
            const defaultProps: ITileInterface & {key: string} = {key: `tile-${y}-${x}`, x, y};
            if (TilesUtils.isCaptured(col)) {
                const id = parseInt(col.split('-')[1], 10);
                return <Capture {...defaultProps} playerId={id} />;
            } else if (TilesUtils.isWall(col)) {
                return <Asteroid {...defaultProps} />;
            } else if (TilesUtils.isBlackHole(col)) {
                return <BlackHole {...defaultProps} />;
            } else if (TilesUtils.isBlitzium(col)) {
                return <Blitzium {...defaultProps} />;
            } else if (TilesUtils.isStar(col)) {
                const isNotCaptured = TilesUtils.isNotCapturedPlanet(col);
                const id = isNotCaptured ? null : parseInt(col.split('-')[1], 10);
                return <Planet {...defaultProps} playerId={id} />;
            }
            return <Empty {...defaultProps} />;
        })
    );

    return (
        <FastLayer hitGraphEnabled={false} offset={{x: -0.5 * Size.Gap, y: -0.5 * Size.Gap}}>
            {tiles}
        </FastLayer>
    );
};
