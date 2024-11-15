import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Users, CalendarCheck, BarChart3, Settings, Church } from 'lucide-react';

const Sidebar = ({ onClose, darkMode }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { icon: Users, label: 'Members', path: '/members' },
    { icon: CalendarCheck, label: 'Attendance', path: '/attendance' },
    { icon: BarChart3, label: 'Analytics', path: '/analytics' },
    { icon: Settings, label: 'Settings', path: '/settings' }
  ];

  const handleNavigation = (path) => {
    navigate(path);
    onClose?.();
  };

  return (
    <div className={`w-64 h-screen flex flex-col ${darkMode ? 'bg-gray-800 text-gray-100' : 'bg-indigo-900 text-white'}`}>
      <div className="p-6 flex items-center gap-3 cursor-pointer" onClick={() => handleNavigation('/')}>
        <Church className="w-8 h-8" />
        <span className="text-xl font-bold">The Vault</span>
      </div>
      
      <nav className="flex-1 px-4 py-6">
        {menuItems.map((item, index) => (
          <button
            key={index}
            onClick={() => handleNavigation(item.path)}
            className={`flex items-center gap-3 w-full px-4 py-3 rounded-lg transition-colors ${
              location.pathname === item.path
                ? `${darkMode ? 'bg-gray-700' : 'bg-indigo-800'} text-white`
                : `${darkMode ? 'text-gray-400' : 'text-gray-300'} hover:${darkMode ? 'bg-gray-700' : 'bg-indigo-800'}`
            }`}
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      
      <div className={`p-4 border-t ${darkMode ? 'border-gray-700' : 'border-indigo-800'}`}>
        <div className="flex items-center gap-3 px-4 py-2">
          <div className={`${darkMode ? 'bg-gray-700' : 'bg-indigo-700'} w-8 h-8 rounded-full flex items-center justify-center`}>
            <span className="text-sm font-medium">JD</span>
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">John Doe</p>
            <p className="text-xs text-gray-400">Admin</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
