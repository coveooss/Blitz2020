import * as React from 'react';
import {FastLayer, Rect} from 'react-konva';

import {shallowWithContext} from '../../tests/TestUtils';
import {Background} from '../Background';

it('should render a FastLayer', () => {
    const component = shallowWithContext(<Background />);
    expect(component.find(FastLayer).exists()).toBe(true);
});

it('should render a backgorund & a gradient', () => {
    const component = shallowWithContext(<Background />);

    expect(component.find(Rect).length).toBe(2);
});
