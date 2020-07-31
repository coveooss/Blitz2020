import * as React from 'react';
import {Layer, Rect} from 'react-konva';

import {CAPTURED_GAP_RATIO, colors, Size, VisualizationContext} from '../Constants';
import {TailCorner} from './TailCorner';

export const Tails: React.FunctionComponent = () => {
    const {tick, game} = React.useContext(VisualizationContext);
    const tails = game.ticks[tick].players.map((player) => (
        <React.Fragment key={`player-tail-${player.id}`}>
            {player.tail
                .map(({x, y}, index: number) => {
                    const posY = y * Size.Tile;
                    const posX = x * Size.Tile;

                    if (index === 0) {
                        return (
                            <Rect
                                key={`player-tail-${player.id}-${index}`}
                                fill="#403F3F"
                                width={Size.InnerTile / 2}
                                height={Size.InnerTile / 2}
                                x={posX + Size.InnerTile / 4}
                                y={posY + Size.InnerTile / 4}
                            />
                        );
                    } else if (index < player.tail.length - 1) {
                        const previous = player.tail[index - 1];
                        const next = player.tail[index + 1];
                        const lineSize = 0.1 * Size.Tile;
                        const halfOffset = Size.InnerTile / 2 - lineSize / 2;
                        const isVertical = next && next.y !== y && next.x === x;
                        const isACorner = previous && next && previous.x !== next.x && previous.y !== next.y;

                        return isACorner ? (
                            <TailCorner
                                key={`player-tail-${player.id}-${index}`}
                                x={x}
                                y={y}
                                previous={previous}
                                next={next}
                                color={colors[player.id]}
                                lineSize={lineSize}
                            />
                        ) : (
                            <Rect
                                key={`player-tail-${player.id}-${index}`}
                                fill={colors[player.id]}
                                width={isVertical ? lineSize : Size.Tile}
                                height={isVertical ? Size.Tile : lineSize}
                                x={isVertical ? posX + halfOffset : posX - Size.Gap / 2}
                                y={isVertical ? posY - Size.Gap / 2 : posY + halfOffset}
                                shadowColor={'#000'}
                                shadowOffset={{
                                    x: (-CAPTURED_GAP_RATIO / 2) * Size.InnerTile,
                                    y: (CAPTURED_GAP_RATIO / 2) * Size.InnerTile,
                                }}
                                shadowOpacity={0.3}
                            />
                        );
                    }
                    return null;
                })
                .filter(Boolean)
                .sort((a: React.ReactElement, b: React.ReactElement) => {
                    if (a.props.x !== b.props.x) {
                        return b.props.x - a.props.x;
                    }
                    return a.props.y - b.props.y;
                })}
        </React.Fragment>
    ));
    return <Layer offset={{x: -0.5 * Size.Gap, y: -0.5 * Size.Gap}}>{tails}</Layer>;
};
