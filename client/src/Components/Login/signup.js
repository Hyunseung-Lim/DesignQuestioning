import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Validate } from './validate';

import './login.css';

export const Signup = (props) => {
    
    // values
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");

    const [errors, setErrors] = useState({});
    const [submitting, setSubmitting] = useState(false);

    const emailHandler = (e) => {
        e.preventDefault();
        setEmail(e.target.value);
    }

    const nameHandler = (e) => {
        e.preventDefault();
        setName(e.target.value);        
    }

    const passwordHandler = (e) => {
        e.preventDefault();
        setPassword(e.target.value);
    }

    const submitHander = async (e) => {
        setSubmitting(true);
        e.preventDefault();
        await new Promise((r) => setTimeout(r, 1000));
        setErrors(Validate({email, name, password}));
    }

    useEffect(() => {
        if(submitting) {
            if(Object.keys(errors).length === 0) {
                axios({
                    method: 'post',
                    url: '/signup',
                    data: {
                        email: email,
                        name: name,
                        password: password
                    }
                });
                props.setIsSignin();
            }
            setSubmitting(false);
        }
    }, [errors]);


    return(
        <>
            <div className='signholder'>
                <form className='signupbox' onSubmit={submitHander}>
                    <div className='signinTitle'>
                        IDMentee
                    </div>
                    <input className='signInput' type="email" placeholder={'이메일'} value={email}  onChange={emailHandler}></input>
                    <input className='signInput' type="name" placeholder={'이름'} value={name} onChange={nameHandler}></input>
                    <input className='signInput' type="password" placeholder={'비밀번호'} value={password} onChange={passwordHandler} autoComplete="on"></input>
                    <button className='loginBtn' type="submit">가입</button>
                </form>
                <div className='createAccountbox'>
                    계정이 있으신가요?
                    <button onClick={() => props.setIsSignin()}>
                        로그인
                    </button>
                </div>            
            </div>
        </>
    )
}