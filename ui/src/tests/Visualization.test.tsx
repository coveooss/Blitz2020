import {shallow} from 'enzyme';
import * as React from 'react';

import {Background, Board, Players, Tails} from '../Game';
import {Visualization} from '../Visualization';

it('should not throw', () => {
    expect(() => shallow(<Visualization />)).not.toThrow();
});

it(`should contain the game components`, () => {
    const component = shallow(<Visualization />);

    expect(component.find(Background).exists()).toBe(true);
    expect(component.find(Board).exists()).toBe(true);
    expect(component.find(Players).exists()).toBe(true);
    expect(component.find(Tails).exists()).toBe(true);
});
