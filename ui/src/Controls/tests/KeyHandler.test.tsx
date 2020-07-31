import {shallow} from 'enzyme';
import * as React from 'react';
import {KeyHandler} from '../KeyHandler';

it('should focus on the input when the user click on the container', () => {
    const focusSpy = jest.fn();
    jest.spyOn(React, 'useRef').mockImplementation(() => ({
        current: {focus: focusSpy},
    }));
    const component = shallow(<KeyHandler onKeyDown={jest.fn} />);
    component.simulate('click');

    expect(focusSpy).toHaveBeenCalledTimes(1);
});

it('should call the onKeyDown prop when the user press a key', () => {
    const spy = jest.fn();
    const component = shallow(<KeyHandler onKeyDown={spy} />);
    component.find('input').simulate('keyDown', {key: '👋'});

    expect(spy).toHaveBeenCalledTimes(1);
});
