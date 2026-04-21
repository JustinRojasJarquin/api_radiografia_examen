import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Records from "./pages/Records";
import CreateRecord from "./pages/CreateRecord";
import EditRecord from "./pages/EditRecord";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/records" element={<Records />} />
        <Route path="/records/create" element={<CreateRecord />} />
        <Route path="/records/edit/:id" element={<EditRecord />} />
      </Routes>
    </BrowserRouter>
  );
}