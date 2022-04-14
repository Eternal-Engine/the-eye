//App component serves as container to our application. exported as child to ./index.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Signup from './pages/Signup';
//import Register from './pages/Register';
import Login from './pages/Login';
import Homepage from './pages/Homepage';
import ForgotPassword from './pages/ForgotPassword';

function App() {
  return (
    <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/sign-up" element={<Signup />} />
          <Route path="/log-in" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
        </Routes>
      </Router>
  );
}

export default App;
