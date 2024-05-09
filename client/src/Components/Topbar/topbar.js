import React from 'react';
import axios from 'axios';

import './topbar.css'

export const Topbar = (props) => {

    function logout() {
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
    })}

    return(
        <>
            <div className='topbar'>
                <img src='logo192.png' alt='logo'/>
                <input className="burger-check" type="checkbox" id="burger-check" /><label className="burger-icon" htmlFor="burger-check"><span className="burger-sticks"></span></label>
                <div className='menu'>                         
                    <button className='hamburger-bar' onClick={logout}>Logout</button>
                </div>
            </div>
        </>
    )
}