import { useEffect, useMemo, useState } from "react";

function Dashboard({ sair }) {
  const [descricao, setDescricao] = useState("");
  const [valor, setValor] = useState("");
  const [tipo, setTipo] = useState("receita");
  const [erro, setErro] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  const [transacoes, setTransacoes] = useState(() => {
    const transacoesSalvas = localStorage.getItem("bytebank_transacoes");

    if (transacoesSalvas) {
      return JSON.parse(transacoesSalvas);
    }

    return [
      { id: 1, descricao: "Salário", tipo: "receita", valor: 3500 },
      { id: 2, descricao: "Mercado", tipo: "despesa", valor: 280 },
      { id: 3, descricao: "Uber", tipo: "despesa", valor: 45.5 },
    ];
  });

  useEffect(() => {
    localStorage.setItem("bytebank_transacoes", JSON.stringify(transacoes));
  }, [transacoes]);

  const receitas = useMemo(
    () =>
      transacoes
        .filter((item) => item.tipo === "receita")
        .reduce((acc, item) => acc + item.valor, 0),
    [transacoes]
  );

  const despesas = useMemo(
    () =>
      transacoes
        .filter((item) => item.tipo === "despesa")
        .reduce((acc, item) => acc + item.valor, 0),
    [transacoes]
  );

  const saldo = receitas - despesas;
  const totalMovimentado = receitas + despesas;

  const formatarMoeda = (numero) =>
    numero.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });

  const limparFormulario = () => {
    setDescricao("");
    setValor("");
    setTipo("receita");
    setErro("");
    setEditandoId(null);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!descricao || !valor) {
      setErro("Preencha descrição e valor");
      return;
    }

    const valorNumero = Number(valor);

    if (Number.isNaN(valorNumero) || valorNumero <= 0) {
      setErro("Digite um valor válido");
      return;
    }

    if (editandoId) {
      setTransacoes(
        transacoes.map((item) =>
          item.id === editandoId
            ? { ...item, descricao, tipo, valor: valorNumero }
            : item
        )
      );
      limparFormulario();
      return;
    }

    setTransacoes([
      { id: Date.now(), descricao, tipo, valor: valorNumero },
      ...transacoes,
    ]);

    limparFormulario();
  };

  const editarTransacao = (item) => {
    setDescricao(item.descricao);
    setValor(String(item.valor));
    setTipo(item.tipo);
    setEditandoId(item.id);
    setErro("");
  };

  const removerTransacao = (id) => {
    setTransacoes(transacoes.filter((item) => item.id !== id));

    if (editandoId === id) {
      limparFormulario();
    }
  };

  return (
    <div style={styles.page}>
      <aside style={styles.sidebar}>
        <div>
          <h1 style={styles.sidebarLogo}>ByteBank</h1>

          <p style={styles.menuTitle}>MENU</p>

          <button style={styles.menuActive}>🏠 Dashboard</button>
          <button style={styles.menuItem}>💸 Transações</button>
          <button style={styles.menuItem}>💳 Cartões</button>
          <button style={styles.menuItem}>📊 Análises</button>
          <button style={styles.menuItem}>🕘 Histórico</button>

          <p style={styles.menuTitle}>GERAL</p>

          <button style={styles.menuItem}>⚙️ Configurações</button>
          <button style={styles.menuItem}>❓ Ajuda</button>
        </div>

        <button style={styles.logoutButton} onClick={sair}>
          🚪 Sair
        </button>
      </aside>

      <main style={styles.main}>
        <div style={styles.header}>
          <div>
            <h2 style={styles.welcome}>Bem-vindo ao ByteBank 👋</h2>
            <p style={styles.subtitle}>Controle suas receitas e despesas</p>
          </div>

          <input
            style={styles.search}
            placeholder="Buscar transação..."
            type="text"
          />
        </div>

        <section style={styles.cards}>
          <div style={styles.card}>
            <p style={styles.cardLabel}>Receita total</p>
            <h3 style={styles.greenText}>{formatarMoeda(receitas)}</h3>
            <small style={styles.smallGreen}>▲ Entradas registradas</small>
          </div>

          <div style={styles.card}>
            <p style={styles.cardLabel}>Despesa total</p>
            <h3 style={styles.redText}>{formatarMoeda(despesas)}</h3>
            <small style={styles.smallRed}>▼ Saídas registradas</small>
          </div>

          <div style={styles.card}>
            <p style={styles.cardLabel}>Saldo atual</p>
            <h3 style={saldo >= 0 ? styles.greenText : styles.redText}>
              {formatarMoeda(saldo)}
            </h3>
            <small style={styles.smallText}>Resultado financeiro</small>
          </div>

          <div style={styles.card}>
            <p style={styles.cardLabel}>Total de transações</p>
            <h3 style={styles.whiteText}>{transacoes.length}</h3>
            <small style={styles.smallText}>Movimentações cadastradas</small>
          </div>
        </section>

        <section style={styles.grid}>
          <div style={styles.panelLarge}>
            <div style={styles.panelHeader}>
              <h3 style={styles.panelTitle}>Resumo financeiro</h3>
              <span style={styles.badge}>Mensal</span>
            </div>

            <div style={styles.chartBox}>
              <div style={styles.chartLineGreen}></div>
              <div style={styles.chartLineYellow}></div>
              <div style={styles.chartInfo}>
                <p style={styles.chartValue}>{formatarMoeda(totalMovimentado)}</p>
                <p style={styles.smallText}>Total movimentado</p>
              </div>
            </div>
          </div>

          <div style={styles.panel}>
            <h3 style={styles.panelTitle}>Meu cartão</h3>

            <div style={styles.creditCard}>
              <p style={styles.cardBank}>BYTEBANK</p>
              <p style={styles.cardNumber}>•••• •••• •••• 7390</p>
              <div style={styles.cardBottom}>
                <span>Luiz Otavio</span>
                <span>12/29</span>
              </div>
            </div>

            <button style={styles.addCardButton}>+ Adicionar novo cartão</button>
          </div>

          <div style={styles.panel}>
            <h3 style={styles.panelTitle}>
              {editandoId ? "Editar transação" : "Nova transação"}
            </h3>

            <p style={styles.error}>{erro || " "}</p>

            <form onSubmit={handleSubmit} style={styles.form}>
              <input
                style={styles.input}
                placeholder="Descrição"
                value={descricao}
                onChange={(e) => {
                  setDescricao(e.target.value);
                  setErro("");
                }}
              />

              <input
                style={styles.input}
                type="number"
                step="0.01"
                placeholder="Valor"
                value={valor}
                onChange={(e) => {
                  setValor(e.target.value);
                  setErro("");
                }}
              />

              <select
                style={styles.input}
                value={tipo}
                onChange={(e) => setTipo(e.target.value)}
              >
                <option value="receita">Receita</option>
                <option value="despesa">Despesa</option>
              </select>

              <button style={styles.primaryButton} type="submit">
                {editandoId ? "Salvar edição" : "Adicionar"}
              </button>

              {editandoId && (
                <button
                  style={styles.secondaryButton}
                  type="button"
                  onClick={limparFormulario}
                >
                  Cancelar edição
                </button>
              )}
            </form>
          </div>

          <div style={styles.panelLarge}>
            <div style={styles.panelHeader}>
              <h3 style={styles.panelTitle}>Últimas transações</h3>
              <span style={styles.smallText}>Ver todas</span>
            </div>

            <div style={styles.transactions}>
              {transacoes.map((item) => (
                <div key={item.id} style={styles.transactionRow}>
                  <div>
                    <p style={styles.transactionTitle}>{item.descricao}</p>
                    <p style={styles.transactionType}>
                      {item.tipo === "receita" ? "Receita" : "Despesa"}
                    </p>
                  </div>

                  <div style={styles.transactionActions}>
                    <strong
                      style={
                        item.tipo === "receita"
                          ? styles.greenTextSmall
                          : styles.redTextSmall
                      }
                    >
                      {item.tipo === "receita" ? "+" : "-"}{" "}
                      {formatarMoeda(item.valor)}
                    </strong>

                    <button
                      style={styles.editButton}
                      onClick={() => editarTransacao(item)}
                    >
                      Editar
                    </button>

                    <button
                      style={styles.removeButton}
                      onClick={() => removerTransacao(item.id)}
                    >
                      Remover
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div style={styles.panel}>
            <h3 style={styles.panelTitle}>Visão geral</h3>

            <div style={styles.circle}>
              <div>
                <h2 style={styles.circleValue}>{formatarMoeda(saldo)}</h2>
                <p style={styles.smallText}>Saldo atual</p>
              </div>
            </div>

            <div style={styles.legend}>
              <span style={styles.legendItem}>🟢 Receitas</span>
              <span style={styles.legendItem}>🔴 Despesas</span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    background: "#0f172a",
    color: "#fff",
    fontFamily: "Arial, sans-serif",
  },
  sidebar: {
    width: "230px",
    background: "#020617",
    padding: "24px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
  },
  sidebarLogo: {
    color: "#22c55e",
    marginBottom: "35px",
  },
  menuTitle: {
    color: "#64748b",
    fontSize: "12px",
    marginTop: "25px",
  },
  menuActive: {
    width: "100%",
    background: "#1e293b",
    color: "#fff",
    border: "1px solid #334155",
    borderRadius: "10px",
    padding: "12px",
    textAlign: "left",
    marginBottom: "8px",
    cursor: "pointer",
  },
  menuItem: {
    width: "100%",
    background: "transparent",
    color: "#94a3b8",
    border: "none",
    borderRadius: "10px",
    padding: "12px",
    textAlign: "left",
    marginBottom: "6px",
    cursor: "pointer",
  },
  logoutButton: {
    background: "#ef4444",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    padding: "12px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  main: {
    flex: 1,
    padding: "28px",
    overflow: "auto",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "25px",
    gap: "20px",
  },
  welcome: {
    margin: 0,
    fontSize: "28px",
  },
  subtitle: {
    color: "#94a3b8",
    marginTop: "6px",
  },
  search: {
    width: "260px",
    background: "#1e293b",
    color: "#fff",
    border: "1px solid #334155",
    borderRadius: "10px",
    padding: "12px",
    outline: "none",
  },
  cards: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))",
    gap: "18px",
    marginBottom: "22px",
  },
  card: {
    background: "#1e293b",
    border: "1px solid #334155",
    borderRadius: "18px",
    padding: "20px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.25)",
  },
  cardLabel: {
    color: "#94a3b8",
    margin: "0 0 18px",
  },
  greenText: {
    color: "#22c55e",
    fontSize: "26px",
    margin: 0,
  },
  redText: {
    color: "#ef4444",
    fontSize: "26px",
    margin: 0,
  },
  whiteText: {
    color: "#fff",
    fontSize: "26px",
    margin: 0,
  },
  smallText: {
    color: "#94a3b8",
    fontSize: "13px",
  },
  smallGreen: {
    color: "#86efac",
    fontSize: "13px",
  },
  smallRed: {
    color: "#fca5a5",
    fontSize: "13px",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1.4fr 0.9fr",
    gap: "20px",
  },
  panel: {
    background: "#1e293b",
    border: "1px solid #334155",
    borderRadius: "18px",
    padding: "20px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.25)",
  },
  panelLarge: {
    background: "#1e293b",
    border: "1px solid #334155",
    borderRadius: "18px",
    padding: "20px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.25)",
  },
  panelHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  panelTitle: {
    marginTop: 0,
  },
  badge: {
    background: "#334155",
    color: "#cbd5e1",
    padding: "8px 12px",
    borderRadius: "10px",
    fontSize: "13px",
  },
  chartBox: {
    height: "230px",
    background: "#0f172a",
    borderRadius: "16px",
    position: "relative",
    overflow: "hidden",
    marginTop: "12px",
  },
  chartLineGreen: {
    position: "absolute",
    width: "85%",
    height: "4px",
    background: "#22c55e",
    left: "8%",
    top: "45%",
    transform: "rotate(-8deg)",
    borderRadius: "999px",
  },
  chartLineYellow: {
    position: "absolute",
    width: "70%",
    height: "4px",
    background: "#eab308",
    left: "12%",
    top: "58%",
    transform: "rotate(11deg)",
    borderRadius: "999px",
  },
  chartInfo: {
    position: "absolute",
    left: "30px",
    bottom: "25px",
  },
  chartValue: {
    fontSize: "26px",
    margin: 0,
    fontWeight: "bold",
  },
  creditCard: {
    background: "linear-gradient(135deg, #22c55e, #14b8a6)",
    borderRadius: "18px",
    padding: "22px",
    minHeight: "150px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    marginBottom: "16px",
  },
  cardBank: {
    fontWeight: "bold",
    letterSpacing: "1px",
  },
  cardNumber: {
    fontSize: "20px",
    fontWeight: "bold",
  },
  cardBottom: {
    display: "flex",
    justifyContent: "space-between",
    fontSize: "13px",
  },
  addCardButton: {
    width: "100%",
    background: "#334155",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    padding: "12px",
    cursor: "pointer",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  input: {
    background: "#334155",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    padding: "12px",
    outline: "none",
  },
  error: {
    color: "#ef4444",
    minHeight: "20px",
    fontSize: "14px",
  },
  primaryButton: {
    background: "#22c55e",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    padding: "12px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  secondaryButton: {
    background: "#475569",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    padding: "12px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  transactions: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    marginTop: "10px",
  },
  transactionRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    background: "#334155",
    borderRadius: "14px",
    padding: "14px",
    gap: "12px",
  },
  transactionTitle: {
    margin: 0,
    fontWeight: "bold",
  },
  transactionType: {
    margin: "4px 0 0",
    color: "#cbd5e1",
    fontSize: "13px",
  },
  transactionActions: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    flexWrap: "wrap",
  },
  greenTextSmall: {
    color: "#22c55e",
  },
  redTextSmall: {
    color: "#ef4444",
  },
  editButton: {
    background: "#3b82f6",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    padding: "8px 10px",
    cursor: "pointer",
  },
  removeButton: {
    background: "#475569",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    padding: "8px 10px",
    cursor: "pointer",
  },
  circle: {
    height: "190px",
    borderRadius: "50%",
    border: "18px solid #22c55e",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    margin: "20px auto",
    maxWidth: "190px",
  },
  circleValue: {
    margin: 0,
    textAlign: "center",
  },
  legend: {
    display: "flex",
    justifyContent: "center",
    gap: "18px",
  },
  legendItem: {
    color: "#cbd5e1",
    fontSize: "13px",
  },
};

export default Dashboard;