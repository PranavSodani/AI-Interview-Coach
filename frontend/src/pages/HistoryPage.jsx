import { useEffect, useState } from "react";
import api from "../api/axios";

function HistoryPage() {
  const [submissions, setSubmissions] = useState([]);

  const storedUser = JSON.parse(localStorage.getItem("user"));

  const fetchHistroy = async () => {
    try {
      const response = await api.get(`/user/${storedUser.id}/submissions`);
      setSubmissions(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchHistroy();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-10">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-5xl font-bold mb-10">Submission History</h1>

        <div className="space-y-6">
          {submissions.map((submission) => (
            <div key={submission.id} className="bg-white p-6 rounded shadow">
              <div className="flex justify-between">
                <h2 className="text-2xl font-bold">{submission.topic}</h2>

                <p className="text-lg">Score: {submission.evaluation_score}</p>
              </div>

              <p className="mt-4 text-gray-700">{submission.question}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
export default HistoryPage;
