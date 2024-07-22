import React from 'react';
import '../chat.css'

export const TypingBubble = ({content}) => {

    return(
        <>
            <div className='studentchatHolder'>
                <img src='images/student.png' alt='logo'/> 
                <div className='studentchat'>
                    <div className='studentName'>동건</div>
                    <div className='typingbubble'>
                        {content}
                    </div>
                </div>
            </div>
        </>
    )
}