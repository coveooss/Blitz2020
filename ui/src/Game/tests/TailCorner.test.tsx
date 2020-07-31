import * as React from 'react';
import {Group, Path} from 'react-konva';

import {shallowWithContext} from '../../tests/TestUtils';
import {ITailCornerProps, TailCorner} from '../TailCorner';

const defaultProps: ITailCornerProps = {
    x: 0,
    y: 0,
    color: 'blue',
    lineSize: 10,
    previous: {x: 0, y: 0},
    next: {x: 1, y: 1},
};

it('should render a two groups and a path', () => {
    const component = shallowWithContext(<TailCorner {...defaultProps} />);
    expect(component.find(Group).length).toBe(2);
    expect(component.find(Path).length).toBe(1);
});

it('should render a corner for up-right corners part of the tail', () => {
    const positionProps = {
        previous: {x: 0, y: 1},
        x: 0,
        y: 0,
        next: {x: 1, y: 0},
    };

    const tailCorner = shallowWithContext(<TailCorner {...defaultProps} {...positionProps} />);

    expect(tailCorner.children().prop('rotation')).toBe(0);
});

it('should render a corner for up-left corners part of the tail', () => {
    const positionProps = {
        previous: {x: 1, y: 1},
        x: 1,
        y: 0,
        next: {x: 0, y: 0},
    };

    const tailCorner = shallowWithContext(<TailCorner {...defaultProps} {...positionProps} />);

    expect(tailCorner.children().prop('rotation')).toBe(90);
});

it('should render a corner for down-right corners part of the tail', () => {
    const positionProps = {
        previous: {x: 0, y: 0},
        x: 0,
        y: 1,
        next: {x: 1, y: 1},
    };

    const tailCorner = shallowWithContext(<TailCorner {...defaultProps} {...positionProps} />);

    expect(tailCorner.children().prop('rotation')).toBe(-90);
});

it('should render a corner for down-left corners part of the tail', () => {
    const positionProps = {
        previous: {x: 1, y: 0},
        x: 1,
        y: 1,
        next: {x: 0, y: 1},
    };

    const tailCorner = shallowWithContext(<TailCorner {...defaultProps} {...positionProps} />);

    expect(tailCorner.children().prop('rotation')).toBe(180);
});

it('should render a corner for left-up corners part of the tail', () => {
    const positionProps = {
        previous: {x: 1, y: 1},
        x: 0,
        y: 1,
        next: {x: 0, y: 0},
    };

    const tailCorner = shallowWithContext(<TailCorner {...defaultProps} {...positionProps} />);

    expect(tailCorner.children().prop('rotation')).toBe(-90);
});

it('should render a corner for right-up corners part of the tail', () => {
    const positionProps = {
        previous: {x: 0, y: 1},
        x: 1,
        y: 1,
        next: {x: 1, y: 0},
    };

    const tailCorner = shallowWithContext(<TailCorner {...defaultProps} {...positionProps} />);

    expect(tailCorner.children().prop('rotation')).toBe(180);
});

it('should render a corner for left-down corners part of the tail', () => {
    const positionProps = {
        previous: {x: 1, y: 0},
        x: 0,
        y: 0,
        next: {x: 0, y: 1},
    };

    const tailCorner = shallowWithContext(<TailCorner {...defaultProps} {...positionProps} />);

    expect(tailCorner.children().prop('rotation')).toBe(0);
});

it('should render a corner for right-down corners part of the tail', () => {
    const positionProps = {
        previous: {x: 0, y: 0},
        x: 1,
        y: 0,
        next: {x: 1, y: 1},
    };

    const tailCorner = shallowWithContext(<TailCorner {...defaultProps} {...positionProps} />);

    expect(tailCorner.children().prop('rotation')).toBe(90);
});
