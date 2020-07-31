export interface IPosition {
    x: number;
    y: number;
}

export interface IStats {
    number_of_captured_tiles?: number;
    number_of_mines_captured?: number;
    number_of_suicides?: number;
    players_killed?: any;
    killed_by_players?: any;
}

export interface IPlayer {
    active: boolean;
    killed: boolean;
    position: IPosition;
    spawn_position: IPosition;
    direction: string;
    tail: IPosition[];
    id: number;
    name: string;
    score: number;
    stats: IStats;
    history: [];
}

export interface ITick {
    type: string;
    game: {
        map: string[][];
        player_id: number;
        tick: number;
        ticks_left: number;
    };
    players: IPlayer[];
}

export interface IBlitzVisualization {
    ticks: ITick[];
    players?: string[];
    winner?: string;
}
