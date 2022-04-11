//component renders our Navbar

function Header({text, bgColor, textColor}) {
  const headerStyles = {
    backgroundColor: bgColor,
    color: textColor,
    
  }



  return (
    <header style={headerStyles}>
    
        <div className='container1'>
        <h1>iWitness</h1>
            <div className="time-member-holder">
                <p>Date: 22/04/2022</p>
                <p>Members: 2,345,675</p>
            </div>
            <div className="link-holder">
              
              <a href="#">Signup</a>
              <a href="#">Login</a>
            </div>
            
        </div>
    </header>
  )
}

Header.defaultProps = {
  text: 'iWitness',
  bgColor: 'rgba(0,0,0,0.4)',
  textColor: '#fff',
}

export default Header
