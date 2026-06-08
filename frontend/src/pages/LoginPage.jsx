import { signInWithPopup, GoogleAuthProvider } from "firebase/auth";

import { auth } from "../firebase";

import { useNavigate } from "react-router-dom";

import api from "../api/axios";


function LoginPage() {
  const navigate = useNavigate();

  const signInWithGoogle = async () => {
    try {
      const provider = new GoogleAuthProvider();

      const result = await signInWithPopup(auth, provider);

      const response = await api.post("/create-user", {
        username: result.user.displayName,
        firebase_uid: result.user.uid,
        email:result.user.email,
      });

      localStorage.setItem("user", JSON.stringify(response.data));

      navigate("/interview");
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-10 rounded shadow w-[400px] text-center">
        <h1 className="text-4xl font-bold mb-6">AI Interview Coach</h1>

        <p className="mb-8 text-gray-600">
          Practice AI-powered coding interviews
        </p>

        <button
          onClick={signInWithGoogle}
          className="bg-black text-white px-6 py-3 rounded w-full"
        >
          Continue with Google
        </button>
      </div>
    </div>
  );
}

export default LoginPage;
