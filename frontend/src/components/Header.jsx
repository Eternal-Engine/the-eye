import { useNavigate } from 'react-router-dom';
import { FiLogIn } from 'react-icons/fi';
import { SiGnuprivacyguard } from 'react-icons/si';
import { BsFillPersonCheckFill } from 'react-icons/bs';

function Header({ bgColor, textColor }) {
  //Initializing navigation hooks from react-dom
  const navigate = useNavigate();
  //const location = useLocation();

  const headerStyles = {
    backgroundColor: bgColor,
    color: textColor,
  };

  return (
    <header style={headerStyles}>
      <div className="container1">
        <h1>iWitness</h1>

        <nav className="navlinks-holder">
          <p>
            <BsFillPersonCheckFill fill="#00cc66" width="25px" height="30px" />
            Members: 2,345,782
          </p>
          <ul className="navlinks">
            <li className="link" onClick={() => navigate('/log-in')}>
              <p className="login">
                <FiLogIn fill="#00cc66" width="25px" height="30px" />
                Login
              </p>
            </li>
            <li className="link" onClick={() => navigate('/sign-up')}>
              <p className="signup">
                <SiGnuprivacyguard fill="#00cc66" width="25px" height="30px" />
                Signup
              </p>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

Header.defaultProps = {
  text: 'iWitness',
  bgColor: 'rgba(0,0,0,0.4)',
  textColor: '#fff',
};

export default Header;
