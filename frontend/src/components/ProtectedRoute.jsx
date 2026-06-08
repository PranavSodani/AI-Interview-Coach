import { Navigate } from "react-router-dom";

function ProtectedRoute({ children }) {
    const storedUser = localStorage.getItem("user");

    if(!storedUser) {
        return <Navigate to="/login" />;
    }

    return children;
}
export default ProtectedRoute;