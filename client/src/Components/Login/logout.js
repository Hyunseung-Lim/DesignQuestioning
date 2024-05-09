import React, { useState } from 'react'
import axios from "axios"

import './login.css'

export const Logout = (props) => {

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
            HI! {props.name}
            <button onClick={logout}> logout </button>
        </>
    )
}