import { useState } from "react";

type Props = {
  initialValues?: any;
  onSubmit: (formData: FormData) => Promise<void>;
  submitText: string;
};

export default function RecordForm({ initialValues, onSubmit, submitText }: Props) {
  const [patientFullName, setPatientFullName] = useState(initialValues?.patient_full_name || "");
  const [patientIdentifier, setPatientIdentifier] = useState(initialValues?.patient_identifier || "");
  const [clinicalReference, setClinicalReference] = useState(initialValues?.clinical_reference || "");
  const [studyDate, setStudyDate] = useState(initialValues?.study_date || "");
  const [image, setImage] = useState<File | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("patient_full_name", patientFullName);
    formData.append("patient_identifier", patientIdentifier);
    formData.append("clinical_reference", clinicalReference);
    formData.append("study_date", studyDate);

    if (image) {
      formData.append("image", image);
    }

    await onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <div style={styles.fieldGroup}>
        <label style={styles.label}>Nombre del paciente</label>
        <input
          style={styles.input}
          type="text"
          placeholder="Ingrese el nombre completo del paciente"
          value={patientFullName}
          onChange={(e) => setPatientFullName(e.target.value)}
          required
        />
      </div>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>Cedula del paciente</label>
        <input
          style={styles.input}
          type="text"
          placeholder="Ingrese la cedula del paciente"
          value={patientIdentifier}
          onChange={(e) => setPatientIdentifier(e.target.value)}
          required
        />
      </div>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>Referencia clínica</label>
        <textarea
          style={styles.textarea}
          placeholder="Ingrese la referencia clinica"
          value={clinicalReference}
          onChange={(e) => setClinicalReference(e.target.value)}
          required
        />
      </div>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>Fecha del estudio</label>
        <input
          style={styles.input}
          type="date"
          value={studyDate}
          onChange={(e) => setStudyDate(e.target.value)}
          required
        />
      </div>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>Imagen radiográfica</label>
        <input
          style={styles.fileInput}
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files?.[0] || null)}
        />
      </div>

      <button type="submit" style={styles.submitButton}>
        {submitText}
      </button>
    </form>
  );
}

const styles = {
  form: {
    background: "#ffffff",
    border: "1px solid #dbe8f4",
    borderRadius: "18px",
    padding: "2rem",
    boxShadow: "0 10px 24px rgba(0,0,0,0.06)",
    display: "flex",
    flexDirection: "column" as const,
    gap: "1.2rem",
  },
  fieldGroup: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "0.45rem",
  },
  label: {
    color: "#23456d",
    fontWeight: 700,
    fontSize: "0.95rem",
  },
  input: {
    padding: "0.9rem 1rem",
    borderRadius: "12px",
    border: "1px solid #c8d8e8",
    background: "#fdfefe",
    fontSize: "1rem",
  },
  textarea: {
    minHeight: "120px",
    padding: "0.9rem 1rem",
    borderRadius: "12px",
    border: "1px solid #c8d8e8",
    resize: "vertical" as const,
    fontSize: "1rem",
  },
  fileInput: {
    padding: "0.8rem",
    borderRadius: "12px",
    border: "1px solid #c8d8e8",
    background: "#fff",
  },
  submitButton: {
    background: "#0056b3",
    color: "#ffffff",
    border: "none",
    borderRadius: "12px",
    padding: "0.95rem 1rem",
    fontWeight: 700,
    fontSize: "1rem",
    cursor: "pointer",
    marginTop: "0.5rem",
  },
};