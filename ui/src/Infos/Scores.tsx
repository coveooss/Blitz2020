import * as React from 'react';
import {FastLayer, Text} from 'react-konva';
import {colors, font, fontSize, fontWeight, Size, VisualizationContext} from '../Constants';

export const Scores: React.FunctionComponent = () => {
    const verticalMargin = 35;
    const {boardSize, game, tick} = React.useContext(VisualizationContext);
    const teamNameMaxLength = 200;
    const getTeamOffset = (i: number) => i * verticalMargin;
    const scores = game.ticks[tick].players.map(({id, name, score}, i: number) => {
        const y = getTeamOffset(i) + verticalMargin;
        const color = colors[i];
        return (
            <React.Fragment key={`player-score-${id}`}>
                <Text
                    y={y}
                    width={teamNameMaxLength}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill={color}
                    shadowColor={color}
                    text={name}
                    align="left"
                    wrap="none"
                    ellipsis
                />
                <Text
                    x={teamNameMaxLength}
                    y={y}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill={color}
                    shadowColor={color}
                    text={score.toFixed(2)}
                    align="left"
                />
            </React.Fragment>
        );
    });

    return (
        <FastLayer hitGraphEnabled={false} x={boardSize + Size.Gap}>
            <Text
                fontSize={fontSize}
                fontFamily={font}
                fontStyle={fontWeight}
                fill="#6EE4CE"
                shadowColor="#6EE4CE"
                text="Team"
                align="left"
            />
            {scores}
        </FastLayer>
    );
};
