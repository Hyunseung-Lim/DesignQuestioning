import React, {useState} from 'react';
import '../chat.css'

import { ChatBubble } from './chatbubble';


export const Chat = (props) => {

    const [chatlog, setChatlog] = useState(props.chatData);

    return(
        <>
            <div className='chatUI'>
                <div className='chatWindow'>
                    <div className='chatContainer'>
                        {chatlog.map((chat, index) => (
                            <ChatBubble
                                key = {index}
                                speaker = {chat.speaker}
                                content = {chat.content}
                            />
                        ))}
                    </div>
                </div>
                <div className='bottombar'>
                    <input placeholder='Message IDMentee...'/>
                    <img className='chatBtn' src='images/chatBtn.png' alt='chatBtn'/>
                </div>
            </div>
        </>
    )
}