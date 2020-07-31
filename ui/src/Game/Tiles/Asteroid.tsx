import * as Konva from 'konva';
import * as React from 'react';
import {Rect, RegularPolygon} from 'react-konva';

import {Size} from '../../Constants';
import {ITileInterface} from './TilesInterface';

export const Asteroid: React.FunctionComponent<ITileInterface> = React.memo(({x, y}) => {
    const posY = y * Size.Tile - Size.Gap / 2;
    const posX = x * Size.Tile - Size.Gap / 2;

    const tileSizeInMockup = 50;
    const scaleOffset = (pos: number) => (pos / tileSizeInMockup) * Size.Tile;

    return (
        <>
            <Rock x={posX + scaleOffset(5)} y={posY + scaleOffset(7)} />
            <Rock x={posX + scaleOffset(25)} y={posY + scaleOffset(5)} />
            <Rock x={posX + scaleOffset(20)} y={posY + scaleOffset(15)} />
            <Rock x={posX + scaleOffset(35)} y={posY + scaleOffset(20)} />
            <Rock x={posX + scaleOffset(10)} y={posY + scaleOffset(30)} />
            <Rock x={posX + scaleOffset(20)} y={posY + scaleOffset(40)} />
            <Rock x={posX + scaleOffset(40)} y={posY + scaleOffset(46)} />
            <BigRock x={posX + scaleOffset(40)} y={posY + scaleOffset(10)} />
            <BigRock x={posX + scaleOffset(10)} y={posY + scaleOffset(22)} />
            <BigRock x={posX + scaleOffset(25)} y={posY + scaleOffset(30)} />
            <BigRock x={posX + scaleOffset(40)} y={posY + scaleOffset(37)} />
            <BigRock x={posX + scaleOffset(10)} y={posY + scaleOffset(45)} />
        </>
    );
});

const Rock: React.FunctionComponent<ITileInterface> = React.memo(
    (props) => {
        const ref = React.useRef<Konva.default.Rect>(null);
        const size = 0.1 * Size.Tile;
        return (
            <Rect
                {...props}
                ref={ref}
                width={size}
                height={size}
                fill="#B5C4CF"
                shadowOffset={{x: size / 3, y: size / 3}}
                shadowColor="#000"
                shadowOpacity={0.1}
            />
        );
    },
    () => true
);

const BigRock: React.FunctionComponent<ITileInterface> = React.memo(
    (props) => {
        const size = 0.2 * Size.Tile;
        return (
            <RegularPolygon
                {...props}
                radius={size / 2}
                sides={6}
                fill="#B5C4CF"
                shadowOffset={{x: size / 3, y: size / 3}}
                shadowColor="#000"
                shadowOpacity={0.1}
            />
        );
    },
    () => true
);
