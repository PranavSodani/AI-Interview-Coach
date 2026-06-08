import { useEffect, useState } from "react";

import api from "../api/axios";

function DashboardPage() {

  const storedUser = JSON.parse(
    localStorage.getItem("user")
  );

  const [submissions, setSubmissions] =
    useState([]);

  useEffect(() => {

    fetchSubmissions();

  }, []);

  const fetchSubmissions = async () => {

    try {

      const response = await api.get(
        `/submissions/${storedUser.id}`
      );

      setSubmissions(response.data);

    } catch (error) {

      console.log(error);

    }
  };

  const totalSubmissions =
    submissions.length;

  const averageScore =
    submissions.length > 0
      ? (
          submissions.reduce(
            (acc, submission) =>
              acc +
              submission.evaluation_score,
            0
          ) / submissions.length
        ).toFixed(1)
      : 0;

  const topicsPracticed =
    [...new Set(
      submissions.map(
        (submission) =>
          submission.topic
      )
    )].length;

  return (

    <div className="p-10">

      <h1 className="text-4xl font-bold mb-10">
        Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div className="bg-white p-8 rounded shadow">

          <h2 className="text-xl font-semibold mb-2">
            Total Interviews
          </h2>

          <p className="text-5xl font-bold">
            {totalSubmissions}
          </p>

        </div>

        <div className="bg-white p-8 rounded shadow">

          <h2 className="text-xl font-semibold mb-2">
            Average Score
          </h2>

          <p className="text-5xl font-bold">
            {averageScore}
          </p>

        </div>

        <div className="bg-white p-8 rounded shadow">

          <h2 className="text-xl font-semibold mb-2">
            Topics Practiced
          </h2>

          <p className="text-5xl font-bold">
            {topicsPracticed}
          </p>

        </div>

      </div>

    </div>
  );
}

export default DashboardPage;