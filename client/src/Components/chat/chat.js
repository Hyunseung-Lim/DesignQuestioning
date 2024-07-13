import React, {useState, useEffect, useRef} from 'react';
import axios from 'axios';
import '../chat.css'

import { ChatBubble } from './chatbubble';


export const Chat = (props) => {

    const [chatlog, setChatlog] = useState(props.chatData);
    const [feedback, setFeedback] = useState("");
    const [triggerResponse, setTriggerResponse] = useState(false);
    const [isDisable, setIsDisable] = useState(false);
    const divRef = useRef(null);

    const giveFeedback = () => {
        if(feedback !== "") {
            setChatlog([...chatlog, {"speaker":"instructor", "content": feedback}]);
            setTriggerResponse(true);
        }
    }

    const handleFeedbackChange = (event) => {
        setFeedback(event.target.value);
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            giveFeedback();
        }
    };

    useEffect(() => {
        // console.log(triggerResponse);
        async function fetchData() {
            if (triggerResponse) {
                await props.getResponse(feedback);
                setTriggerResponse(false); // Reset trigger
                setFeedback("");
                setIsDisable(true);
            }
        }
        fetchData();
    }, [triggerResponse]);

    useEffect(() => {
        setChatlog(props.chatData);
        if(isDisable) {
            setIsDisable(false);
        }
    }, [props.chatData]);

    useEffect(() => {
        if (divRef.current) {
            divRef.current.scrollTo({
                top: divRef.current.scrollHeight,
                behavior: 'smooth'
            });
        }
    }, [chatlog]);

    return(
        <>
            <div className='chatUI'>
                <div className='chatWindow' ref={divRef}>
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
                <div className={isDisable ? 'disabled bottombar': 'bottombar'}>
                    <input value={feedback} onKeyDown={handleKeyDown} onChange={handleFeedbackChange} disabled={isDisable} placeholder='Feeback to Student...'/>
                    <img className='chatBtn' src='images/chatBtn.png' alt='chatBtn' onClick={giveFeedback} disabled={isDisable}/>
                </div>
            </div>
        </>
    )
}