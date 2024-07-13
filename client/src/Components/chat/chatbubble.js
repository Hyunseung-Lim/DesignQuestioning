import React from 'react';
import '../chat.css'

export const ChatBubble = ({speaker, content}) => {
    return(
        <>
            {speaker === "student" ? 
                <div className='studentchatHolder'>
                    <img src='images/student.png' alt='logo'/>
                    <div className='studentchat'>
                        <div className='studentName'>동건</div>
                        <div className='chatbubble'>
                            {content}
                        </div>
                    </div>
                </div>
                :
                <div className='instructorchatHolder'>
                    <div className='userName'>You</div>
                    <div className='instructorchat'>
                        {content}
                    </div>
                </div>
            }
        </>
    )
}