import React, {useState, useEffect, useRef} from 'react';
import axios from 'axios';
import '../chat.css'

import { ChatBubble } from './chatbubble';
import { TypingAnimation } from './typinganimation';

export const Chat = (props) => {

    const [chatlog, setChatlog] = useState(props.chatData);
    const [feedback, setFeedback] = useState("");
    const [triggerResponse, setTriggerResponse] = useState(false);
    const [isDisable, setIsDisable] = useState(false);
    const [isQuestionUpdated, setIsQuestionUpdated] = useState(false);
    const [isReset, setIsReset] = useState(false);
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
        setTimeout(() => {
            setIsQuestionUpdated(false);
        }, 500);
        async function askQuestion() {
            await props.getQuestion();
            setIsQuestionUpdated(true);
            setIsReset(true);
            setTimeout(() => setIsReset(false), 100);
        }
        if(isDisable) {
            if(props.questionChecker) {
                askQuestion();
            }
            else if(!isQuestionUpdated) {
                setIsDisable(false);
            }
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
                        {isDisable ? 
                        <ChatBubble
                                key = {'umm'}
                                speaker = {'student'}
                                content = {<TypingAnimation text="음...그게........." interval={800} isDisable={isDisable} reset={isReset}/>}
                            />
                        :
                        null
                        }
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