import * as React from 'react';
import {Rect} from 'react-konva';

import {GAP_RATIO, Size} from '../../Constants';
import {ITileInterface} from './TilesInterface';

export const Empty: React.FunctionComponent<ITileInterface> = React.memo(({x, y}) => {
    return (
        <Rect
            fill="#F2F2F2"
            opacity={0.2}
            width={Size.InnerTile}
            height={Size.InnerTile}
            x={x * Size.Tile}
            y={y * Size.Tile}
            shadowColor="rgb(45,41,38)"
            shadowOffset={{x: (-GAP_RATIO / 2) * Size.InnerTile, y: (GAP_RATIO / 2) * Size.InnerTile}}
            shadowOpacity={0.3}
        />
    );
});
