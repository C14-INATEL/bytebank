import { useState } from "react";
import Login from "./Login";
import Cadastro from "./Cadastro";

function App() {
  const [tela, setTela] = useState("login"); // 👈 AQUI

  return (
    <>
      {tela === "login" ? (
        <Login mudarTela={() => setTela("cadastro")} />
      ) : (
        <Cadastro mudarTela={() => setTela("login")} />
      )}
    </>
  );
}

export default App;