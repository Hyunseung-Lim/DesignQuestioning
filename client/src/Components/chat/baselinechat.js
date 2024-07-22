import React, {useState, useEffect, useRef} from 'react';
import axios from 'axios';
import '../chat.css';

import { ChatBubble } from './chatbubble';
import { TypingAnimation } from './typinganimation';

export const BaselineChat = (props) => {

    const [chatlog, setChatlog] = useState(props.chatData);
    const [feedback, setFeedback] = useState("");
    const [triggerResponse, setTriggerResponse] = useState(false);
    const [isDisable, setIsDisable] = useState(false);
    const divRef = useRef(null);
    const textareaRef = useRef(null);

    const giveFeedback = () => {
        if(feedback !== "") {
            setChatlog([...chatlog, {"speaker":"instructor", "content": feedback}]);
            setTriggerResponse(true);
        }
    }

    const handleFeedbackChange = (event) => {
        setFeedback(event.target.value);
        adjustHeight();
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
    }, [chatlog, isDisable]);

    const adjustHeight = () => {
        if (textareaRef.current) {
            // Reset height to recalculate
            textareaRef.current.style.height = '14px';
            // Set height based on the scroll height which reflects the content height
            const maxHeight = 112; // Example max height in pixels for about 5 lines
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, maxHeight)}px`;
        }
    };
    
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
            adjustHeight(); // Adjust height on initial render to ensure it fits the content
        }
    }, [feedback]);

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
                                mode = {2}
                            />
                        ))}
                    </div>
                </div>
                <div className={isDisable ? 'disabled bottombar': 'bottombar'} style={{height: 'auto'}}>
                    <textarea ref={textareaRef} id='bottomtextarea' style={{height: 'auto'}} value={feedback} onKeyDown={handleKeyDown} onChange={handleFeedbackChange} disabled={isDisable} placeholder='피드백을 입력하세요.'/>
                    <img className='chatBtn' src='images/chatBtn.png' alt='chatBtn' onClick={giveFeedback} disabled={isDisable}/>
                </div>
            </div>
        </>
    )
}