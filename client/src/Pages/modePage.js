import React from 'react';
import axios from 'axios';

import { Topbar } from '../Components/Topbar/topbar';
import { useNavigate } from 'react-router-dom';

import './pages.css'

export const ModePage = (props) => {

    const navigate = useNavigate();

    const modeButtonClick = async (mode) => {
        try {
            await axios({
                method: "POST",
                url:"/mode",
                headers: {
                    Authorization: 'Bearer ' + props.token
                },
                data: {mode: mode}
            })
            .then((response) => {
            
            }).catch((error) => {
            
            })
            navigate('/start');
        } catch (error) {
            //
        }
    };

    return(
        <>
            <Topbar removeToken={props.removeToken}/>
            <div className='modepage'>
                <div className='modeinstruction'>
                    진행자의 안내에 따라서 모드를 선택해주세요.
                </div>
                <div className='modeBox'>
                    <div className='modeBtn' onClick={() => modeButtonClick(1)}>
                        Mode A
                    </div>
                    <div className='modeBtn' onClick={() => modeButtonClick(2)}>
                        Mode B
                    </div>
                </div>
            </div>
        </>
    )
}