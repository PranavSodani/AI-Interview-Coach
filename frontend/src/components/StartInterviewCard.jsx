function StartInterviewCard({
  interviewType,
  setInterviewType,

  experienceLevel,
  setExperienceLevel,

  difficulty,
  setDifficulty,

  company,
  setCompany,

  generateQuestion,
  generatingQuestion,

  setResumeFile,
  uploadResume,
  resumeUploaded,
  resumeFileName,

  comfortableTopics,
  setComfortableTopics,
}) {
  const experienceLevels = [
    "Beginner",
    "Intermediate",
    "Advanced",
  ];

  const difficulties = [
    "Easy",
    "Medium",
    "Hard",
  ];

  const topics = [
    "Arrays",
    "Strings",
    "Linked List",
    "Trees",
    "Graphs",
    "Dynamic Programming",
    "Heap",
    "Greedy",
    "Binary Search",
  ];

  return (
    <div className="bg-white p-8 rounded shadow mt-10">
      <h2 className="text-3xl font-bold mb-6">
        Start Interview
      </h2>

      <div>
        <label className="block mb-2 font-semibold">
          Interview Type
        </label>

        <select
          value={interviewType}
          onChange={(e) => setInterviewType(e.target.value)}
          className="border p-3 rounded w-full"
        >
          <option value="DSA">DSA</option>
          <option value="Behavioral">Behavioral</option>
        </select>

        <p className="mt-2 text-blue-600 font-semibold">
          Selected: {interviewType}
        </p>
      </div>

      <div className="mt-4">
        <label className="block mb-2 font-semibold">
          Experience Level
        </label>

        <select
          value={experienceLevel}
          onChange={(e) => setExperienceLevel(e.target.value)}
          className="border p-3 rounded w-full"
        >
          {experienceLevels.map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>
      </div>

      {interviewType === "DSA" && (
        <>
          <div className="mt-4">
            <label className="block mb-2 font-semibold">
              Difficulty
            </label>

            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="border p-3 rounded w-full"
            >
              <option value="">
                Auto (Based on Resume)
              </option>

              {difficulties.map((difficultyOption) => (
                <option
                  key={difficultyOption}
                  value={difficultyOption}
                >
                  {difficultyOption}
                </option>
              ))}
            </select>
          </div>

          <div className="mt-4">
            <label className="block mb-2 font-semibold">
              Company
            </label>

            <select
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              className="border p-3 rounded w-full"
            >
              <option value="Google">Google</option>
              <option value="Amazon">Amazon</option>
              <option value="Meta">Meta</option>
              <option value="Microsoft">Microsoft</option>
            </select>
          </div>
        </>
      )}

      <div className="mt-4">
        <label className="block mb-2 font-semibold">
          Resume
        </label>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) =>
            setResumeFile(e.target.files[0])
          }
          className="border p-2 rounded w-full"
        />

        <button
          onClick={uploadResume}
          className="
            mt-2
            bg-blue-600
            text-white
            px-4
            py-2
            rounded
          "
        >
          Upload Resume
        </button>

        {resumeUploaded && (
          <div className="mt-3 text-green-600 font-semibold">
            Resume Uploaded ✅
            <br />
            {resumeFileName}
          </div>
        )}
      </div>

      {interviewType === "DSA" && (
        <div className="mt-4">
          <label className="block mb-2 font-semibold">
            Comfortable Topics
          </label>

          <div className="flex flex-wrap gap-2">
            {topics.map((topicOption) => (
              <button
                key={topicOption}
                type="button"
                onClick={() => {
                  if (
                    comfortableTopics.includes(
                      topicOption,
                    )
                  ) {
                    setComfortableTopics(
                      comfortableTopics.filter(
                        (topic) =>
                          topic !== topicOption,
                      ),
                    );
                  } else {
                    setComfortableTopics([
                      ...comfortableTopics,
                      topicOption,
                    ]);
                  }
                }}
                className={`px-3 py-2 rounded border ${
                  comfortableTopics.includes(
                    topicOption,
                  )
                    ? "bg-blue-600 text-white"
                    : "bg-white"
                }`}
              >
                {topicOption}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="mt-6">
        <button
          onClick={generateQuestion}
          className="bg-green-600 text-white px-6 py-3 rounded w-full"
        >
          {generatingQuestion
            ? "Starting..."
            : "Start Interview"}
        </button>
      </div>
    </div>
  );
}

export default StartInterviewCard;