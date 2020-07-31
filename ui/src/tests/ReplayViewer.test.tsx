import {shallow} from 'enzyme';
import * as React from 'react';
import {keyCodes} from '../Constants';
import {KeyHandler} from '../Controls/KeyHandler';

import {game} from '../mock/Mock';
import {IReplayViewerProps, ReplayViewer} from '../ReplayViewer';

const defaultProps: IReplayViewerProps = {
    game,
    height: 500,
    width: 500,
};

it('should not throw on render', () => {
    expect(() => shallow(<ReplayViewer {...defaultProps} />)).not.toThrow();
});

it('should call useEffect when the user press some keys', () => {
    const spy = spyOn(React, 'useEffect');
    const component = shallow(<ReplayViewer {...defaultProps} />);

    const simulateKeyDown = (key: string) => component.find(KeyHandler).prop('onKeyDown')({key} as any);

    let count = 1;
    simulateKeyDown(keyCodes.Space);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.Comma);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.Period);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.One);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.Two);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.Three);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.Four);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.Five);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.X);
    expect(spy).toHaveBeenCalledTimes(++count);

    simulateKeyDown(keyCodes.Z);
    expect(spy).toHaveBeenCalledTimes(++count);
});

it('should not call useEffect when the user press a non-binded key', () => {
    const spy = spyOn(React, 'useEffect');
    const component = shallow(<ReplayViewer {...defaultProps} />);
    spy.calls.reset();

    const simulateKeyDown = (key: string) => component.find(KeyHandler).prop('onKeyDown')({key} as any);
    simulateKeyDown('w');
    simulateKeyDown('o');
    simulateKeyDown('w');

    expect(spy).not.toHaveBeenCalled();
});
