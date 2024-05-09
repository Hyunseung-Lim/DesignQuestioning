import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import useToken from './Components/useToken';
import './App.css';

import { MainPage } from './Pages/mainpage';
import { LoginPage } from './Pages/LoginPage';

function App() {

  const { token, removeToken, setToken } = useToken();

  return (
    <Router>
      <div className='App'>
        {!token && token!=="" &&token!== undefined?
          <LoginPage setToken={setToken}/>
          :
          <>
            <Routes>
              <Route path='/' element={<MainPage token={token} setToken={setToken} removeToken={removeToken}/>} />
            </Routes>
          </>
        }
      </div>
    </Router>
  );
}

export default App;