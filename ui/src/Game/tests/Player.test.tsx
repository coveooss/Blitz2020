import * as React from 'react';
import {Path} from 'react-konva';
import {AnglePerDirection} from '../../Constants';
import {shallowWithContext} from '../../tests/TestUtils';
import {Player} from '../Player';

const defaultProps = {
    direction: 'LEFT',
    id: 0,
    position: {x: 0, y: 0},
};

it('should render a Path', () => {
    const component = shallowWithContext(<Player {...defaultProps} />);
    expect(component.find(Path).exists()).toBe(true);
});

Object.entries(AnglePerDirection).forEach(([direction, angle]) => {
    it(`should rotate the group relative to the dir: ${direction}`, () => {
        const component = shallowWithContext(<Player {...defaultProps} direction={direction} />);
        expect(component.findWhere((el) => el.prop('id') === 'rotation').prop('rotation')).toBe(angle);
    });
});
