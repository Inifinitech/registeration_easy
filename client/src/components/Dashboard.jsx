import React from 'react';
import { Users, TrendingUp, UserCheck, AlertCircle } from 'lucide-react';
import MembersList from './MembersList';

const Dashboard = ({ darkMode }) => {
  const stats = [
    { icon: Users, label: 'Total Members', value: '156', change: '+12%' },
    { icon: UserCheck, label: 'Present Today', value: '89', change: '57%' },
    { icon: TrendingUp, label: 'Growth Rate', value: '23%', change: '+5%' },
    { icon: AlertCircle, label: 'Absent 3+ Weeks', value: '12', change: '-3' }
  ];

  return (
    <div className={`p-8 ${darkMode ? 'bg-gray-900 text-gray-100' : 'bg-gray-50 text-gray-900'}`}>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className={`text-2xl font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>Dashboard</h1>
          <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Welcome back, track your ministry's growth</p>
        </div>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
          Take Attendance
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <div
            key={index}
            className={`p-6 rounded-xl shadow-sm border ${
              darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-100'
            }`}
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`${darkMode ? 'bg-gray-700' : 'bg-indigo-50'} p-2 rounded-lg`}>
                <stat.icon className={`w-6 h-6 ${darkMode ? 'text-gray-300' : 'text-indigo-600'}`} />
              </div>
              <span
                className={`text-sm font-medium ${
                  stat.change.startsWith('+') ? 'text-green-500' : 'text-red-500'
                }`}
              >
                {stat.change}
              </span>
            </div>
            <h3 className={`text-2xl font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'} mb-1`}>
              {stat.value}
            </h3>
            <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} text-sm`}>{stat.label}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-100'} p-6 rounded-xl shadow-sm`}>
          <h2 className="text-lg font-semibold mb-4 text-gray-100">Attendance Trends</h2>
          {/* <AttendanceChart /> */}
        </div>
        <div className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-100'} p-6 rounded-xl shadow-sm`}>
          <h2 className="text-lg font-semibold mb-4 text-gray-100">Recent Members</h2>
          <MembersList darkMode={darkMode}/>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
