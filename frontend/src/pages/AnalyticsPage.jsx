import { useEffect, useState } from "react";

import api from "../api/axios";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);

  const storedUser = JSON.parse(localStorage.getItem("user"));

  const topicData = analytics?.topic_performance || [];

  const fetchAnalytics = async () => {
    try {
      const response = await api.get(`/user/${storedUser.id}/analytics`);

      console.log(response.data);

      setAnalytics({
        ...response.data,
      });
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (!analytics) {
    return <div className="p-10 text-2xl">Loading analytics...</div>;
  }

  return (
    <div className="p-10 bg-gray-100 min-h-screen">
      <h1 className="text-4xl font-bold mb-10">Performance Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Total Sessions</h2>

          <p className="text-5xl font-bold text-blue-600">
            {analytics.total_sessions}
          </p>
        </div>

        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Total Questions</h2>

          <p className="text-5xl font-bold text-green-600">
            {analytics.total_questions}
          </p>
        </div>

        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Average Score</h2>

          <p className="text-5xl font-bold text-purple-600">
            {analytics.average_score}
          </p>
        </div>

        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-bold">Average Attempts</h2>

          <p className="text-4xl mt-4">{analytics.average_attempts}</p>
        </div>

        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Recommended Topic</h2>

          <p className="text-2xl font-bold text-red-500 capitalize">
            {analytics.recommended_topic}
          </p>
        </div>
      </div>

      <div className="mt-10 bg-white p-8 rounded shadow">
        <h2 className="text-3xl font-bold mb-6">Weak Topics</h2>

        {analytics.weak_topics.length === 0 ? (
          <p className="text-gray-600">No weak topics detected yet.</p>
        ) : (
          <div className="flex flex-wrap gap-4">
            {analytics.weak_topics.map((topic, index) => (
              <div
                key={index}
                className="bg-red-100 text-red-700 px-4 py-2 rounded-full font-semibold capitalize"
              >
                {topic}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="mt-10 bg-white p-8 rounded shadow">
        <h2 className="text-3xl font-bold mb-6">Weak Topic Analysis</h2>

        <div style={{ width: "100%", height: 300 }}>
          <ResponsiveContainer>
            <BarChart data={topicData}>
              <XAxis dataKey="topic" />

              <YAxis />

              <Tooltip />

              <Bar dataKey="average_score" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-10 bg-white p-8 rounded shadow">
          <h2 className="text-3xl font-bold mb-6">Performance Trend</h2>

          <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer>
              <LineChart data={analytics.submission_trend}>
                <XAxis dataKey="submission" />

                <YAxis />

                <Tooltip />

                <Line type="monotone" dataKey="score" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-10 bg-white p-8 rounded shadow">
            <h2 className="text-3xl font-bold mb-6">Difficulty Performance</h2>

            <div style={{ width: "100%", height: 300 }}>
              <ResponsiveContainer>
                <BarChart data={analytics.difficulty_performance}>
                  <XAxis dataKey="difficulty" />

                  <YAxis />

                  <Tooltip />

                  <Bar dataKey="average_score" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>

      <div
        className="
  bg-white
  p-8
  rounded
  shadow
  mt-10
"
      >
        <h2
          className="
    text-2xl
    font-bold
    mb-4
  "
        >
          Interview Strategy
        </h2>

        <p
          className="
    whitespace-pre-line
    text-gray-700
    leading-7
  "
        >
          {analytics.strategy}
        </p>
      </div>
    </div>
  );
}

export default AnalyticsPage;
