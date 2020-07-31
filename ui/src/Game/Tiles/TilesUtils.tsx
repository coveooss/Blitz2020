const isCaptured = (tile: string): boolean => /C-\d+/.test(tile);

const isWall = (tile: string): boolean => tile === 'W';

const isBlackHole = (tile: string): boolean => tile === '!';

const isBlitzium = (tile: string): boolean => tile === '$';

const isStar = (tile: string): boolean => /%(-\d+)?/.test(tile);

const isNotCapturedPlanet = (tile: string): boolean => tile === '%';

export const TilesUtils = {
    isCaptured,
    isWall,
    isBlackHole,
    isBlitzium,
    isStar,
    isNotCapturedPlanet,
};
