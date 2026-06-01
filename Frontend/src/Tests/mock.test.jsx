import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import { vi } from "vitest";

import Login from "../Login";
import Dashboard from "../Dashboard";

describe("Testes com Mock - ByteBank", () => {

  test("deve chamar irDashboard após login válido", async () => {
    // Mock do fetch para simular resposta bem-sucedida da API
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ token: "fake-jwt-token" }),
      })
    );

    const irDashboardMock = vi.fn();
    const mudarTelaMock = vi.fn();

    render(
      <Login
        mudarTela={mudarTelaMock}
        irDashboard={irDashboardMock}
      />
    );

    fireEvent.change(screen.getByPlaceholderText("Seu email"), {
      target: { value: "teste@email.com" },
    });

    fireEvent.change(screen.getByPlaceholderText("Sua senha"), {
      target: { value: "123456" },
    });

    fireEvent.click(screen.getByText("Entrar"));

    await waitFor(() => {
      expect(irDashboardMock).toHaveBeenCalled();
    });

    vi.restoreAllMocks();
  });

  test("deve chamar sair ao clicar no botão sair do dashboard", () => {
    const sairMock = vi.fn();

    render(<Dashboard sair={sairMock} />);

    fireEvent.click(screen.getByText(/Sair/i));

    expect(sairMock).toHaveBeenCalled();
  });

});
