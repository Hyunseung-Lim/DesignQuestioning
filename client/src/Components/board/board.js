import React, { useState, useRef } from 'react';
import axios from 'axios';
import './board.css';

import { StickyNote } from './stickynote';

export const Board = (props) => {

    const [currentNotesData, setCurrentNotesData] = useState(props.notesData);
    const parentRef = useRef(null);

    const saveNote = () => {
        axios({
            method: "POST",
            url:"/saveNote",
            headers: {
                Authorization: 'Bearer ' + props.token
            },
            data: {notesData: currentNotesData}
            })
            .then((response) => {

            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    const addNote = () => {
        axios({
            method: "POST",
            url:"/saveNote",
            headers: {
                Authorization: 'Bearer ' + props.token
            },
            data: {notesData: currentNotesData}
            })
            .then((response) => {
                axios({
                    method: "GET",
                    url:"/addNote",
                    headers: {
                        Authorization: 'Bearer ' + props.token
                    }
                    })
                    .then((response) => {
                    const res =response.data
                    res.access_token && props.setToken(res.access_token)
                    setCurrentNotesData(
                        res.notesData
                    )
                    }).catch((error) => {
                    if (error.response) {
                        console.log(error.response)
                        console.log(error.response.status)
                        console.log(error.response.headers)
                    }
                })
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    const deleteNote = (id) => {
        axios({
            method: "POST",
            url:"/saveNote",
            headers: {
                Authorization: 'Bearer ' + props.token
            },
            data: {notesData: currentNotesData}
            })
            .then((response) => {
                axios({
                    method: "POST",
                    url:"/deleteNote",
                    headers: {
                        Authorization: 'Bearer ' + props.token
                    },
                    data: {'deleteId': id}
                    })
                    .then((response) => {
                    const res =response.data
                    res.access_token && props.setToken(res.access_token)
                    setCurrentNotesData(
                        res.notesData
                    )
                    }).catch((error) => {
                    if (error.response) {
                        console.log(error.response)
                        console.log(error.response.status)
                        console.log(error.response.headers)
                    }
                })
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    const moveNote = (id, newPos) => {
        setCurrentNotesData(currentNotesData.map(noteData => {
            return noteData.id === id ? { ...noteData, position: newPos } : noteData;
        }));
    };

    return(
        <>
            <div className='board'>
                <div className='boardUI'>
                    <div className='noteContainer' ref={parentRef}>
                        {currentNotesData.map((noteData, index) => (
                            <StickyNote
                                key = {index}
                                id={noteData.id}
                                initialPos={noteData.position}
                                initalContent={noteData.content}
                                num={index}
                                moveNote={moveNote}
                                deleteNote ={() => deleteNote(noteData.id)}
                                parentRef={parentRef}
                            />
                        ))}
                    </div>
                </div>
                <div className='bottombar'>
                    <button onClick={addNote}>add note</button>
                    <button onClick={saveNote}>save</button>
                </div>
            </div>
        </>
    )
}