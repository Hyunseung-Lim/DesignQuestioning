import React from 'react';
import '../chat.css'

export const Chat = (props) => {
    return(
        <>
            <div className='chatUI'>
                <div className='bottombar'>
                    <input placeholder='Message IDMentee...'/>
                    <img className='chatBtn' src='images/chatBtn.png' alt='chatBtn'/>
                </div>
            </div>
        </>
    )
}