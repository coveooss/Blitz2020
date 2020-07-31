import {IBlitzVisualization} from '../IVisualization';

export const game: IBlitzVisualization = {
    ticks: [
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', ' ', 'C-0', ' ', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 1,
                ticks_left: 9,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 2,
                        y: 1,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'UP',
                    tail: [
                        {
                            x: 2,
                            y: 1,
                        },
                    ],
                    id: 0,
                    name: 'human',
                    score: 0.02,
                    stats: {
                        number_of_captured_tiles: 1,
                        number_of_mines_captured: 0,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', ' ', 'C-0', ' ', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 2,
                ticks_left: 8,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 1,
                        y: 1,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'LEFT',
                    tail: [
                        {
                            x: 2,
                            y: 1,
                        },
                        {
                            x: 1,
                            y: 1,
                        },
                    ],
                    id: 0,
                    name: 'human',
                    score: 0.04,
                    stats: {
                        number_of_captured_tiles: 1,
                        number_of_mines_captured: 0,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 3,
                ticks_left: 7,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 1,
                        y: 2,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'DOWN',
                    tail: [],
                    id: 0,
                    name: 'human',
                    score: 3.12,
                    stats: {
                        number_of_captured_tiles: 4,
                        number_of_mines_captured: 0,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 4,
                ticks_left: 6,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 1,
                        y: 3,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'DOWN',
                    tail: [
                        {
                            x: 1,
                            y: 3,
                        },
                    ],
                    id: 0,
                    name: 'human',
                    score: 3.2,
                    stats: {
                        number_of_captured_tiles: 4,
                        number_of_mines_captured: 0,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 5,
                ticks_left: 5,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 2,
                        y: 3,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'RIGHT',
                    tail: [],
                    id: 0,
                    name: 'human',
                    score: 5.319999999999998,
                    stats: {
                        number_of_captured_tiles: 6,
                        number_of_mines_captured: 0,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', 'C-0', 'C-0', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 6,
                ticks_left: 4,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 3,
                        y: 3,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'RIGHT',
                    tail: [
                        {
                            x: 3,
                            y: 3,
                        },
                    ],
                    id: 0,
                    name: 'human',
                    score: 5.439999999999995,
                    stats: {
                        number_of_captured_tiles: 6,
                        number_of_mines_captured: 0,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', ' ', 'C-0', ' ', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 7,
                ticks_left: 3,
            },
            players: [
                {
                    active: true,
                    killed: true,
                    position: {
                        x: 2,
                        y: 2,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'RIGHT',
                    tail: [],
                    id: 0,
                    name: 'human',
                    score: 5.459999999999995,
                    stats: {
                        number_of_captured_tiles: 1,
                        number_of_mines_captured: 0,
                        number_of_suicides: 1,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', ' ', 'C-0', ' ', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 8,
                ticks_left: 2,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 3,
                        y: 2,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'RIGHT',
                    tail: [
                        {
                            x: 3,
                            y: 2,
                        },
                    ],
                    id: 0,
                    name: 'human',
                    score: 5.479999999999994,
                    stats: {
                        number_of_captured_tiles: 1,
                        number_of_mines_captured: 0,
                        number_of_suicides: 1,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', ' ', 'C-0', ' ', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 9,
                ticks_left: 1,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 3,
                        y: 1,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'UP',
                    tail: [
                        {
                            x: 3,
                            y: 2,
                        },
                        {
                            x: 3,
                            y: 1,
                        },
                    ],
                    id: 0,
                    name: 'human',
                    score: 5.499999999999994,
                    stats: {
                        number_of_captured_tiles: 1,
                        number_of_mines_captured: 0,
                        number_of_suicides: 1,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
        {
            type: 'tick',
            game: {
                map: [
                    ['W', 'W', 'W', 'W', 'W'],
                    ['W', ' ', 'C-0', 'C-0', 'W'],
                    ['W', ' ', 'C-0', 'C-0', 'W'],
                    ['W', ' ', ' ', ' ', 'W'],
                    ['W', 'W', 'W', 'W', 'W'],
                ],
                player_id: -1,
                tick: 10,
                ticks_left: 0,
            },
            players: [
                {
                    active: true,
                    killed: false,
                    position: {
                        x: 2,
                        y: 1,
                    },
                    spawn_position: {
                        x: 2,
                        y: 2,
                    },
                    direction: 'LEFT',
                    tail: [],
                    id: 0,
                    name: 'human',
                    score: 8.579999999999991,
                    stats: {
                        number_of_captured_tiles: 4,
                        number_of_mines_captured: 0,
                        number_of_suicides: 1,
                        players_killed: {},
                        killed_by_players: {},
                    },
                    history: [],
                },
            ],
        },
    ],
    players: ['human-0'],
    winner: 'human-0',
};
