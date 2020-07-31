import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {keyCodes} from '../Constants';
import {KeyHandler} from '../Controls/KeyHandler';
import {ITick} from '../IVisualization';
import {LiveViewer} from '../LiveViewer';

const root = document.querySelector('.root');

const HumanBotApp: React.FunctionComponent = () => {
    const [tick, setTick] = React.useState<ITick>();
    const [socket, setSocket] = React.useState<WebSocket>();

    const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        const action = {
            [keyCodes.Up]: 'FORWARD',
            [keyCodes.Left]: 'TURN_LEFT',
            [keyCodes.Right]: 'TURN_RIGHT',
        }[e.key];

        if (tick && socket && action) {
            socket.send(JSON.stringify({type: 'move', action, tick: tick.game.tick}));
        }
    };

    React.useEffect(() => {
        const ws = new WebSocket('ws://' + window.location.hostname + ':8765');

        ws.onopen = () => {
            ws.send(JSON.stringify({type: 'register', name: 'human'}));
        };

        ws.onmessage = (event) => {
            setTick(JSON.parse(event.data));
        };

        setSocket(ws);
    }, []);

    if (!tick) {
        return null;
    }

    const height = root!.clientHeight;
    const width = root!.clientWidth;

    const ticks = new Array(tick.game.tick + tick.game.ticks_left);
    ticks[tick.game.tick] = tick;

    return (
        <KeyHandler onKeyDown={onKeyDown}>
            <LiveViewer width={width} height={height} game={{ticks}} tick={tick.game.tick} />
        </KeyHandler>
    );
};

ReactDOM.render(<HumanBotApp />, root);
