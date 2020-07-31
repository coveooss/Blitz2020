import * as React from 'react';
import {Layer} from 'react-konva';
import {Size, VisualizationContext} from '../Constants';
import {Player} from './Player';

export const Players: React.FunctionComponent = () => {
    const {tick, game} = React.useContext(VisualizationContext);
    const positions = game.ticks[tick].players.map((p) => <Player key={`player-${p.id}`} {...p} />);
    return (
        <Layer hitGraphEnabled={false} offset={{x: -0.5 * Size.Gap, y: -0.5 * Size.Gap}}>
            {positions}
        </Layer>
    );
};
