import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import useToken from './Components/useToken';
import './App.css';

import { MainPage } from './Pages/mainpage';
import { LoginPage } from './Pages/loginPage';
import { StartPage } from './Pages/startPage';

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
              <Route path='/feedback' element={<MainPage token={token} setToken={setToken} removeToken={removeToken}/>}/>
              <Route path='/' element={<StartPage token={token} setToken={setToken} removeToken={removeToken}/>}/>
            </Routes>
          </>
        }
      </div>
    </Router>
  );
}

export default App;