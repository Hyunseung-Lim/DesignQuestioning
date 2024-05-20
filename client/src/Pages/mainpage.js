import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './pages.css'

import { Topbar } from '../Components/Topbar/topbar';
// import { Board } from '../Components/board/board';
import { Chat } from '../Components/chat/chat';
import { IdeaContainer } from '../Components/IdeaContainer/ideaContainer';
import { Student } from '../Components/student/student';

export const MainPage = (props) => {

    const [profileData, setProfileData] = useState({'name':null});
    const [ideasData, setIdeasData] = useState();
    const [chatData, setChatData] = useState();
    const [divergentLevel, setDivergentLevel] = useState(0);
    const [convergentLevel, setConvergentLevel] = useState(0);
    const [knowledgeLevel, setKnowledgeLevel] = useState(0);

    // get profile data from server
    function getData() {
        axios({
        method: "GET",
        url:"/profile",
        headers: {
            Authorization: 'Bearer ' + props.token
        }
        })
        .then((response) => {
        const res =response.data
        res.access_token && props.setToken(res.access_token)
        setProfileData(({
            name: res.name
        }))
        setIdeasData(
            res.ideasData
        )
        setChatData(
            res.chatData
        )
        }).catch((error) => {
        if (error.response) {
            console.log(error.response)
            console.log(error.response.status)
            console.log(error.response.headers)
            axios({
            method: "POST",
            url:"/logout",
            })
            .then((response) => {
            props.removeToken()
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
                }
            })
            }
        })
    }

    const getResponse = (feedback) => {
        axios({
            method: "POST",
            url:"/response",
            headers: {
                Authorization: 'Bearer ' + props.token
            },
            data: {feedback: feedback}
            })
            .then((response) => {
                const res =response.data
                setChatData([...chatData, 
                    {"speaker": "instructor", "content": feedback},
                    {"speaker": "student", "content": res.response}
                ]);
                setDivergentLevel(res.student_divergent_level);
                setConvergentLevel(res.student_convergent_level);
                setKnowledgeLevel(res.student_knowledge_level);
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    useEffect(() => {
        getData()
    }, []);

    return(
        <>
            <div className='mainpage'>
                <Topbar removeToken={props.removeToken}/>
                <div className='UIContainer'>
                    {/* {notesData ? <Board token={props.token} notesData={notesData}/> : <>loading</>} */}
                    {ideasData ? <IdeaContainer ideasData={ideasData}/> : <>loading</>}
                    {chatData ? <Chat token={props.token} chatData={chatData} getResponse={(feedback) => getResponse(feedback)}/> : <>loading</>}
                    <Student divergentLevel={divergentLevel} convergentLevel={convergentLevel} knowledgeLevel={knowledgeLevel}/>
                </div>
            </div>
        </>
    )
}