import React from 'react';
import './pages.css'

import { Board } from '../Components/board/board';
import { Chat } from '../Components/chat/chat';



export const MainPage = (props) => {
    return(
        <>
            <div className='mainpage'>
                <div className='UIContainer'>
                    <Board/>
                    <Chat/>
                </div>
            </div>
        </>
    )
}