import * as React from 'react';
import {Rect} from 'react-konva';
import {CAPTURED_GAP_RATIO, colors, Size} from '../../Constants';
import {ITileInterface} from './TilesInterface';

export interface ICaptureProps extends ITileInterface {
    playerId: number;
}

export const Capture: React.FunctionComponent<ICaptureProps> = React.memo(({x, y, playerId}) => {
    const posY = y * Size.Tile;
    const posX = x * Size.Tile;
    return (
        <>
            <Rect
                fill={colors[playerId]}
                shadowColor={colors[playerId]}
                shadowBlur={Size.InnerTile}
                shadowOpacity={0.5}
                width={Size.InnerTile}
                height={Size.InnerTile}
                x={posX}
                y={posY}
            />
            <Rect
                fill={colors[playerId]}
                width={Size.InnerTile}
                height={Size.InnerTile}
                x={posX}
                y={posY}
                shadowColor="#000"
                shadowOffset={{
                    x: (-CAPTURED_GAP_RATIO / 2) * Size.InnerTile,
                    y: (CAPTURED_GAP_RATIO / 2) * Size.InnerTile,
                }}
                shadowOpacity={0.3}
            />
        </>
    );
});
