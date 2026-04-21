import { useEffect, useState } from "react";
import API from "../api/api";
import Navbar from "../components/Navbar";
import RecordCard from "../components/RecordCard";

export default function Records() {
  const [records, setRecords] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(20);
  const [total, setTotal] = useState<number>(0);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/";
      return;
    }

    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      const res = await API.get("/records/");
      console.log("Records response:", res.data);

      if (Array.isArray(res.data)) {
        setRecords(res.data);
        setTotal(res.data.length);
        setPage(1);
        setPageSize(res.data.length || 20);
      } else if (Array.isArray(res.data.results)) {
        setRecords(res.data.results);
        setTotal(res.data.total ?? 0);
        setPage(res.data.page ?? 1);
        setPageSize(res.data.page_size ?? 20);
      } else {
        console.error("Expected a paginated object or array but got:", res.data);
        setRecords([]);
        setTotal(0);
      }
    } catch (error) {
      console.error("Error loading records:", error);
      alert("Could not load records");
      setRecords([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this record?");
    if (!confirmDelete) return;

    try {
      await API.delete(`/records/${id}/`);
      await fetchRecords();
    } catch (error) {
      console.error("Delete error:", error);
      alert("Could not delete record");
    }
  };

  const handleViewImage = async (id: number) => {
    try {
      const res = await API.get(`/records/${id}/signed-image-url/`);
      window.open(res.data.signed_url, "_blank");
    } catch (error) {
      console.error("Signed image error:", error);
      alert("Could not open secure image");
    }
  };

  return (
    <div style={styles.page}>
      <Navbar />

      <div style={styles.container}>
        <div style={styles.headerCard}>
          <div>
            <p style={styles.sectionLabel}>Gestión clínica</p>
            <h1 style={styles.title}>Registros radiográficos</h1>
            <p style={styles.subtitle}>
              
            </p>
          </div>
        </div>

        <div style={styles.summaryGrid}>
          <div style={styles.summaryCard}>
            <span style={styles.summaryTitle}>Registros totales</span>
            <strong style={styles.summaryValue}>{total}</strong>
          </div>

          <div style={styles.summaryCard}>
            <span style={styles.summaryTitle}>Página actual</span>
            <strong style={styles.summaryValue}>{page}</strong>
          </div>

          <div style={styles.summaryCard}>
            <span style={styles.summaryTitle}>Tamaño de página</span>
            <strong style={styles.summaryValue}>{pageSize}</strong>
          </div>
        </div>

        {loading ? (
          <div style={styles.stateBox}>Cargando registros...</div>
        ) : records.length === 0 ? (
          <div style={styles.stateBox}>
            <h3 style={{ marginTop: 0 }}>No existen registros disponibles</h3>
            <p style={{ marginBottom: 0 }}>
              Cree su primer registro radiográfico desde la sección crear registro.
            </p>
          </div>
        ) : (
          <div style={styles.recordsGrid}>
            {records.map((record) => (
              <RecordCard
                key={record.id}
                record={record}
                onDelete={handleDelete}
                onViewImage={handleViewImage}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f2f6fb",
  },
  container: {
    maxWidth: "1180px",
    margin: "0 auto",
    padding: "2rem",
  },
  headerCard: {
    background: "linear-gradient(135deg, #ffffff 0%, #eef5fc 100%)",
    border: "1px solid #d7e4f2",
    borderRadius: "18px",
    padding: "2rem",
    marginBottom: "1.5rem",
    boxShadow: "0 8px 24px rgba(28, 71, 125, 0.08)",
  },
  sectionLabel: {
    margin: 0,
    color: "#0056b3",
    fontWeight: 700,
    fontSize: "0.9rem",
    textTransform: "uppercase" as const,
    letterSpacing: "0.05em",
  },
  title: {
    margin: "0.5rem 0 0.5rem 0",
    fontSize: "2.2rem",
    color: "#123c74",
  },
  subtitle: {
    margin: 0,
    color: "#5a6470",
    maxWidth: "720px",
  },
  summaryGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "1rem",
    marginBottom: "1.5rem",
  },
  summaryCard: {
    background: "#ffffff",
    border: "1px solid #dbe8f4",
    borderRadius: "14px",
    padding: "1rem 1.25rem",
    boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
  },
  summaryTitle: {
    display: "block",
    color: "#5f6b79",
    fontSize: "0.95rem",
    marginBottom: "0.5rem",
  },
  summaryValue: {
    color: "#0b3d91",
    fontSize: "1.5rem",
  },
  recordsGrid: {
    display: "grid",
    gap: "1rem",
  },
  stateBox: {
    background: "#ffffff",
    border: "1px solid #dbe8f4",
    borderRadius: "16px",
    padding: "2rem",
    textAlign: "center" as const,
    boxShadow: "0 6px 16px rgba(0,0,0,0.05)",
  },
};