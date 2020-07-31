import {shallow} from 'enzyme';
import * as React from 'react';
import {ILiveViewerProps, LiveViewer} from '../LiveViewer';

import {game} from '../mock/Mock';
import {Visualization} from '../Visualization';

const defaultProps: ILiveViewerProps = {
    game,
    height: 500,
    width: 500,
    tick: 0,
};

it('should not throw on render', () => {
    expect(() => shallow(<LiveViewer {...defaultProps} />)).not.toThrow();
});

it('should render a Visualization', () => {
    const component = shallow(<LiveViewer {...defaultProps} />);
    expect(component.find(Visualization).exists()).toBe(true);
});
