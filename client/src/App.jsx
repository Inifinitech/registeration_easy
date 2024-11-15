import { BrowserRouter as Router } from 'react-router-dom';
import Layout from './components/Layout';
// import Dashboard from './components/Dashboard';
// import Members from './components/Members';
// import MemberForm from './components/MemberForm';

// import Attendance from './components/Attendance';


function App() {

  return (
    <Router>

        {/* <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/members" element={<Members />} />
          <Route path="/addmember" element={<MemberForm />} />
          <Route path="/attendance" element={<Attendance />} />
        </Routes> */}
      <Layout/>
    </Router>
  );
}

export default App;