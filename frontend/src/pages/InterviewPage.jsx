import { useState, useEffect } from "react";

import { useNavigate } from "react-router-dom";

import api from "../api/axios";

import Editor from "@monaco-editor/react";

import StartInterviewCard from "../components/StartInterviewCard";

function InterviewPage() {
  const storedUser = JSON.parse(localStorage.getItem("user"));

  console.log(storedUser);

  const navigate = useNavigate();

  const [session, setSession] = useState(null);

  const [topic, setTopic] = useState("Arrays");

  const [difficulty, setDifficulty] = useState("");

  const [company, setCompany] = useState("Google");

  const [question, setQuestion] = useState(null);

  const [code, setCode] = useState("");

  const [submissionResult, setSubmissionResult] = useState(null);

  const [hint, setHint] = useState("");

  const [generatingQuestion, setGeneratingQuestion] = useState(false);

  const [submittingSolution, setSubmittingSolution] = useState(false);

  const [generatingHint, setGeneratingHint] = useState(false);

  const [timeLeft, setTimeLeft] = useState(60 * 60);

  const [sessionInfo, setSessionInfo] = useState(null);

  const [interviewCompleted, setInterviewCompleted] = useState(false);

  const [finalAnalytics, setFinalAnalytics] = useState(null);

  const [experienceLevel, setExperienceLevel] = useState("Intermediate");

  const [interviewType, setInterviewType] = useState("DSA");

  const [comfortableTopics, setComfortableTopics] = useState([]);

  const [resumeFile, setResumeFile] = useState(null);

  const [resumeUploaded, setResumeUploaded] = useState(false);

  const [resumeFileName, setResumeFileName] = useState("");

  const [transcript, setTranscript] = useState("");

  const [recognition, setRecognition] = useState(null);

  const [voiceFeedback, setVoiceFeedback] = useState("");

  const [behavioralAnswer, setBehavioralAnswer] = useState("");

  const [behavioralFeedback, setBehavioralFeedback] = useState(null);

  const [behavioralQuestionIndex, setBehavioralQuestionIndex] = useState(0);
  
  const [resumeBehavioralQuestions, setResumeBehavioralQuestions] = useState([]);

  const [behavioralCompleted, setBehavioralCompleted] = useState(false);

  const [behavioralAnswers, setBehavioralAnswers] = useState([]);

  const [finalBehavioralReport, setFinalBehavioralReport] = useState(null);

  const [isListening, setIsListening] = useState(false);

  const startSession = async () => {
    try {
      const response = await api.post("/start-session", {
        user_id: storedUser.id,
        session_name: "Interview Session",
      });

      setSession(response.data);

      setSessionInfo(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const fetchLatestResume = async () => {
    try {
      const response = await api.get("/latest-resume", {
        params: {
          user_id: storedUser.id,
        },
      });

      console.log(response.data);
      if (response.data) {
        setResumeUploaded(true);

        setResumeFileName(response.data.file_name);
      }
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    startSession();
    fetchLatestResume();
  }, []);

  useEffect(() => {
    if (!session) return;
    if (timeLeft <= 0) {
      submitSolution();
      return;
    }
    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [question, timeLeft]);
  useEffect(() => {
    if (question?.type === "behavioral" && transcript) {
      setBehavioralAnswer(transcript);
    }
  }, [transcript]);

  const generateQuestion = async () => {
    try {
      if (interviewType === "Behavioral") {
  const response = await api.get(
    "/resume-behavioral-questions",
    {
      params: {
        user_id: storedUser.id,
      },
    },
  );

  setResumeBehavioralQuestions(
    response.data.questions,
  );

  setBehavioralQuestionIndex(0);

  setQuestion({
    type: "behavioral",
    title: "Behavioral Interview",
    problem_statement:
      response.data.questions[0],
  });

  return;
}
      setGeneratingQuestion(true);
      const response = await api.get("/generate-question", {
        params: {
          user_id: storedUser.id,
          difficulty: difficulty.toUpperCase(),
          company: company,
          experience_level: experienceLevel,
          comfortable_topics: comfortableTopics.join(","),
        },
      });

      setQuestion(response.data);
      setGeneratingQuestion(false);
      setCode(response.data.starter_code);
    } catch (error) {
      setGeneratingQuestion(false);
      console.log(error);
    }
  };

  const generateAdaptiveQuestion = async () => {
    if (sessionInfo?.current_question_number >= sessionInfo?.total_questions) {
      await fetchFinalAnalytics();

      setInterviewCompleted(true);

      return;
    }
    try {
      setSessionInfo((prev) => ({
        ...prev,
        current_question_number: prev.current_question_number + 1,
      }));
      const response = await api.get("/generate-question", {
        params: {
          user_id: storedUser.id,
          topic: submissionResult.next_topic || topic,

          difficulty: submissionResult.next_difficulty,

          company: company,
        },
      });

      setQuestion(response.data);

      setCode(response.data.starter_code);

      setSubmissionResult(null);

      setHint("");

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    } catch (error) {
      console.log(error);
    }
  };

  const submitSolution = async () => {
    console.log(session);
    try {
      setSubmittingSolution(true);
      const response = await api.post("/submit-solution", {
        session_id: session.session_id,
        topic: topic,
        difficulty: difficulty,
        question: question.problem_statement,
        code: code,
        function_name: question.function_name,
        test_cases: [
          ...question.visible_test_cases,
          ...question.hidden_test_cases,
        ],
      });

      setSubmittingSolution(false);

      setSubmissionResult(response.data);

      console.log(response.data);

      setDifficulty(response.data.next_difficulty);
    } catch (error) {
      setSubmittingSolution(false);
      console.log(error);
    }
  };
  const generateHint = async () => {
    try {
      setGeneratingHint(true);
      const response = await api.post("/generate-hint", {
        question: question.problem_statement,
        code: code,
        execution_result: submissionResult?.execution?.all_passed
          ? "Passed"
          : "Failed",
      });
      setGeneratingHint(false);
      setHint(response.data.hint);
    } catch (error) {
      setGeneratingHint(false);
      console.log(error);
    }
  };

  const fetchFinalAnalytics = async () => {
    try {
      const response = await api.get(`/user/${storedUser.id}/analytics`);

      setFinalAnalytics(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const uploadResume = async () => {
    try {
      const formData = new FormData();

      formData.append("file", resumeFile);

      const response = await api.post(
        `/upload-resume?user_id=${storedUser.id}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );
      console.log(response.data);

      setResumeUploaded(true);
      setResumeFileName(response.data.file_name);
    } catch (error) {
      console.log(error);
    }
  };

  const minutes = Math.floor(timeLeft / 60);

  const seconds = timeLeft % 60;
  if (interviewCompleted) {
    return (
      <div className="p-10">
        <div className="bg-white p-10 rounded shadow max-w-2xl mx-auto">
          <h1 className="text-4xl font-bold mb-8 text-center">
            🎉 Interview Completed
          </h1>

          <div className="space-y-4 text-lg">
            <p>
              Questions Attempted:
              <strong> {sessionInfo?.total_questions}</strong>
            </p>

            <p>
              Average Score:
              <strong> {finalAnalytics?.average_score}</strong>
            </p>

            <p>
              Recommended Topic:
              <strong> {finalAnalytics?.recommended_topic}</strong>
            </p>
          </div>
        </div>
        <div className="mt-8 text-center">
          <button
            onClick={() => navigate("/analytics")}
            className="
      bg-blue-600
      text-white
      px-6
      py-3
      rounded
      hover:bg-blue-700
    "
          >
            View Full Analytics
          </button>
        </div>
      </div>
    );
  }

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);

    speechSynthesis.speak(utterance);
  };

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    console.log("SpeechRecognition:", SpeechRecognition);

    if (!SpeechRecognition) {
      alert("Speech Recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();

    setRecognition(recognition);

    recognition.continuous = true;

    recognition.interimResults = false;

    recognition.lang = "en-US";

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      let finalTranscript = "";

      for (let i = 0; i < event.results.length; i++) {
        finalTranscript += event.results[i][0].transcript + " ";
      }

      setTranscript(finalTranscript);

      console.log(finalTranscript);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      console.log("Speech error:", event.error);
    };

    recognition.start();
  };

  const stopListening = () => {
    if (recognition) {
      recognition.stop();
    }
  };
  const behavioralQuestions = [
    "Tell me about yourself.",
    "Why do you want to work here?",
    "Tell me about a challenging project.",
    "Describe a time you faced a conflict in a team.",
    "What is your biggest strength?",
  ];
  const generateFinalBehavioralReport = async () => {
    console.log("FUNCTION CALLED");
    try {
      const response = await api.post("/final-behavioral-report", {
        answers: behavioralAnswers,
      });

      console.log(response.data);

      setFinalBehavioralReport(response.data);
      setBehavioralCompleted(true);
    } catch (error) {
      console.log(error);
    }
  };
  const evaluateBehavioralAnswer = async () => {
    try {
      const response = await api.post("/evaluate-behavioral-answer", {
        question: question.problem_statement,
        answer: behavioralAnswer,
      });
      console.log(response.data);
      setBehavioralFeedback(response.data);
      console.log("Saving Answer:", behavioralAnswer);
      setBehavioralAnswers((prev) => [
        ...prev,
        {
          question: question.problem_statement,
          answer: behavioralAnswer,
          feedback: response.data,
        },
      ]);
      console.log(behavioralAnswers);
      const nextIndex = behavioralQuestionIndex + 1;

      if (nextIndex < resumeBehavioralQuestions.length) {
        setBehavioralQuestionIndex(nextIndex);

        setQuestion({
          type: "behavioral",
          title: "Behavioral Interview",
          problem_statement: resumeBehavioralQuestions[nextIndex],
        });

        setBehavioralAnswer("");
        setTranscript("");
        setBehavioralFeedback(null);
      } else {
        console.log("GENERATING FINAL REPORT")
        await generateFinalBehavioralReport();
      }
    } catch (error) {
      console.log(error);
    }
  };

  const nextBehavioralQuestion = async () => {
    if (behavioralQuestionIndex < behavioralQuestions.length - 1) {
      const nextIndex = behavioralQuestionIndex + 1;

      setBehavioralQuestionIndex(nextIndex);

      setQuestion({
        type: "behavioral",
        title: "Behavioral Interview",
        problem_statement: behavioralQuestions[nextIndex],
      });

      setBehavioralAnswer("");
      setBehavioralFeedback(null);
    } else {
      await generateFinalBehavioralReport();
      setBehavioralCompleted(true);
    }
  };

  const fetchResumeBehavioralQuestions = async () => {
  try {
    const response = await api.get(
      "/resume-behavioral-questions",
      {
        params: {
          user_id: storedUser.id,
        },
      },
    );

    setResumeBehavioralQuestions(
      response.data.questions,
    );

    console.log(response.data.questions);
  } catch (error) {
    console.log(error);
  }
};
  if (behavioralCompleted) {
    return (
      <div className="p-10">
        <div className="bg-white p-8 rounded shadow">
          <h1 className="text-4xl font-bold mb-6">
            Behavioral Interview Completed
          </h1>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-blue-100 p-4 rounded">
              <h3 className="font-bold">Communication</h3>
              <p className="text-3xl">
                {finalBehavioralReport?.communication_score}/10
              </p>
            </div>

            <div className="bg-green-100 p-4 rounded">
              <h3 className="font-bold">Leadership</h3>
              <p className="text-3xl">
                {finalBehavioralReport?.leadership_score}/10
              </p>
            </div>

            <div className="bg-yellow-100 p-4 rounded">
              <h3 className="font-bold">Confidence</h3>
              <p className="text-3xl">
                {finalBehavioralReport?.confidence_score}/10
              </p>
            </div>

            <div className="bg-purple-100 p-4 rounded">
              <h3 className="font-bold">Overall</h3>
              <p className="text-3xl">
                {finalBehavioralReport?.overall_score}/10
              </p>
            </div>
          </div>
          <div className="mb-6">
            <h3 className="text-xl font-bold mb-2">Hiring Recommendation</h3>

            <span
              className={`
      px-4
      py-2
      rounded
      text-white
      font-semibold
      ${
        finalBehavioralReport?.hiring_recommendation === "Hire"
          ? "bg-green-600"
          : "bg-orange-500"
      }
    `}
            >
              {finalBehavioralReport?.hiring_recommendation}
            </span>
          </div>
          <div className="bg-gray-100 p-6 rounded">
            <h3 className="text-xl font-bold mb-3">Interview Summary</h3>

            <p className="leading-7">{finalBehavioralReport?.summary}</p>
          </div>
        </div>
      </div>
    );
  }
  if (question?.type === "behavioral") {
    return (
      <div className="p-10">
        <h2 className="text-3xl font-bold mb-6">Behavioral Interview</h2>
        <div className="mb-4">
          <p className="text-gray-600 font-semibold">
            Question {behavioralQuestionIndex + 1} /{" "}
            {resumeBehavioralQuestions.length}
          </p>
        </div>
        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-xl font-bold mb-4">
            {question.problem_statement}
          </h3>
          <div className="flex gap-4 mb-4">
            <button
              onClick={startListening}
              className="bg-green-600 text-white px-4 py-2 rounded"
            >
              🎤 Start Recording
            </button>

            <button
              onClick={stopListening}
              className="bg-red-600 text-white px-4 py-2 rounded"
            >
              ⏹ Stop Recording
            </button>
          </div>
          {isListening && (
            <div className="mb-4 text-green-600 font-semibold">
              🎤 Listening...
            </div>
          )}
          <textarea
            value={behavioralAnswer}
            onChange={(e) => setBehavioralAnswer(e.target.value)}
            className="w-full border p-4 rounded h-48"
            placeholder="Type your answer here..."
          />

          <button
            onClick={evaluateBehavioralAnswer}
            className="
            mt-4
            bg-green-600
            text-white
            px-6
            py-3
            rounded
          "
          >
            Submit Answer
          </button>
        </div>
      </div>
    );
  }
  return (
    <div className="p-10">
      <h1 className="text-4xl font-bold mb-6">AI Interview Coach</h1>
      <p>{transcript}</p>
      {question && (
        <div className="mt-4 text-2xl font-bold text-red-500">
          ⏱ {minutes}:{seconds.toString().padStart(2, "0")}
        </div>
      )}

      {sessionInfo && (
        <div className="border p-4 rounded w-96">
          <p className="text-green-600 font-semibold">
            Interview Session Active
          </p>

          <p className="mt-2 font-bold">
            Question {sessionInfo.current_question_number}
            {" / "}
            {sessionInfo.total_questions}
          </p>
        </div>
      )}

      {session && !question && (
        <StartInterviewCard
          interviewType={interviewType}
          setInterviewType={setInterviewType}
          experienceLevel={experienceLevel}
          setExperienceLevel={setExperienceLevel}
          difficulty={difficulty}
          setDifficulty={setDifficulty}
          company={company}
          setCompany={setCompany}
          generateQuestion={generateQuestion}
          generatingQuestion={generatingQuestion}
          resumeFile={resumeFile}
          setResumeFile={setResumeFile}
          uploadResume={uploadResume}
          resumeUploaded={resumeUploaded}
          resumeFileName={resumeFileName}
          comfortableTopics={comfortableTopics}
          setComfortableTopics={setComfortableTopics}
        />
      )}

      {question && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-10">
            <div className="border p-6 rounded bg-white space-y-4 overflow-auto max-h-[700px]">
              <h3 className="text-2xl font-bold">{question.title}</h3>

              <div>
                <strong>Problem Statement:</strong>
                <p>{question.problem_statement}</p>
              </div>

              <div>
                <strong>Constraints:</strong>
                <p>{question.constraints}</p>
              </div>

              <div>
                <strong>Examples:</strong>
                <p>{question.examples}</p>
              </div>

              {question?.visible_test_cases && (
                <div>
                  <strong>Test Cases:</strong>

                  <ul className="list-disc ml-6">
                    {question.visible_test_cases.map((test, index) => (
                      <li key={index}>
                        Input: {JSON.stringify(test.input_data)}
                        {" | "}
                        Output: {test.expected_output}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="space-y-4">
              <div>
                <h2 className="text-2xl font-bold mb-4">Write Solution</h2>

                <p className="mb-2 text-gray-600">
                  Complete the function only. Do not use input() or print().
                </p>

                <Editor
                  height="600px"
                  defaultLanguage="python"
                  value={code}
                  onChange={(value) => setCode(value || "")}
                  theme="vs-dark"
                />
              </div>

              <div className="flex gap-4">
                <button
                  onClick={submitSolution}
                  className="bg-purple-600 text-white px-6 py-2 rounded"
                >
                  {submittingSolution ? "Evaluating..." : "Submit Solution"}
                </button>

                <button
                  onClick={generateHint}
                  className="bg-orange-500 text-white px-6 py-2 rounded"
                >
                  {generatingHint ? "Thinking..." : "Get Hint"}
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {submissionResult && (
        <div className="mt-10 bg-white p-8 rounded shadow">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-3xl font-bold">Submission Result</h2>

            <div
              className={`px-4 py-2 rounded text-white font-semibold ${
                submissionResult.execution.all_passed
                  ? "bg-green-600"
                  : "bg-red-500"
              }`}
            >
              {submissionResult.execution.all_passed
                ? "All Test Cases Passed"
                : "Some Test Cases Failed"}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-100 p-6 rounded">
              <h3 className="text-xl font-bold mb-2">Score</h3>

              <p className="text-5xl font-bold">
                {submissionResult.evaluation.score}
                <span className="text-2xl">/10</span>
              </p>
            </div>

            <div className="bg-gray-100 p-6 rounded">
              <h3 className="text-xl font-bold mb-2">Status</h3>

              <p className="text-2xl font-semibold">
                {submissionResult.execution.all_passed ? "Passed" : "Failed"}
              </p>
            </div>
          </div>

          <div className="mt-8">
            <h3 className="text-2xl font-bold mb-4">AI Feedback</h3>

            <div className="bg-gray-100 p-6 rounded">
              <p className="leading-7">
                {submissionResult.evaluation.feedback}
              </p>
            </div>
          </div>

          {submissionResult.next_difficulty && (
            <div className="mt-6 bg-blue-100 p-4 rounded">
              <h3 className="text-xl font-bold">Adaptive Difficulty</h3>

              <p className="mt-2">
                Based on your performance, next recommended difficulty:
                <strong> {submissionResult.next_difficulty}</strong>
              </p>

              <button
                onClick={generateAdaptiveQuestion}
                className="mt-4
                bg-blue-600
                text-white
                  px-6
                  py-2
                  rounded
                "
              >
                Next Adaptive Question
              </button>
            </div>
          )}

          {submissionResult.next_topic && (
            <div className="mt-4">
              <p>
                Recommended focus topic:
                <strong> {submissionResult.next_topic}</strong>
              </p>
            </div>
          )}

          <div className="mt-8">
            <h3 className="text-2xl font-bold mb-4">Test Case Results</h3>

            <div className="space-y-4">
              {submissionResult.execution.results.map((test, index) => {
                const isHidden = index >= question.visible_test_cases.length;

                return (
                  <div
                    key={index}
                    className={`p-6 rounded border ${
                      test.passed
                        ? "bg-green-50 border-green-300"
                        : "bg-red-50 border-red-300"
                    }`}
                  >
                    <div className="flex justify-between items-center mb-4">
                      <h4 className="text-xl font-bold">
                        {isHidden
                          ? `Hidden Test Case ${
                              index - question.visible_test_cases.length + 1
                            }`
                          : `Test Case ${index + 1}`}
                      </h4>

                      <div
                        className={`px-3 py-1 rounded text-white ${
                          test.passed ? "bg-green-600" : "bg-red-500"
                        }`}
                      >
                        {test.passed ? "Passed" : "Failed"}
                      </div>
                    </div>

                    {!isHidden && (
                      <div className="space-y-2">
                        <p>
                          <strong>Input:</strong>{" "}
                          {JSON.stringify(test.input_data)}
                        </p>

                        <p>
                          <strong>Expected Output:</strong>{" "}
                          {test.expected_output}
                        </p>

                        <p>
                          <strong>Actual Output:</strong> {test.actual_output}
                        </p>

                        {test.error && (
                          <p className="text-red-600">
                            <strong>Error:</strong> {test.error}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {hint && (
        <div className="mt-8 border p-6 rounded bg-yellow-100">
          <h2 className="text-2xl font-bold mb-2">Hint</h2>

          <p>{hint}</p>
        </div>
      )}
    </div>
  );
}

export default InterviewPage;
