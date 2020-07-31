import * as React from 'react';
import {Rect} from 'react-konva';

import {shallowWithContext} from '../../../tests/TestUtils';
import {Capture, ICaptureProps} from '../Capture';

const defaultProps: ICaptureProps = {
    x: 0,
    y: 0,
    playerId: 0,
};

it('should render two Rects', () => {
    const component = shallowWithContext(<Capture {...defaultProps} />);
    expect(component.find(Rect).length).toBe(2);
});
