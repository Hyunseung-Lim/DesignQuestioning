import React from 'react';
import '../chat.css'

export const ChatBubble = ({speaker, content}) => {
    return(
        <>
            {speaker === "student" ? 
                <div className='studentchat'>
                    <img src='images/student.png' alt='logo'/>
                    <div className='chatbubble'>
                        {content}
                    </div>
                </div>
                :
                <div className='instructorchat'>
                    {content}
                </div>
            }
        </>
    )
}