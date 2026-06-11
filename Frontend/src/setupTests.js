import { vi } from "vitest";

// ResizeObserver não existe no jsdom (usado pelo recharts)
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Mock completo do recharts para evitar erros de SVG/canvas no jsdom
vi.mock("recharts", () => ({
  ResponsiveContainer: ({ children }) => children,
  BarChart: ({ children }) => children,
  Bar: () => null,
  XAxis: () => null,
  YAxis: () => null,
  CartesianGrid: () => null,
  Tooltip: () => null,
  Legend: () => null,
}));