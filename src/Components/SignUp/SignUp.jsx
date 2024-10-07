import React, { useState } from 'react'
import './SignUp.css'
import Vidback from './Glow.mp4'
import { FaLock , FaEnvelope , FaUser} from "react-icons/fa";
import { Link } from 'react-router-dom';
const SignUp = () => {2

  const Loginfo =()=>{
    return
  }
  const[action, setAction]= useState("Sign-Up");
  return (
    <>
    <form action='' className="Form">
       <div className="login-container">
        <div className={action}>
            
            
           
            <div className="SignUp-inputs">
              
            
                <h1 className='h1-txt'>Sign Up Now</h1>
                <input type="text" placeholder='Enter First Name' required/><div className="icon-user"><FaUser/></div>
                <input type="text" placeholder='Enter Last Name' required/><div className="icon-user"><FaUser/></div>
                <input type="Email" placeholder='Enter Email' required/><div className="icon-mail"><FaEnvelope/></div>
                <input type="Password" placeholder='Enter Password' required/><div className="icon-lock"><FaLock/></div>
              
            </div>
            <div className="btns2">
            <button type="submit" className={action==="Login-now"?"submit-gray":"submit"} onClick={()=>{setAction("Sign-Up")}}>Sign Up </button>
          <Link to="/Login">  <button type="submit" className={action==="Sign-Up"?"submit-gray":"submit"} onClick={()=>{setAction("Login-now")}}>Login</button></Link>
            </div>
        </div>
    </div> 
    <div className="choose">
          <input type="checkbox" /><label>I agree to the Terms and conditions</label>
        </div>
    </form>
    
    </>
  )
}

export default SignUp