//Button component to be rendered with props on any page


const buttonStyle = {
    color: '#ff6a95',
    backgroundColor: '#202142',   
}

const Button = ({label}) => {
  return (
    <button style={buttonStyle}>{label}</button>
  )
}

export default Button
