import React, { useState } from 'react';
import { Signin } from '../Components/Login/signin'
import { Signup } from '../Components/Login/signup'

import './pages.css'

export const LoginPage = (props) => {

    const [isSignup, setIsSignup ] = useState(false);

    return(
            <div className='loginpage'>
                {
                    isSignup === false
                    ? <Signin setIsSignup = { () => setIsSignup(true) } setToken={props.setToken}/>
                    : <Signup setIsSignin = { () => setIsSignup(false) }/>
                }
            </div>
    )
}