import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../chat.css'

import { ChatBubble } from './chatbubble';


export const Chat = (props) => {

    const [chatlog, setChatlog] = useState(props.chatData);
    const [feedback, setFeedback] = useState("");
    const [triggerResponse, setTriggerResponse] = useState(false);

    const handleFeedbackChange = (event) => {
        setFeedback(event.target.value);
    };

    const giveFeedback = () => {
        if(feedback !== "") {
            setChatlog([...chatlog, {"speaker":"instructor", "content": feedback}]);
            setTriggerResponse(true);
        }
    }

    useEffect(() => {
        async function fetchData() {
            if (triggerResponse) {
                await props.getResponse(feedback);
                setTriggerResponse(false); // Reset trigger
                setFeedback("");
            }
        }
        fetchData();
    }, [triggerResponse]);

    useEffect(() => {
        setChatlog(props.chatData);
    }, [props.chatData]);

    // const getResponse = () => {
    //     axios({
    //         method: "POST",
    //         url:"/response",
    //         headers: {
    //             Authorization: 'Bearer ' + props.token
    //         },
    //         data: {feedback: feedback}
    //         })
    //         .then((response) => {
    //             const res =response.data
    //             setChatlog([...chatlog, {"speaker":"student", "content": res.response}]);
    //         }).catch((error) => {
    //         if (error.response) {
    //             console.log(error.response)
    //             console.log(error.response.status)
    //             console.log(error.response.headers)
    //         }
    //     })
    // }

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
                    <input value={feedback} onChange={handleFeedbackChange} placeholder='Feeback to Student...'/>
                    <img className='chatBtn' src='images/chatBtn.png' alt='chatBtn' onClick={giveFeedback}/>
                </div>
            </div>
        </>
    )
}