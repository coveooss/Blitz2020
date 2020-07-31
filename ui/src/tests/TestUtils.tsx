import {shallow} from 'enzyme';
import * as React from 'react';

import {IVisualizationContext} from '../Constants';
import {IBlitzVisualization, IPlayer, IPosition} from '../IVisualization';
import {game} from '../mock/Mock';

const getMockContext = (props: Partial<IVisualizationContext> = {}) => ({
    tick: 0,
    speed: 1,
    isPaused: false,
    game: {...game},
    boardSize: 200,
    ...props,
});

export const getMockGameWithMap = (map: string[][]): IBlitzVisualization => {
    return {...game, ticks: [{...game.ticks[0], game: {...game.ticks[0].game, map}}]};
};

export const getMockGameWithPlayers = (players: IPlayer[]): IBlitzVisualization => {
    return {...game, ticks: [{...game.ticks[0], players: players}]};
};

export const getMockGameWithTail = (tail: IPosition[]): IBlitzVisualization => {
    return {...game, ticks: [{...game.ticks[0], players: [{...game.ticks[0].players[0], tail}]}]};
};

export const shallowWithContext = (children: React.ReactElement, props: Partial<IVisualizationContext> = {}) => {
    jest.spyOn(React, 'useContext').mockImplementation(() => getMockContext(props));
    return shallow(children);
};
