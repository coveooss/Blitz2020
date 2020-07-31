import * as React from 'react';
import {Circle} from 'react-konva';

import {Size} from '../../Constants';
import {ITileInterface} from './TilesInterface';

export const BlackHole: React.FunctionComponent<ITileInterface> = React.memo(({x, y}) => {
    const posY = y * Size.Tile;
    const posX = x * Size.Tile;
    const half = (Size.Tile + Size.Gap) / 2;
    return (
        <Circle
            opacity={1}
            x={posX + Size.Gap}
            y={posY + Size.Gap}
            radius={half}
            fillRadialGradientStartRadius={Size.Tile / 4}
            fillRadialGradientEndRadius={Size.Tile - Size.Gap}
            fillRadialGradientColorStops={[0, 'rgba(0,0,0, 1)', 1, 'rgba(0,0,0,0)']}
        />
    );
});
