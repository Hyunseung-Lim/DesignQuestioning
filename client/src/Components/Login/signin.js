import React, { useEffect, useState } from 'react';
import axios from 'axios';

import './login.css';

export const Signin = (props) => {

    //values
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const emailHandler = (e) => {
        e.preventDefault();
        setEmail(e.target.value);
    }

    const passwordHandler = (e) => {
        e.preventDefault();
        setPassword(e.target.value);
    }

    const submitHander = async (e) => {
        e.preventDefault();
        axios({
            method: 'post',
            url: '/token',
            data: {
                email: email,
                password: password
            }
        })
        .then((response) => {
            props.setToken(response.data.access_token)
        }).catch((error) => {
            if (error.response) {
            console.log(error.response)
            console.log(error.response.status)
            console.log(error.response.headers)
            }
        })
        setEmail("");
        setPassword("");
    }

    return(
        <>
            <div className='signholder'>
                <form className='signinbox' onSubmit={submitHander}>
                    <div className='signinTitle'>
                        IDMentee
                    </div>
                    <input className='signInput' type="email" value={email} onChange={emailHandler} placeholder={'이메일'}></input>
                    <input className='signInput' type="password" value={password} onChange={passwordHandler} placeholder={'비밀번호'} autoComplete="on"></input>
                    <button className='loginBtn' type="submit">
                        로그인
                    </button>
                </form>
                <div className='createAccountbox'>
                    계정이 없으신가요?
                    <button onClick={() => props.setIsSignup()}>
                        가입하기
                    </button>
                </div>
            </div>
        </>
    )
}