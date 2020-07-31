import * as React from 'react';

import {shallowWithContext} from '../../../tests/TestUtils';
import {Asteroid} from '../Asteroid';
import {ITileInterface} from '../TilesInterface';

const defaultProps: ITileInterface = {
    x: 0,
    y: 0,
};

it('should have some children', () => {
    const component = shallowWithContext(<Asteroid {...defaultProps} />);
    expect(component.children().length).toBeGreaterThan(0);
});
