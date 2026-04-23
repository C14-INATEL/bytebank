import { useState } from "react";
import Login from "./Login";
import Cadastro from "./Cadastro";
import Dashboard from "./Dashboard";

function App() {
  const [tela, setTela] = useState("login");

  return (
    <>
      {tela === "login" && (
        <Login
          mudarTela={() => setTela("cadastro")}
          irDashboard={() => setTela("dashboard")}
        />
      )}

      {tela === "cadastro" && (
        <Cadastro mudarTela={() => setTela("login")} />
      )}

      {tela === "dashboard" && (
        <Dashboard sair={() => setTela("login")} />
      )}
    </>
  );
}

export default App;