import React, { useState, useEffect } from 'react';
import Attendance from './Attendance'; 
import { Route, Routes } from 'react-router-dom';
import Sidebar from './Sidebar';
import { Menu, Sun, Moon } from 'lucide-react';
import Members from './Members';
import Dashboard from './Dashboard';
import AttendanceChart from './AttendanceChart';

const Layout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const [members, setMembers] = useState([]);

  useEffect(() => {
    const fetchedMembers = [
      { id: 1, firstname: 'John', lastname: 'Doe', group: 'Transformers' },
      { id: 2, firstname: 'Jane', lastname: 'Smith', group: 'Pacesetters' },
      { id: 3, firstname: 'Michael', lastname: 'Johnson', group: 'Ignition' },
    ];
    setMembers(fetchedMembers);
  }, []);

  return (
    <div className={`flex h-screen ${darkMode ? 'bg-gray-900 text-gray-100' : 'bg-gray-50 text-gray-900'}`}>
      <button
        className="fixed top-4 right-4 z-50 p-2 rounded-md bg-indigo-600 text-white"
        onClick={() => setDarkMode(!darkMode)}
      >
        {darkMode ? <Sun className="w-6 h-6" /> : <Moon className="w-6 h-6" />}
      </button>

      <button
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-indigo-600 text-white"
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
      >
        <Menu className="w-6 h-6" />
      </button>

      {isSidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      <div
        className={`${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 fixed lg:static inset-y-0 left-0 z-40 transition-transform duration-300 ease-in-out ${
          darkMode ? 'bg-gray-800' : 'bg-white'
        }`}
      >
        <Sidebar onClose={() => setIsSidebarOpen(false)} />
      </div>

      <div className="flex-1 overflow-auto pt-16 lg:pt-0">
        <Routes>
        <Route path="/" 
               element={<Dashboard darkMode={darkMode} />}/>
          <Route
            path="/attendance"
            element={<Attendance members={members} darkMode={darkMode} />}
          />
          <Route path="/members"
                 element={<Members darkMode={darkMode}/>}/>
          <Route path="/analytics"
                 element={<AttendanceChart darkMode={darkMode}/>} />
        </Routes>
      </div>
    </div>
  );
};

export default Layout;
