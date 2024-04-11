import React, {useState, useEffect, useCallback} from 'react';
import './board.css'

export const StickyNote = ({ initialPos, content, id, onMove, parentRef}) => {
    const [isDragging, setIsDragging] = useState(false);
    const [position, setPosition] = useState(initialPos);
    const [relPosition, setRelPosition] = useState({ x: 0, y: 0 }); // Relative position of the cursor

    const onMouseDown = (e) => {
        if (e.button !== 0) return;
        const elem = e.target.getBoundingClientRect();
        setRelPosition({
            x: e.clientX - elem.left,
            y: e.clientY - elem.top,
        });
        setIsDragging(true);
    };

    const onMouseMove = useCallback((e) => {
        if (!isDragging) return;
        if (parentRef && parentRef.current) {
            const parentRect = parentRef.current.getBoundingClientRect();
            setPosition({
                x: e.clientX - parentRect.left - relPosition.x,
                y: e.clientY - parentRect.top - relPosition.y,
            });
        }
    }, [isDragging, parentRef, relPosition]);

    const onMouseUp = useCallback(() => {
        setIsDragging(false);
        onMove(id, position);
    }, [id, onMove, position]);

    useEffect(() => {
        if (isDragging) {
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        } else {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        }

        return () => {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        };
    }, [isDragging, onMouseMove, onMouseUp]);

    return(
        <>
            <div className='stickynote' 
                onMouseDown={onMouseDown}
                onMouseMove={onMouseMove}
                onMouseUp={onMouseUp}
                style={{ 
                    left: position.x + 'px', 
                    top: position.y + 'px', 
                    position: 'absolute' 
                }}>
                <div className='num'>#{id + 1}
                    <button>delete</button>
                </div>
                <textarea placeholder='Write here...'>{content}</textarea>
            </div>
        </>
    )
}