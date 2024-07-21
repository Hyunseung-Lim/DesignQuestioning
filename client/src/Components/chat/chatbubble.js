import React from 'react';
import '../chat.css'

export const ChatBubble = ({speaker, content, mode}) => {
    return(
        <>
            {speaker === "student" ? 
                <div className='studentchatHolder'>
                    {mode ==1 ? <img src='images/student.png' alt='logo'/> : <img src='images/gpt.png' alt='logo'/>}
                    <div className='studentchat'>
                        <div className='studentName'>{mode == 1 ? <>동건</> : <>GPT</>}</div>
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