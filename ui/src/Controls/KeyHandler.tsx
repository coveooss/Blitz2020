import * as React from 'react';

export interface IKeyHandlerProps {
    onKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
}

export const KeyHandler: React.FunctionComponent<IKeyHandlerProps> = ({onKeyDown, children}) => {
    const ref = React.useRef<HTMLInputElement>(null);
    const onClick = () => ref!.current!.focus();
    return (
        <div className="Visualization" onClick={onClick}>
            {children}
            <input
                ref={ref}
                onKeyDown={onKeyDown}
                autoFocus={true}
                defaultValue=""
                style={{
                    color: 'transparent',
                    backgroundColor: 'transparent',
                    border: 'none',
                    outline: 'none',
                    opacity: 0,
                    zIndex: -1,
                    top: 0,
                    left: 0,
                    position: 'absolute',
                }}
            />
        </div>
    );
};
