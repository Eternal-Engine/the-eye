import {useState} from 'react'
import {Link, useNavigate} from 'react-router-dom'
import visibilityIcon from '../assets/svg/visibilityIcon.svg'
import { ReactComponent as ArrowRightIcon } from '../assets/svg/keyboardArrowRightIcon.svg'



function Signup(){
    const [formData, setFormData] = useState({    // managing form
        email : ''
    })

    const {email} = formData            //destructuring
    const navigate = useNavigate()

    //updating our formdata state
    const onChange = (e) => {
    setFormData((prevState) => ({
      ...prevState,
      [e.target.id]: e.target.value,
    }))
  }

    return(
        <>
            <div className='pageContainer'>
                <header>
                    <p className='pageHeader'>Enter Your Email to Signup!</p>
                </header>
                
                <form className='form'>
                    <input type='email' className='emailInput' placeholder='Email' id='email' value={email} onChange={onChange}/>

                    <div className='signUpBar'>
                      <p className='signUpText'>Submit</p>
                      <button className='signInButton'>    
                      <ArrowRightIcon fill='#ffffff' width='34px' height='34px' />
                      </button>
                    </div>
                </form>


                <Link to='/log-in' className='registerLink'>
                  Login Instead
                </Link>
                
            </div>
        </>
    )
}

export default Signup

