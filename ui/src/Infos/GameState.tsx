import * as React from 'react';
import {FastLayer, Text} from 'react-konva';

import {font, fontSize, fontWeight, Size, VisualizationContext} from '../Constants';

export interface GameStateProps {
    speed?: number;
}

export const GameState: React.FunctionComponent<GameStateProps> = ({speed}) => {
    const verticalMargin = 35;
    const {boardSize, game, tick} = React.useContext(VisualizationContext);
    const y = (game.ticks[tick].players.length + 2) * verticalMargin;

    return (
        <FastLayer hitGraphEnabled={false} x={boardSize + Size.Gap} y={y}>
            <Text
                fontSize={fontSize}
                fontFamily={font}
                fontStyle={fontWeight}
                fill="red"
                shadowColor="red"
                text={`Step: ${Math.max(0, tick + 1)}`}
                align="left"
            />
            {speed && (
                <Text
                    y={verticalMargin}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill="red"
                    shadowColor="red"
                    text={`Speed: ${speed + 1}`}
                    align="right"
                />
            )}
        </FastLayer>
    );
};
