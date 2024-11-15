import React, { useState } from 'react';
import { CheckCircle, XCircle } from 'lucide-react';

const Attendance = ({ members, darkMode }) => {
  const [attendance, setAttendance] = useState({});

  const handleAttendance = (id, status) => {
    setAttendance((prevAttendance) => ({
      ...prevAttendance,
      [id]: status,
    }));
  };

  return (
    <div className={`p-6 ${darkMode ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-900'}`}>
      <h2 className="text-2xl font-semibold mb-4">Mark Attendance</h2>
      <div className="overflow-x-auto">
        <table className={`min-w-full divide-y ${darkMode ? 'divide-gray-700 bg-gray-800' : 'divide-gray-200 bg-white'}`}>
          <thead className={`${darkMode ? 'bg-gray-700 text-gray-400' : 'bg-gray-50 text-gray-500'}`}>
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Group</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Attendance</th>
            </tr>
          </thead>
          <tbody className={`${darkMode ? 'bg-gray-900 divide-gray-700' : 'bg-white divide-gray-200'}`}>
            {members.map((member) => (
              <tr key={member.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm font-medium ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
                    {member.firstname} {member.lastname}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{member.group}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-right">
                  <button
                    onClick={() => handleAttendance(member.id, 'present')}
                    className={`${
                      attendance[member.id] === 'present' ? 'text-green-500' : 'text-gray-500'
                    } hover:text-green-600`}
                  >
                    <CheckCircle className="w-5 h-5" />
                    Present
                  </button>
                  <button
                    onClick={() => handleAttendance(member.id, 'absent')}
                    className={`ml-4 ${
                      attendance[member.id] === 'absent' ? 'text-red-500' : 'text-gray-500'
                    } hover:text-red-600`}
                  >
                    <XCircle className="w-5 h-5" />
                    Absent
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Attendance;
