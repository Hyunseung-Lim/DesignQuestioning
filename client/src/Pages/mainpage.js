import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './pages.css'

import { Topbar } from '../Components/Topbar/topbar';
// import { Board } from '../Components/board/board';
import { Chat } from '../Components/chat/chat';
import { BaselineChat } from '../Components/chat/baselinechat';
import { IdeaContainer } from '../Components/IdeaContainer/ideaContainer';
import { Student } from '../Components/student/student';

export const MainPage = (props) => {

    const [mode, setMode] = useState();
    const [profileData, setProfileData] = useState({'name':null, 'character':0, 'goal1':"", 'goal2':"", 'goal3':""});
    const [ideaData, setIdeaData] = useState();
    const [chatData, setChatData] = useState();
    // const [divergentLevel, setDivergentLevel] = useState(0);
    // const [convergentLevel, setConvergentLevel] = useState(0);
    const [knowledgeLevel, setKnowledgeLevel] = useState(0);
    const [time, setTime] = useState(0);
    const [feedbackData, setFeedbackData] = useState({'cnd': 0, 'qns': 0, 'uniqueness': 0, 'relevance': 0, 'high_level': 0, 'specificity': 0, 'justification': 0, 'active': 0})
    const [questionChecker, setQuestionChecker] = useState(false);
    const [face, setFace] = useState(33);
    const [isUpdateIdea, setIsUpdateIdea] = useState(false);

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
        setMode(res.mode)
        setProfileData(({
            name: res.name,
            character: res.character,
            goal1: res.goal1,
            goal2: res.goal2,
            goal3: res.goal3
        }))
        setIdeaData(res.ideaData)
        setChatData(res.chatData)
        setTime(res.time *  60000)
        setKnowledgeLevel(res.student_knowledge_level)
        setFeedbackData({'cnd': res.cnd, 'qns': res.qns, 'uniqueness': res.uniqueness, 'relevance': res.relevance, 'high_level': res.high_level, 'specificity': res.specificity, 'justification': res.justification, 'active': res.active})
        setFace(res.face)    
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
                // setDivergentLevel(res.student_divergent_level);
                // setConvergentLevel(res.student_convergent_level);
                setKnowledgeLevel(res.student_knowledge_level)
                setFeedbackData({'cnd': res.cnd, 'qns': res.qns, 'uniqueness': res.uniqueness, 'relevance': res.relevance, 'high_level': res.high_level, 'specificity': res.specificity, 'justification': res.justification, 'active': res.active})
                setQuestionChecker(res.questionChecker)
                setFace(res.face)
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    const getBaselineResponse = (feedback) => {
        axios({
            method: "POST",
            url:"/baselineresponse",
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
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function getQuestion() {
        axios({
            method: "GET",
            url:"/askQuestion",
            headers: {
                Authorization: 'Bearer ' + props.token
            }
            })
            .then((response) => {
                const res =response.data
                setChatData([...chatData, 
                    {"speaker": "student", "content": res.response}
                ]);
                setQuestionChecker(false);
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    const updateIdea = async () => {
        setIsUpdateIdea(true);
        await axios({
            method: "GET",
            url:"/updateIdea",
            headers: {
                Authorization: 'Bearer ' + props.token
            }
            })
            .then((response) => {
                const res =response.data
                setIdeaData(res.ideaData)
                setIsUpdateIdea(false);
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
            setIsUpdateIdea(false);
        })
    }

    useEffect(() => {
        getData()
    }, []);

    return(
        <>
            <div className='mainpage'>
                <Topbar token={props.token} setToken={props.setToken} removeToken={props.removeToken} time={time}/>
                <div className='UIContainer'>
                    {/* {notesData ? <Board token={props.token} notesData={notesData}/> : <>loading</>} */}
                    {ideaData ? <IdeaContainer ideaData={ideaData} isUpdateIdea={isUpdateIdea} updateIdea={() => updateIdea()}/> : <>loading</>}
                    {chatData ? (mode === 1 ? 
                        <Chat token={props.token} chatData={chatData} isUpdateIdea={isUpdateIdea} questionChecker={questionChecker} getResponse={(feedback) => getResponse(feedback)} getQuestion={() => getQuestion()}/>
                        : <BaselineChat token={props.token} chatData={chatData} isUpdateIdea={isUpdateIdea} getResponse={(feedback) => getBaselineResponse(feedback)}/>) : <>loading</>}
                    {profileData ? (mode === 1 ? <Student knowledgeLevel={knowledgeLevel} profileData={profileData} feedbackData={feedbackData} face={face}/> : null) : <>loading</> }
                </div>
            </div>
        </>
    )
}