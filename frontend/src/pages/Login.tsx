import { useState } from "react";
import api from "../config/api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      params.append("username", email);  
      params.append("password", password);

      const res = await api.post("/login", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
        console.log("RESPOSTA LOGIN:", res.data);
        localStorage.setItem("token", res.data.access_token);
        navigate("/dashboard");
    } catch (err: unknown) {
        if (err instanceof Error) {
            console.error("ERRO LOGIN:", err.message);
        } else {
            console.error("ERRO LOGIN:", err);
        }
        setError("Login inválido");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 to-blue-200">
      <form
        onSubmit={handleLogin}
        className="bg-white p-8 rounded-2xl shadow-lg w-96 hover:shadow-2xl transition-shadow duration-300">
        <h1 className="text-3xl font-bold mb-6 text-center text-blue-700">Bem-vindo!</h1>

        {error && (
          <p className="text-red-500 bg-red-100 p-2 rounded mb-4 text-center">
            {error}
          </p>
        )}

        <input
          type="email"
          placeholder="Email"
          className="border border-gray-300 p-3 rounded w-full mb-4 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Senha"
          className="border border-gray-300 p-3 rounded w-full mb-6 focus:ring-2 focus:ring-blue-400 focus:outline-none transition"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-300">
          Entrar
        </button>
      </form>
    </div>
  );
}
