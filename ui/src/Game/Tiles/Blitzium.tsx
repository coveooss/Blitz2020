import * as React from 'react';
import {Path} from 'react-konva';

import {Size} from '../../Constants';
import {ITileInterface} from './TilesInterface';

const shapes = ['M14,33L41,21L14,42Z', 'M14,9L41,21L14,33Z', 'M14,0V27L41,21Z'];
const shapeColors = ['#dc7704', '#f58020', '#ff9844'];

export const Blitzium: React.FunctionComponent<ITileInterface> = React.memo(({x, y}) => {
    const posY = y * Size.Tile;
    const posX = x * Size.Tile;
    const pathSize = 42;
    const tileSizeInMockup = 50;
    const pathScale = ((tileSizeInMockup / pathSize) * Size.InnerTile) / tileSizeInMockup;
    return (
        <>
            <Path
                key="background"
                data="M14,42L41,21L14,0Z"
                fill={shapeColors[1]}
                shadowColor={shapeColors[1]}
                shadowBlur={Size.Tile / 4}
                shadowOpacity={1}
                width={Size.InnerTile}
                height={Size.InnerTile}
                scale={{x: pathScale, y: pathScale}}
                x={posX}
                y={posY}
            />
            {shapes.map((shape: string, i: number) => (
                <Path
                    key={`shape-${i}`}
                    data={shape}
                    fill={shapeColors[i]}
                    width={Size.InnerTile}
                    height={Size.InnerTile}
                    scale={{x: pathScale, y: pathScale}}
                    x={posX}
                    y={posY}
                />
            ))}
        </>
    );
});
