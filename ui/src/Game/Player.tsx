import * as React from 'react';
import {Group, Path} from 'react-konva';
import {AnglePerDirection, CAPTURED_GAP_RATIO, lightenColors, Size} from '../Constants';
import {IPlayer} from '../IVisualization';

export type IPlayerProps = Pick<IPlayer, 'position' | 'id' | 'direction'>;

export const Player: React.FunctionComponent<IPlayerProps> = ({position, id, direction}) => {
    const {x, y} = position;

    const lengthInMockup = 63;
    const tileSizeInMockup = 50;
    const pathScale = ((lengthInMockup / tileSizeInMockup) * Size.Tile) / lengthInMockup;
    return (
        <Group id="position" x={Size.Tile * x - Size.Gap / 2} y={Size.Tile * y - Size.Gap / 2}>
            <Group id="rotation" rotation={AnglePerDirection[direction]} x={Size.Tile / 2} y={Size.Tile / 2}>
                <Group id="offset" offset={{x: Size.Tile / 2 + Size.Gap / 2, y: Size.Tile / 2 - Size.Gap / 4}}>
                    <Path
                        data="M10,14L0,9V4l16-4l11,9c18-2,31,4,36,12l0,0c-5,8-18,14-36,12l-11,9L0,38v-5l10-5V14z"
                        scale={{x: pathScale, y: pathScale}}
                        fill={lightenColors[id]}
                        shadowColor="#000"
                        shadowOffset={{
                            x: (-CAPTURED_GAP_RATIO / 2) * Size.InnerTile,
                            y: (CAPTURED_GAP_RATIO / 2) * Size.InnerTile,
                        }}
                        shadowOpacity={0.6}
                        shadowBlur={Size.Gap / 2}
                    />
                </Group>
            </Group>
        </Group>
    );
};
