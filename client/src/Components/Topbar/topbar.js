import React, {useState, useEffect} from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

import './topbar.css'

export const Topbar = (props) => {

    const navigate = useNavigate();
    const location = useLocation();
    const isFeedback = location.state?.feedback;
    const [time, setTime] = useState(0);
    // const [isFeedback, setIsFeedback] = useState(false);

    useEffect(() => {
        // Only set up the interval if the time is greater than 0
        if (time > 0) {
            const timer = setInterval(() => {
                setTime((prevTime) => prevTime - 10); // update every 10 milliseconds
            }, 10);
            // Clear the interval when the component unmounts
            return () => clearInterval(timer);
        }
    }, [time]);

    useEffect(() => {
        setTime(props.time);
    }, [props.time]);

    function formatTime(milliseconds) {
        const minutes = Math.floor(milliseconds / 60000);
        const seconds = Math.floor((milliseconds % 60000) / 1000);
        return `${padTo2Digits(minutes)}:${padTo2Digits(seconds)}`;
    }

    // Helper function to ensure two-digit numbers
    function padTo2Digits(num) {
        return num.toString().padStart(2, '0');
    }

    const logout = async () => {
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
        navigate('/');
    })}


    // function nextRound() {
    //     axios({
    //     method: "GET",
    //     url:"/nextRound",
    //     headers: {
    //         Authorization: 'Bearer ' + props.token
    //     }
    //     })
    //     .then((response) => {

    //     }).catch((error) => {
    //     if (error.response) {
    //         console.log(error.response)
    //         console.log(error.response.status)
    //         console.log(error.response.headers)
    //         }
    //     })
    // }

    const finish = async () => {
        await axios({
            method: "GET",
            url:"/nextRound",
            headers: {
                Authorization: 'Bearer ' + props.token
            }
        })
        .then((response) => {

        }).catch((error) => {
        if (error.response) {
            console.log(error.response)
            console.log(error.response.status)
            console.log(error.response.headers)
            }
        })
        navigate('/start');
    }

    return(
        <>
            <div className='topbar'>
                <img src='logo192.png' alt='logo'/>
                <div className='rightContainer'>
                    {isFeedback ? <div className='timeHolder'><img src="/images/timer.svg" alt="timer"/>{formatTime(time)}</div> : null }
                    <input className="burger-check" type="checkbox" id="burger-check" /><label className="burger-icon" htmlFor="burger-check"><span className="burger-sticks"></span></label>
                    <div className='menu'>
                        {isFeedback ?
                            <button className='hamburger-bar' onClick={finish}>라운드 종료</button> 
                            :
                            null
                        }                         
                        <button className='hamburger-bar' onClick={logout}>로그아웃</button>
                    </div>
                </div>
            </div>
        </>
    )
}