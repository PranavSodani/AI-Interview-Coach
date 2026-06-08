import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const storedUser = JSON.parse(localStorage.getItem("user"));

  const logout = () => {
    localStorage.removeItem("user");

    navigate("/login");
  };

  return (
    <nav className="bg-black text-white px-8 py-4 flex justify-between items-center">
      <div className="flex gap-6 items-center">
        <Link to="/" className="font-bold text-xl">
          AI Interview Coach
        </Link>

        <Link to="/">Home</Link>

        {storedUser && (
          <>
            <Link to="/interview">Interview</Link>

            <Link to="/analytics">Analytics</Link>

            <Link to="/history">History</Link>
          </>
        )}
      </div>

      <div>
        {!storedUser ? (
          <Link to="/login">Login</Link>
        ) : (
          <button onClick={logout}>Logout</button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
