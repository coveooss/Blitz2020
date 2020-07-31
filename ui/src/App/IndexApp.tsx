import * as React from 'react';
import * as ReactDOM from 'react-dom';

const root = document.querySelector('.root');

const IndexApp = () => {
    return (
        <>
            <a href="/viewer.html">Viewer</a>
            <a href="/human_bot.html">Human bot</a>
            <a href="/replay.html">Replay</a>
        </>
    );
};

ReactDOM.render(<IndexApp />, root);
