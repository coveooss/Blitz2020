import * as React from 'react';
import {FastLayer} from 'react-konva';
import {Size} from '../../Constants';

import {getMockGameWithMap, shallowWithContext} from '../../tests/TestUtils';
import {Board} from '../Board';
import {BlackHole, Capture, Empty} from '../Tiles';

it('should render a FastLayer', () => {
    const component = shallowWithContext(<Board />);
    expect(component.find(FastLayer).exists()).toBe(true);
});

it('should offset the FastLayer by half the gap', () => {
    const component = shallowWithContext(<Board />);
    expect(component.find(FastLayer).prop('offset')).toEqual({x: -Size.Gap / 2, y: -Size.Gap / 2});
});

it('should render an Empty tile for every empty space', () => {
    const map = [
        ['W', 'W', 'W'],
        [' ', 'W', ' '],
        ['W', 'W', 'W'],
    ];
    const component = shallowWithContext(<Board />, {game: getMockGameWithMap(map)});

    expect(component.find(Empty).length).toBe(2);
});

it('should render a Capture for every captured tiles', () => {
    const map = [
        ['C-1', 'C-4'],
        [' ', 'C-0'],
    ];
    const component = shallowWithContext(<Board />, {game: getMockGameWithMap(map)});

    expect(component.find(Capture).length).toBe(3);
});

it('should render a Blackhole for every blackhole tiles', () => {
    const map = [
        ['C-1', '!'],
        ['!', 'W'],
    ];
    const component = shallowWithContext(<Board />, {game: getMockGameWithMap(map)});

    expect(component.find(BlackHole).length).toBe(2);
});

it('should render an Empty tile for all unknown tiles', () => {
    const map = [
        ['D-1', 'E-1', 'C-'],
        ['C--1', 'A', ' '],
        [' ', 'Z', 'K'],
    ];
    const component = shallowWithContext(<Board />, {game: getMockGameWithMap(map)});

    expect(component.find(Empty).length).toBe(9);
});

it('should have one children per map square', () => {
    const map = [
        ['W', 'W', 'W'],
        ['W', ' ', 'W'],
        ['W', 'W', 'W'],
    ];
    const component = shallowWithContext(<Board />, {game: getMockGameWithMap(map)});

    const mapLength = map.reduce((acc, row) => acc + row.length, 0);
    expect(component.find(FastLayer).children().length).toBe(mapLength);
});
