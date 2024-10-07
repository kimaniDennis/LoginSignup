import React from 'react'
import './ForgotPass.css'
import { HiHome } from 'react-icons/hi'
import { Link } from 'react-router-dom'
import { FaLock , FaEnvelope , FaUser} from "react-icons/fa";

const ForgotPass = () => {
  return (
    <div className='fgotpass'>
        <div className="regain">
             <h2>Forgot Your Password?</h2>
            <form action="submit">
                <input type='email' placeholder='enter your Email' required className='veri-mail'/><FaEnvelope className='Env'/>
                <button type='submit' className='verify'>Verify Now</button>
                <div className="return">
                   <Link to="/"><HiHome className='Home'/>Home</Link>
                    </div>
            </form>
        </div>
    </div>
  )
}

export default ForgotPass
