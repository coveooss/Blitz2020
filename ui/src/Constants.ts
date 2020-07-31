import * as React from 'react';
import {IBlitzVisualization} from './IVisualization';

export const TILE_RATIO = 0.65;
export const GAP_RATIO = 1 - TILE_RATIO;

export const CAPTURED_TILE_RATIO = 0.8;
export const CAPTURED_GAP_RATIO = 1 - CAPTURED_TILE_RATIO;

export const font = 'Arial';
export const fontSize = 24;
export const smallFontSize = 16;
export const fontWeight = 'bold';

export const lightenColors = ['#c55353', '#8cb5da', '#dba75e', '#93c289'];
export const colors = ['#BF4040', '#79A8D4', '#D69C49', '#84B978'];
export const darkenColors = ['#ac3a3a', '#669bce', '#d19134', '#75b067'];

export const buttonColors = ['#E88F5E', '#E3D1A7', '#AAAAAA'];

export const speeds = [1000, 700, 500, 300, 100];

export const AnglePerDirection = {
    LEFT: 180,
    RIGHT: 0,
    UP: -90,
    DOWN: 90,
};

export const keyCodes = {
    Comma: ',',
    Five: '5',
    Four: '4',
    One: '1',
    Period: '.',
    Space: ' ',
    Three: '3',
    Two: '2',
    X: 'x',
    Z: 'z',
    Down: 'ArrowDown',
    Up: 'ArrowUp',
    Left: 'ArrowLeft',
    Right: 'ArrowRight',
};

export interface IVisualizationContext {
    tick: number;
    game: IBlitzVisualization;
    boardSize: number;
}

export const VisualizationContext = React.createContext<IVisualizationContext>({} as IVisualizationContext);

export class Size {
    static Tile = 50;

    static get Gap() {
        return Size.Tile * GAP_RATIO;
    }

    static get InnerTile() {
        return Size.Tile * TILE_RATIO;
    }
}
