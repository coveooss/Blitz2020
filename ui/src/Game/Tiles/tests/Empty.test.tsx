import * as React from 'react';
import {Rect} from 'react-konva';

import {shallowWithContext} from '../../../tests/TestUtils';
import {Empty} from '../Empty';
import {ITileInterface} from '../TilesInterface';

const defaultProps: ITileInterface = {
    x: 0,
    y: 0,
};

it('should render a Rects', () => {
    const component = shallowWithContext(<Empty {...defaultProps} />);
    expect(component.find(Rect).exists()).toBe(true);
});
