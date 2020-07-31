import * as React from 'react';
import {Layer, Rect} from 'react-konva';

import {Size} from '../../Constants';
import {getMockGameWithTail, shallowWithContext} from '../../tests/TestUtils';
import {TailCorner} from '../TailCorner';
import {Tails} from '../Tails';

it('should render a Layer', () => {
    const component = shallowWithContext(<Tails />);
    expect(component.find(Layer).exists()).toBe(true);
});

it('should offset the Layer by half the gap', () => {
    const component = shallowWithContext(<Tails />);
    expect(component.find(Layer).prop('offset')).toEqual({x: -Size.Gap / 2, y: -Size.Gap / 2});
});

it('should render a Rect for every horizontal straight part of the tail (except the one under the player)', () => {
    const tail = [
        {x: 0, y: 0},
        {x: 1, y: 0},
        {x: 2, y: 0},
    ];
    const component = shallowWithContext(<Tails />, {game: getMockGameWithTail(tail)});
    expect(component.find(Rect).length).toBe(tail.length - 1);
});

it('should render a Rect for every vertical straight part of the tail (except the one under the player)', () => {
    const tail = [
        {x: 0, y: 0},
        {x: 0, y: 1},
        {x: 0, y: 2},
    ];
    const component = shallowWithContext(<Tails />, {game: getMockGameWithTail(tail)});
    expect(component.find(Rect).length).toBe(tail.length - 1);
});

it('should render a TailCorner when the tail makes a corner', () => {
    const tail = [
        {x: 0, y: 1},
        {x: 0, y: 0},
        {x: 1, y: 0},
        {x: 1, y: 0},
    ];
    const component = shallowWithContext(<Tails />, {game: getMockGameWithTail(tail)});

    expect(component.find(TailCorner).exists()).toBe(true);
});
