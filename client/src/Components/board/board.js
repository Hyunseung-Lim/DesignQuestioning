import React, { useState, useRef } from 'react';
import './board.css'

import { StickyNote } from './stickynote';

export const Board = (props) => {

    const [notesData, setNotesData] = useState([{"id": 0, "content": "저출산의 원인은 바쁜 와중에 아이를 돌볼 시간이 없다는 것. 그래서 디지털 트윈 기술을 활용해 디지털 환경에서 아이를 케어하면 실제 아이도 케어를 받도록 함", "position": {"x": 0, "y": 0}}, {"id": 1, "content": "hi1", "position": {"x": 400, "y": 400}}]);
    const parentRef = useRef(null);

    const moveNote = (id, newPos) => {
        setNotesData(notesData.map(notesData => {
            return notesData.id === id ? { ...notesData, position: newPos } : notesData;
        }));
    };

    return(
        <>
            <div className='board'>
                <div className='boardUI'>
                    <div className='noteContainer' ref={parentRef}>
                        {notesData.map(noteData => (
                            <StickyNote
                                key={noteData.id}
                                initialPos={noteData.position}
                                content={noteData.content}
                                id={noteData.id}
                                onMove={moveNote}
                                parentRef={parentRef}
                            />
                        ))}
                    </div>
                </div>
                <div className='bottombar'>
                    <button>add note</button>
                </div>
            </div>
        </>
    )
}