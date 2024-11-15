import React from 'react';
import MembersList from './MembersList';

const Members = ({ darkMode }) => {
  return (
    <div className={`p-4 sm:p-8 ${darkMode ? 'bg-gray-900 text-gray-100' : 'bg-gray-50 text-gray-900'}`}>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <div>
          <h1 className={`text-2xl font-bold ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>Members</h1>
          {/* <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Manage your youth ministry members</p> */}
        </div>
      </div>
      <div className={`rounded-xl shadow-sm border overflow-hidden ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-100'}`}>
        <MembersList darkMode={darkMode}/>
      </div>
    </div>
  );
};

export default Members;
