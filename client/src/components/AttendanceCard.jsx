const AttendanceCard = ({ date, percentage, onClick, darkMode }) => (
    <div
      className={`p-4 rounded-lg shadow-lg text-center cursor-pointer ${darkMode ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-800'}`}
      onClick={() => onClick(date)}
    >
      <h3 className="text-lg font-bold">{date}</h3>
      <p className="text-sm">Attendance: {percentage}%</p>
    </div>
  );
  
  export default AttendanceCard;
  