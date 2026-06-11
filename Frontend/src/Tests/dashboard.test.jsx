import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import { vi } from "vitest";
import Dashboard from "../Dashboard";

// Transações fictícias que simulam resposta da API
const transacoesMock = [
  { _id: "1", description: "Mercado", type: "despesa", amount: 200, category: "alimentacao", date: new Date().toISOString() },
  { _id: "2", description: "Salário", type: "receita", amount: 3000, category: "salario", date: new Date().toISOString() },
];

function mockFetch(respostaInicial = transacoesMock) {
  global.fetch = vi.fn((url, options) => {
    const method = options?.method || "GET";

    // POST — adicionar transação: retorna a nova + existentes
    if (method === "POST") {
      const body = JSON.parse(options.body);
      const nova = { _id: "99", ...body };
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(nova),
      });
    }

    // DELETE — remover transação
    if (method === "DELETE") {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    }

    // GET — lista de transações
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve(respostaInicial),
    });
  });
}

describe("Dashboard", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  test("deve renderizar transações carregadas da API", async () => {
    mockFetch();
    render(<Dashboard sair={() => {}} />);

    await waitFor(() => {
      expect(screen.getByText("Mercado")).toBeInTheDocument();
    });

    expect(screen.getAllByText("Salário").length).toBeGreaterThan(0);
  });

  test("deve adicionar uma nova transação chamando a API", async () => {
    // Primeiro GET retorna mock inicial; após POST o GET retorna mock + nova
    const transacoesAposAdd = [
      ...transacoesMock,
      { _id: "99", description: "Freelance", type: "receita", amount: 500, category: "outros", date: new Date().toISOString() },
    ];

    let chamadas = 0;
    global.fetch = vi.fn((url, options) => {
      const method = options?.method || "GET";
      if (method === "POST") {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
      }
      // 1ª chamada GET retorna inicial; as seguintes retornam com a nova transação
      chamadas++;
      const dados = chamadas === 1 ? transacoesMock : transacoesAposAdd;
      return Promise.resolve({ ok: true, json: () => Promise.resolve(dados) });
    });

    render(<Dashboard sair={() => {}} />);

    // Espera carregar
    await waitFor(() => expect(screen.getByText("Mercado")).toBeInTheDocument());

    fireEvent.change(screen.getByPlaceholderText("Descrição"), {
      target: { value: "Freelance" },
    });
    fireEvent.change(screen.getByPlaceholderText("Valor (ex: 0.00)"), {
      target: { value: "500" },
    });
    fireEvent.click(screen.getByText("Adicionar"));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/transactions"),
        expect.objectContaining({ method: "POST" })
      );
    });
  });

  test("deve chamar a API de delete ao remover uma transação", async () => {
    mockFetch();
    render(<Dashboard sair={() => {}} />);

    await waitFor(() => expect(screen.getByText("Mercado")).toBeInTheDocument());

    // Confirma o dialog de confirmação automaticamente
    vi.spyOn(window, "confirm").mockReturnValue(true);

    const linhaMercado = screen.getByText("Mercado").closest("div");
    const botaoRemover = linhaMercado.parentElement.querySelector("button:last-child");
    fireEvent.click(botaoRemover);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/transactions/1"),
        expect.objectContaining({ method: "DELETE" })
      );
    });

    vi.restoreAllMocks();
  });
});
