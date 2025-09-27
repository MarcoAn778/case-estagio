import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../config/api";

type Metric = {
    account_id: number;
    campaign_id: number;
    cost_micros?: number | null;
    clicks: number;
    conversions: number;
    impressions: number;
    interactions: number;
    date: string;
};

export default function Dashboard() {
    const [metrics, setMetrics] = useState<Metric[]>([]);
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [orderBy, setOrderBy] = useState("date");
    const [desc, setDesc] = useState(true);
    const [page, setPage] = useState(0);
    const [role, setRole] = useState("");
    const [username, setUsername] = useState("");

    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/");
    };

    useEffect(() => {
        async function fetchData() {
            try {
                const userRes = await api.get("/users/me");
                setRole(userRes.data.role);
                setUsername(userRes.data.username);

                const res = await api.get("/metrics", {
                    params: {
                        start_date: startDate || undefined,
                        end_date: endDate || undefined,
                        order_by: orderBy,
                        desc,
                        skip: page * 10,
                        limit: 10,
                    },
                });
                setMetrics(res.data);
            } catch (err) {
                console.error(err);
            }
        }
        fetchData();
    }, [startDate, endDate, orderBy, desc, page]);

    return (
        <div className="p-6 bg-gray-50 min-h-screen">
            {/* Topbar */}
            <div className="flex justify-between items-center mb-6 bg-white p-4 rounded-xl shadow-md">
                <h1 className="text-2xl font-bold text-blue-700">Dashboard</h1>
                <div className="flex items-center gap-4">
                    <span className="font-medium text-gray-700">Olá, {username}</span>
                    <button
                        onClick={handleLogout}
                        className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors">
                        Sair
                    </button>
                </div>
            </div>

            {/* Filtros */}
            <div className="flex gap-4 mb-4 flex-wrap">
                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="border p-2 rounded-lg focus:ring-2 focus:ring-blue-300 transition"
                />
                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="border p-2 rounded-lg focus:ring-2 focus:ring-blue-300 transition"
                />
                <button
                    onClick={() => setDesc(!desc)}
                    className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors">
                    {desc ? "↓ Desc" : "↑ Asc"}
                </button>
            </div>

            {/* Tabela */}
            <div className="overflow-x-auto rounded-lg shadow-sm bg-white">
                <table className="w-full border-collapse">
                    <thead className="bg-gray-100">
                        <tr>
                            <th
                                className={`p-3 cursor-pointer hover:bg-gray-200 transition ${orderBy === "account_id" ? "bg-blue-100 font-semibold" : ""}`}
                                onClick={() => setOrderBy("account_id")}>
                                Account
                            </th>
                            <th
                                className={`p-3 cursor-pointer hover:bg-gray-200 transition ${orderBy === "campaign_id" ? "bg-blue-100 font-semibold" : ""}`}
                                onClick={() => setOrderBy("campaign_id")}>
                                Campaign
                            </th>
                            {role === "admin" && (
                                <th
                                    className={`p-3 cursor-pointer hover:bg-gray-200 transition ${orderBy === "cost_micros" ? "bg-blue-100 font-semibold" : ""}`}
                                    onClick={() => setOrderBy("cost_micros")}>
                                    Cost
                                </th>
                            )}
                            <th
                                className={`p-3 cursor-pointer hover:bg-gray-200 transition ${orderBy === "clicks" ? "bg-blue-100 font-semibold" : ""}`}
                                onClick={() => setOrderBy("clicks")}>
                                Clicks
                            </th>
                            <th
                                className={`p-3 cursor-pointer hover:bg-gray-200 transition ${orderBy === "conversions" ? "bg-blue-100 font-semibold" : ""}`}
                                onClick={() => setOrderBy("conversions")}>
                                Conversions
                            </th>
                            <th
                                className={`p-3 cursor-pointer hover:bg-gray-200 transition ${orderBy === "impressions" ? "bg-blue-100 font-semibold" : ""}`}
                                onClick={() => setOrderBy("impressions")}>
                                Impressions
                            </th>
                            <th
                                className={`p-3 cursor-pointer hover:bg-gray-200 transition ${orderBy === "interactions" ? "bg-blue-100 font-semibold" : ""}`}
                                onClick={() => setOrderBy("interactions")}>
                                Interactions
                            </th>
                            <th
                                className={`p-3 cursor-pointer hover:bg-gray-200 transition ${orderBy === "date" ? "bg-blue-100 font-semibold" : ""}`}
                                onClick={() => setOrderBy("date")}>
                                Date
                            </th>
                        </tr>

                    </thead>
                    <tbody>
                        {metrics.map((m, i) => (
                            <tr key={i} className="border-t hover:bg-blue-50 transition">
                                <td className="p-2 text-center">{m.account_id}</td>
                                <td className="p-2 text-center">{m.campaign_id}</td>
                                {role === "admin" && <td className="p-2 text-center">{m.cost_micros}</td>}
                                <td className="p-2 text-center">{m.clicks}</td>
                                <td className="p-2 text-center">{m.conversions}</td>
                                <td className="p-2 text-center">{m.impressions}</td>
                                <td className="p-2 text-center">{m.interactions}</td>
                                <td className="p-2 text-center">{m.date}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Paginação */}
            <div className="flex gap-2 mt-4 justify-center flex-wrap">
                <button
                    disabled={page === 0}
                    onClick={() => setPage((p) => p - 1)}
                    className="px-4 py-2 border rounded-lg hover:bg-gray-100 transition disabled:opacity-50">
                    Anterior
                </button>
                <button
                    onClick={() => setPage((p) => p + 1)}
                    className="px-4 py-2 border rounded-lg hover:bg-gray-100 transition">
                    Próximo
                </button>
            </div>
        </div>
    );
}
