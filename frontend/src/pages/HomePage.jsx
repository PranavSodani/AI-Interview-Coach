import { Link } from "react-router-dom";

function HomePage() {

  return (

    <div className="min-h-screen bg-gray-100 p-10">

      <div className="max-w-6xl mx-auto">

        <div className="text-center mt-20">

          <h1 className="text-6xl font-bold mb-6">
            AI Interview Coach
          </h1>

          <p className="text-xl text-gray-700 mb-10">
            Practice coding interviews with AI-generated
            questions, real-time evaluation, analytics,
            and personalized feedback.
          </p>

          <Link
            to="/login"
            className="bg-black text-white px-8 py-4 rounded text-lg"
          >
            Start Practicing
          </Link>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24">

          <div className="bg-white p-8 rounded shadow">

            <h2 className="text-2xl font-bold mb-4">
              AI Question Generation
            </h2>

            <p className="text-gray-600">
              Generate LeetCode-style coding interview
              questions dynamically using AI.
            </p>

          </div>

          <div className="bg-white p-8 rounded shadow">

            <h2 className="text-2xl font-bold mb-4">
              Real-Time Evaluation
            </h2>

            <p className="text-gray-600">
              Execute and evaluate coding solutions
              instantly with AI-powered feedback.
            </p>

          </div>

          <div className="bg-white p-8 rounded shadow">

            <h2 className="text-2xl font-bold mb-4">
              Performance Analytics
            </h2>

            <p className="text-gray-600">
              Track weak topics, progress trends,
              and interview performance over time.
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default HomePage;