import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './pages.css'

import { Topbar } from '../Components/Topbar/topbar';
import { Board } from '../Components/board/board';
import { Chat } from '../Components/chat/chat';

export const MainPage = (props) => {

    const [profileData, setProfileData] = useState({'name':null})
    const [notesData, setNotesData] = useState([]);


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
        setNotesData(
            res.notesData
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

    useEffect(() => {
        getData()
    }, []);

    return(
        <>
            <div className='mainpage'>
                <Topbar removeToken={props.removeToken}/>
                <div className='UIContainer'>
                    {notesData ? <Board token={props.token} notesData={notesData}/> : <>loading</>}
                    <Chat/>
                </div>
            </div>
        </>
    )
}