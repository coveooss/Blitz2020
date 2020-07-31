import * as React from 'react';
import {Circle, Path} from 'react-konva';
import {colors, Size} from '../../Constants';
import {ITileInterface} from './TilesInterface';

const ringPath =
    'M42.83,18.418C47.291,19.966,50,22.209,50,25C50,30.471,39.551,33.848,25.933,33.995L25,34C10.929,34,0,30.596,0,25C0,22.213,2.71,19.97,7.17,18.42C4.767,23.253,4,24.016,4,24.499C4,25.303,6.115,26.876,9.726,28.013C13.736,29.275,19.183,30,25,30C30.817,30,36.263,29.275,40.274,28.013C43.885,26.876,46,25.303,46,24.499C46,24.019,45.234,23.25,43.834,22.474Z';
export interface IPlanetProps extends ITileInterface {
    playerId: number | null;
}

export const Planet: React.FunctionComponent<IPlanetProps> = React.memo(({x, y, playerId}) => {
    const posY = y * Size.Tile;
    const posX = x * Size.Tile;
    const half = Size.InnerTile / 2;
    const pathSize = 37;
    const tileSizeInMockup = 50;
    const pathScale = ((tileSizeInMockup / pathSize) * Size.InnerTile) / tileSizeInMockup;
    const color = playerId !== null ? colors[playerId] : '#EBEBEB';
    return (
        <>
            <Circle
                fill={color}
                x={posX + Size.Gap}
                y={posY + Size.Gap}
                radius={half}
                shadowColor={color}
                shadowBlur={Size.Tile / 5}
                shadowOpacity={1}
            />
            <Circle fill={color} x={posX + Size.Gap} y={posY + Size.Gap} radius={half} />
            <Path
                data={ringPath}
                fill="#FFF"
                width={Size.Tile}
                height={Size.Tile}
                scale={{x: pathScale, y: pathScale}}
                x={posX - Size.Gap / 4}
                y={posY - Size.Gap / 4}
            />
        </>
    );
});
