import API from "../api/api";
import Navbar from "../components/Navbar";
import RecordForm from "../components/RecordForm";

export default function CreateRecord() {
  const handleCreate = async (formData: FormData) => {
    try {
      await API.post("/records/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert("Record created successfully");
      window.location.href = "/records";
    } catch (error) {
      console.error(error);
      alert("Could not create record");
    }
  };

  return (
    <div style={styles.page}>
      <Navbar />
      <div style={styles.container}>
        <div style={styles.headerCard}>
          <p style={styles.label}>Registro clinico</p>
          <h1 style={styles.title}>Crear registro</h1>
          <p style={styles.subtitle}>
            Registrar un nuevo estudio radiográfico con la información del paciente correspondiente.
          </p>
        </div>

        <RecordForm onSubmit={handleCreate} submitText="Create Record" />
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
    maxWidth: "960px",
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
  label: {
    margin: 0,
    color: "#0056b3",
    fontWeight: 700,
    fontSize: "0.9rem",
    textTransform: "uppercase" as const,
  },
  title: {
    margin: "0.5rem 0",
    color: "#123c74",
    fontSize: "2rem",
  },
  subtitle: {
    margin: 0,
    color: "#5a6470",
  },
};