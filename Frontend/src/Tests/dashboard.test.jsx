import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import Dashboard from "../Dashboard";

describe("Dashboard", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test("deve adicionar uma nova transação", () => {
    render(<Dashboard sair={() => {}} />);

    fireEvent.change(screen.getByPlaceholderText("Descrição"), {
      target: { value: "Freelance" },
    });

    fireEvent.change(screen.getByPlaceholderText("Valor"), {
      target: { value: "500" },
    });

    fireEvent.change(screen.getByDisplayValue("Receita"), {
      target: { value: "receita" },
    });

    fireEvent.click(screen.getByText("Adicionar"));

    expect(screen.getByText("Freelance")).toBeInTheDocument();
  });

  test("deve remover uma transação", () => {
  render(<Dashboard sair={() => {}} />);

  expect(screen.getByText("Mercado")).toBeInTheDocument();

  const linhaMercado = screen.getByText("Mercado").closest("div");

  const botaoRemover =
    linhaMercado.parentElement.querySelector("button:last-child");

  fireEvent.click(botaoRemover);

  expect(screen.queryByText("Mercado")).not.toBeInTheDocument();
});

  test("deve salvar transações no localStorage", () => {
    render(<Dashboard sair={() => {}} />);

    fireEvent.change(screen.getByPlaceholderText("Descrição"), {
      target: { value: "Pix" },
    });

    fireEvent.change(screen.getByPlaceholderText("Valor"), {
      target: { value: "1000" },
    });

    fireEvent.click(screen.getByText("Adicionar"));

    const dadosSalvos = JSON.parse(
      localStorage.getItem("bytebank_transacoes")
    );

    expect(dadosSalvos.some((item) => item.descricao === "Pix")).toBe(true);
  });
});