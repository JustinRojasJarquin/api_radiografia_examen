import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../api/api";
import Navbar from "../components/Navbar";
import RecordForm from "../components/RecordForm";

export default function EditRecord() {
  const { id } = useParams();
  const [record, setRecord] = useState<any>(null);

  useEffect(() => {
    fetchRecord();
  }, []);

  const fetchRecord = async () => {
    try {
      const res = await API.get(`/records/${id}/`);
      setRecord(res.data);
    } catch (error) {
      console.error(error);
      alert("Could not load record");
    }
  };

  const handleUpdate = async (formData: FormData) => {
    try {
      const payload: any = {
        patient_full_name: formData.get("patient_full_name"),
        patient_identifier: formData.get("patient_identifier"),
        clinical_reference: formData.get("clinical_reference"),
        study_date: formData.get("study_date"),
      };

      await API.put(`/records/${id}/`, payload);

      alert("Record updated successfully");
      window.location.href = "/records";
    } catch (error) {
      console.error(error);
      alert("Could not update record");
    }
  };

  return (
    <div style={styles.page}>
      <Navbar />
      <div style={styles.container}>
        <div style={styles.headerCard}>
          <p style={styles.label}>Actualizacion clinica</p>
          <h1 style={styles.title}>Editar registro</h1>
          <p style={styles.subtitle}>
            Actualizar información del paciente y detalles de la estudio radiográfico.
          </p>
        </div>

        {record && (
          <RecordForm
            initialValues={record}
            onSubmit={handleUpdate}
            submitText="Update Record"
          />
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