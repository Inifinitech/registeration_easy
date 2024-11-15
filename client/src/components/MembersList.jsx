import React, { useState } from 'react';
import { format } from 'date-fns';
import { Edit2, Trash2, UserPlus } from 'lucide-react';
import MemberForm from './MemberForm';

const MembersList = ({ darkMode }) => {
  const [members, setMembers] = useState([
    {
      id: 1,
      firstName: 'John',
      lastName: 'Doe',
      gender: 'Male',
      DOB: '2000-01-01',
      location: 'Nairobi',
      phone: '123-456-7890',
      isStudent: true,
      school: 'Nairobi University',
      isVisitor: false,
      willBeComing: false,
      occupation: 'Engineer',
      group: 'Transformers',
      leader: false,
      emergencyContact: {
        name: 'Jane Doe',
        phone: '987-654-3210',
        relation: 'Sister',
      },
    },
    {
      id: 2,
      firstName: 'Jane',
      lastName: 'Smith',
      gender: 'Female',
      DOB: '1998-05-15',
      location: 'Mombasa',
      phone: '987-654-3210',
      isStudent: false,
      school: '',
      isVisitor: true,
      willBeComing: true,
      occupation: 'Artist',
      group: 'Visionaries',
      leader: true,
      emergencyContact: {
        name: 'John Smith',
        phone: '123-456-7890',
        relation: 'Brother',
      },
    },
  ]);

  const [selectedMember, setSelectedMember] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const handleEdit = (member) => {
    setSelectedMember(member);
    setShowForm(true);
  };

  const handleDelete = (id) => {
    if (confirm('Are you sure you want to delete this member?')) {
      setMembers(members.filter((member) => member.id !== id));
    }
  };

  const handleAddMember = (newMember) => {
    setMembers([...members, newMember]);
  };

  if (showForm) {
    return (
      <div className={`p-6 ${darkMode ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-900'}`}>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">
            {selectedMember ? 'Edit Member' : 'Add New Member'}
          </h2>
          <button
            onClick={() => {
              setShowForm(false);
              setSelectedMember(null);
            }}
            className={`text-sm ${darkMode ? 'text-gray-400 hover:text-gray-100' : 'text-gray-600 hover:text-gray-900'}`}
          >
            Cancel
          </button>
        </div>
        <MemberForm
          initialData={selectedMember || undefined}
          onSuccess={(newMember) => {
            handleAddMember(newMember);
            setShowForm(false);
            setSelectedMember(null);
          }}
          darkMode={darkMode}
        />
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-end p-4">
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
        >
          <UserPlus className="w-4 h-4" />
          Add Member
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className={`min-w-full divide-y ${darkMode ? 'divide-gray-700 bg-gray-800' : 'divide-gray-200 bg-white'}`}>
          <thead className={`${darkMode ? 'bg-gray-700 text-gray-400' : 'bg-gray-50 text-gray-500'}`}>
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">AG-Group</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Gender</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Location</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Phone</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">DOB</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">School</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">E-Contact</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className={`${darkMode ? 'bg-gray-900 divide-gray-700' : 'bg-white divide-gray-200'}`}>
            {members.map((member) => (
              <tr key={member.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm font-medium ${darkMode ? 'text-gray-100' : 'text-gray-900'}`}>
                    {member.firstName} {member.lastName}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{member.group}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    {member.gender}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{member.location}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{member.phone}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{format(new Date(member.DOB), 'MMM d, yyyy')}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    {member.school}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    {member.emergencyContact.phone}
                  </div>
                </td>

                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    onClick={() => handleEdit(member)}
                    className={`mr-4 ${darkMode ? 'text-indigo-400 hover:text-indigo-200' : 'text-indigo-600 hover:text-indigo-900'}`}
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(member.id)}
                    className={`${darkMode ? 'text-red-400 hover:text-red-200' : 'text-red-600 hover:text-red-900'}`}
                  >
                    <Trash2 className="w-4 h-4" />
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

export default MembersList;