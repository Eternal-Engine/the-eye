import {useState} from 'react'
import {Link, useNavigate} from 'react-router-dom'
import visibilityIcon from '../assets/svg/visibilityIcon.svg'
import { ReactComponent as ArrowRightIcon } from '../assets/svg/keyboardArrowRightIcon.svg'



function Login(){
    const [showPassword, setShowPassword] = useState(false) //pw visibility state

    const [formData, setFormData] = useState({    //hook managing form
        email : '',
        password: ''
    })

    const {email, password} = formData            //destructuring
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
                    <p className='pageHeader'>Welcome Back!</p>
                </header>
                
                <form className='form'>
                    <input type='email' className='emailInput' placeholder='Email' id='email' value={email} onChange={onChange}/>
                    <div className='passwordInputDiv'>
                        <input type={showPassword ? 'text': 'password'} className='passwordInput' placeholder='Password' onChange={onChange} id='password' value={password}></input>
                        <img
                        src={visibilityIcon}
                        alt='show password'
                        className='showPassword'
                        onClick={() => setShowPassword((prevState) => !prevState)}
                        />
                    </div>

                    <Link to='/forgot-password' className='forgotPasswordLink'>
                     Forgot Password ?
                    </Link>

                    <div className='signInBar'>
                      <p className='signInText'>Sign In</p>
                      <button className='signInButton'>
                      <ArrowRightIcon fill='#ffffff' width='34px' height='34px' />
                      </button>
                    </div>
                </form>


                <Link to='/sign-up' className='registerLink'>
                  Sign Up Instead
                </Link>
                
            </div>
        </>
    )
}

export default Login
