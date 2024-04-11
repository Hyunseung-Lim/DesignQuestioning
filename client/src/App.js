import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import './App.css';
import { MainPage } from './Pages/mainpage';

function App() {
  return (
    <Router>
      <div className='App'>
          <Routes>
            <Route path='/' element={<MainPage/>} />
          </Routes>
      </div>
    </Router>
  );
}

export default App;
