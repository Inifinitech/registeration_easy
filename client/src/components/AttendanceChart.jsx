import { useState, useEffect } from 'react';
import { Pie, Line } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

const mockData = {
  totalMembers: 100,
  attendancePercentage: 85,
  absentMembers: 15,
  attendanceTrends: [
    { date: '2024-11-01', percentage: 90 },
    { date: '2024-11-02', percentage: 85 },
    { date: '2024-11-03', percentage: 80 },
    { date: '2024-11-04', percentage: 95 },
  ],
};

const AttendanceCard = ({ date, percentage, onClick, darkMode }) => (
  <div
    className={`p-4 rounded-lg shadow-lg text-center cursor-pointer ${darkMode ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-800'}`}
    onClick={() => onClick(date)}
  >
    <h3 className="text-lg font-bold">{date}</h3>
    <p className="text-sm">Attendance: {percentage}%</p>
  </div>
);

function AttendanceChart({ darkMode }) {
  const [totalMembers, setTotalMembers] = useState(0);
  const [attendancePercentage, setAttendancePercentage] = useState(0);
  const [absentMembers, setAbsentMembers] = useState(0);
  const [attendanceTrends, setAttendanceTrends] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setTotalMembers(mockData.totalMembers);
    setAttendancePercentage(mockData.attendancePercentage);
    setAbsentMembers(mockData.absentMembers);
    setAttendanceTrends(mockData.attendanceTrends);

    setLoading(false);
  }, []);

  const handleCardClick = (date) => {
    setSelectedDate(date);
  };

  const handleBackToCards = () => {
    setSelectedDate(null);
  };

  const selectedData = attendanceTrends.find((trend) => trend.date === selectedDate);

  const pieData = selectedData
    ? {
        labels: ['Present', 'Absent'],
        datasets: [
          {
            data: [selectedData.percentage, 100 - selectedData.percentage],
            backgroundColor: ['#4caf50', '#f44336'],
          },
        ],
      }
    : null;

  const lineData = {
    labels: attendanceTrends.map((item) => item.date),
    datasets: [
      {
        label: 'Attendance Trend',
        data: attendanceTrends.map((item) => item.percentage),
        fill: false,
        borderColor: '#42a5f5',
      },
    ],
  };

  return (
    <div className={`${darkMode ? 'bg-gray-900 text-white' : 'bg-white text-gray-900'} min-h-screen p-8`}>
      <button
        className="mb-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
        onClick={handleBackToCards}
      >
        Back
      </button>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <div>
          <h2 className="text-3xl font-bold text-center mb-6">Attendance Report</h2>
          <div className="text-center mb-6 bg-gray-700 text-white p-4 rounded-lg">
            <h3 className="text-lg">Total Members: {totalMembers}</h3>
          </div>

          {selectedDate ? (
            <div className="flex justify-center gap-8">
              <div className="w-96 p-6 bg-white rounded-lg shadow-md">
                <Pie data={pieData} />
              </div>
              <div className="w-96 p-6 bg-white rounded-lg shadow-md">
                <Line data={lineData} />
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {attendanceTrends.map((trend) => (
                <AttendanceCard
                  key={trend.date}
                  date={trend.date}
                  percentage={trend.percentage}
                  onClick={handleCardClick}
                  darkMode={darkMode}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AttendanceChart;
