import * as React from 'react';
import {Group, Path} from 'react-konva';
import {IPosition} from 'src/IVisualization';

import {CAPTURED_GAP_RATIO, Size} from '../Constants';

export interface ITailCornerProps extends IPosition {
    previous: IPosition;
    next: IPosition;
    color: string;
    lineSize: number;
}

export const TailCorner: React.FunctionComponent<ITailCornerProps> = ({x, y, previous, next, lineSize, color}) => {
    const long = Size.Tile / 2 + lineSize;

    let angle: number;

    if (previous.x === x - 1 && next.y === y - 1) {
        angle = 180;
    } else if (previous.x === x - 1 && next.y === y + 1) {
        angle = 90;
    } else if (previous.x === x + 1 && next.y === y - 1) {
        angle = -90;
    } else if (previous.x === x + 1 && next.y === y + 1) {
        angle = 0;
    } else if (previous.y === y - 1 && next.x === x - 1) {
        angle = 180;
    } else if (previous.y === y - 1 && next.x === x + 1) {
        angle = -90;
    } else if (previous.y === y + 1 && next.x === x - 1) {
        angle = 90;
    } else {
        angle = 0;
    }

    return (
        <Group x={Size.Tile * x - Size.Gap / 2} y={Size.Tile * y - Size.Gap / 2}>
            <Group rotation={angle} x={Size.Tile / 2} y={Size.Tile / 2}>
                <Path
                    fill={color}
                    data={`M${long} 0 L0 0 L0 ${long} L${lineSize} ${long} L${lineSize} ${lineSize} L${long} ${lineSize} Z`}
                    width={lineSize}
                    height={Size.Tile / 2}
                    offset={{x: lineSize / 2, y: lineSize / 2}}
                    shadowColor={'#000'}
                    shadowOffset={{
                        x: (-CAPTURED_GAP_RATIO / 2) * Size.InnerTile,
                        y: (CAPTURED_GAP_RATIO / 2) * Size.InnerTile,
                    }}
                    shadowOpacity={0.3}
                />
            </Group>
        </Group>
    );
};
