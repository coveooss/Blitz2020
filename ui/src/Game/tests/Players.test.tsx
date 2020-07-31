import * as React from 'react';
import {Layer} from 'react-konva';
import {Size} from '../../Constants';
import {IPlayer} from '../../IVisualization';
import {game} from '../../mock/Mock';

import {getMockGameWithPlayers, shallowWithContext} from '../../tests/TestUtils';
import {Player} from '../Player';
import {Players} from '../Players';

it('should render a Layer', () => {
    const component = shallowWithContext(<Players />);
    expect(component.find(Layer).exists()).toBe(true);
});

it('should offset the Layer by half the gap', () => {
    const component = shallowWithContext(<Players />);
    expect(component.find(Layer).prop('offset')).toEqual({x: -Size.Gap / 2, y: -Size.Gap / 2});
});

it('should render a Player per player', () => {
    const players: IPlayer[] = [
        {...game.ticks[0].players[0], id: 7},
        {...game.ticks[0].players[0], id: 42},
        {...game.ticks[0].players[0], id: 1},
    ];
    const component = shallowWithContext(<Players />, {game: getMockGameWithPlayers(players)});

    expect(component.find(Player).length).toBe(players.length);
});
