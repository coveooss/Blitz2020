import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {IBlitzVisualization} from '../IVisualization';
import {ReplayViewer} from '../ReplayViewer';

const root = document.querySelector('.root');
const height = root!.clientHeight;
const width = root!.clientWidth;

const ReplayApp = () => {
    const [data, setData] = React.useState<IBlitzVisualization>();
    const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (files?.length === 1) {
            const reader = new FileReader();
            reader.readAsText(files[0], 'UTF-8');
            reader.onload = (evt) => {
                try {
                    const game = JSON.parse(evt?.target?.result as string);
                    setData(game);
                } catch (e) {
                    alert('game file parsing failed');
                }
            };
        }
    };

    if (data) {
        return <ReplayViewer width={width} height={height} game={data} />;
    }
    return <input type="file" onChange={onChange} />;
};

ReactDOM.render(<ReplayApp />, root);
