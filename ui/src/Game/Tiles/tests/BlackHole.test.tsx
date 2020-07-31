import * as React from 'react';
import {Circle} from 'react-konva';

import {shallowWithContext} from '../../../tests/TestUtils';
import {BlackHole} from '../BlackHole';
import {ITileInterface} from '../TilesInterface';

const defaultProps: ITileInterface = {
    x: 0,
    y: 0,
};

it('should render a Circle', () => {
    const component = shallowWithContext(<BlackHole {...defaultProps} />);
    expect(component.find(Circle).exists()).toBe(true);
});
