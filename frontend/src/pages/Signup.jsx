import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ReactComponent as ArrowRightIcon } from '../assets/svg/keyboardArrowRightIcon.svg';
import visibilityIcon from '../assets/svg/visibilityIcon.svg';

function Signup() {

  const [showPassword, setShowPassword] = useState(false);

  const [formData, setFormData] = useState({
    email: '',
  });

  const { email, firstname, lastname, username, password } = formData;

  const onChange = (e) => {
    setFormData((prevState) => ({
      ...prevState,
      [e.target.id]: e.target.value,
    }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
  };

  return (
    <div className="pageContainer">
      <header>
        <p className="pageHeader">Enter your Email to sign up.</p>
      </header>

      <form onSubmit={onSubmit}>
        <input
          type="email"
          className="emailInput"
          placeholder="Email"
          id="email"
          value={email}
          onChange={onChange}
        />

        <input
          type="text"
          className="firstnameInput"
          placeholder="Firstname"
          id="firstname"
          value={firstname}
          onChange={onChange}
        />

        <input
          type="text"
          className="lastnameInput"
          placeholder="Lastname"
          id="lastname"
          value={lastname}
          onChange={onChange}
        />

        <input
          type="text"
          className="usernameInput"
          placeholder="Username"
          id="username"
          value={username}
          onChange={onChange}
        />

        <div className="passwordInputDiv">
          <input
            type={showPassword ? 'text' : 'password'}
            className="passwordInput"
            placeholder="Password"
            id="password"
            value={password}
            onChange={onChange}
          />

          <img
            src={visibilityIcon}
            alt="show password"
            className="showPassword"
            onClick={() => setShowPassword((prevState) => !prevState)}
          />
        </div>

        <div className="signUpBar">
          <p className="signUpText">Sign Up</p>
          <button className="signUpButton">
            <ArrowRightIcon fill="#ffffff" width="34px" height="34px" />
          </button>
        </div>
      </form>

      <Link to="/log-in" className="registerLink">
        Login Instead
      </Link>
    </div>
  );
}

export default Signup;
