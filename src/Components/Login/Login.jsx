import React from 'react'
import { useState } from 'react';
import { FaLock , FaEnvelope , FaUser} from "react-icons/fa";
import { Link } from 'react-router-dom';
import './Login.css'
const Login = () => {
    const[action, setAction]= useState("Sign-Up");

  return (
    <div className='FlexBox'>
      <form action='' className="Form">
       <div className="login-container">
        <div className={action}>
            <div className="Login-inputs">
                <h1 className='h1-txt'>Login  Now</h1>
                <input type="text" placeholder='Enter Username' required/><div className="icon-user"><FaUser/></div>
                <input type="Email" placeholder='Enter Email' required/><div className="icon-mail"><FaEnvelope/></div>
                <input type="Password" placeholder='Enter Password' required/><div className="icon-lock"><FaLock/></div>
              
            </div>
            <div className="btns2">
              <Link to="/"><button type="submit" className={action==="Login-now"?"submit-gray":"submit"} onClick={()=>{setAction("Sign-Up")}}>Sign Up </button></Link>
           <button type="submit" className={action==="Sign-Up"?"submit-gray":"submit"} onClick={()=>{setAction("Login-now")}}>Login</button>
            </div>
            <div className="lost">
                <text>Lost/Forgot Password?</text>
                <Link to="/Forgot">Click Here</Link>
            </div>
        </div>
    </div> 
    </form>
    
    </div>
  )
}

export default Login
