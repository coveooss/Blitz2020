import * as React from 'react';
import {Stage} from 'react-konva';
import {keyCodes, Size, speeds, VisualizationContext} from './Constants';
import {KeyHandler} from './Controls/KeyHandler';
import {Infos} from './Infos/Infos';
import {IBlitzVisualization} from './IVisualization';
import {Visualization} from './Visualization';

export interface IReplayViewerProps {
    game: IBlitzVisualization;
    width: number;
    height: number;
    onEnd?: () => void;
}

export const ReplayViewer: React.FunctionComponent<IReplayViewerProps> = ({width, height, game, onEnd}) => {
    const [tick, setTick] = React.useState(0);
    const [speed, setSpeed] = React.useState(0);
    const [isPaused, setIsPaused] = React.useState(false);

    const numberOfTile: number = game.ticks[tick].game.map.length;
    const boardSize = Math.min(height, Math.min(width - 250));

    Size.Tile = boardSize / numberOfTile;

    const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        const gameStart = 0;
        const gameMax = game.ticks.length - 1;
        switch (e.key) {
            case keyCodes.Space:
                setIsPaused(!isPaused);
                break;
            case keyCodes.Z:
                setTick(gameStart);
                break;
            case keyCodes.X:
                setTick(gameMax);
                break;
            case keyCodes.Comma:
                setTick(Math.max(tick - 1, gameStart));
                break;
            case keyCodes.Period:
                setTick(Math.min(tick + 1, gameMax));
                break;
            case keyCodes.One:
                setSpeed(0);
                break;
            case keyCodes.Two:
                setSpeed(1);
                break;
            case keyCodes.Three:
                setSpeed(2);
                break;
            case keyCodes.Four:
                setSpeed(3);
                break;
            case keyCodes.Five:
                setSpeed(4);
                break;
            default:
                break;
        }
    };

    React.useEffect(() => {
        if (!isPaused) {
            const lastTick = game.ticks.length;
            const newTick = Math.min(tick + 1, lastTick);
            let timeout: number;
            if (newTick === lastTick && onEnd) {
                // After 5 seconds, call the onEnd Props
                timeout = window.setTimeout(onEnd, 5000);
            } else {
                // play next game tick
                timeout = window.setTimeout(() => setTick(newTick), speeds[speed]);
            }
            return () => window.clearTimeout(timeout);
        }
        return undefined;
    }, [tick, isPaused, speed]);

    return (
        <KeyHandler onKeyDown={onKeyDown}>
            <Stage width={width} height={height}>
                <VisualizationContext.Provider value={{tick, boardSize, game}}>
                    <Visualization />
                    <Infos speed={speed} />
                </VisualizationContext.Provider>
            </Stage>
        </KeyHandler>
    );
};
