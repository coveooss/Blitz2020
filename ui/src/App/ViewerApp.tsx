import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {ITick} from '../IVisualization';
import {LiveViewer} from '../LiveViewer';

const root = document.querySelector('.root');

const ViewerApp: React.FunctionComponent = () => {
    const [tick, setTick] = React.useState<ITick>();

    const retry = () => window.setTimeout(start, 1000);

    function start() {
        const ws = new WebSocket('ws://' + window.location.hostname + ':8765');

        ws.onerror = retry;
        ws.onclose = retry;
        ws.onopen = () => {
            ws.send(JSON.stringify({type: 'viewer'}));
        };
        ws.onmessage = (event) => {
            setTick(JSON.parse(event.data));
        };
    }

    React.useEffect(start, []);

    if (!tick) {
        return null;
    }

    const height = root!.clientHeight;
    const width = root!.clientWidth;

    const ticks = new Array(tick.game.tick + tick.game.ticks_left);
    ticks[tick.game.tick] = tick;

    return <LiveViewer width={width} height={height} game={{ticks}} tick={tick?.game.tick} />;
};

ReactDOM.render(<ViewerApp />, root);
