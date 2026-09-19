import { defineConfig } from "vitest/config";

// Unit Test 전용 설정. tests/e2e(Playwright)는 여기서 검색하지 않는다.
// 아직 Unit Test 파일이 없는 단계에서는 passWithNoTests로 통과 처리한다.
export default defineConfig({
  test: {
    environment: "node",
    include: ["src/**/*.{test,spec}.{ts,tsx}", "tests/unit/**/*.{test,spec}.{ts,tsx}"],
    exclude: ["tests/e2e/**", "node_modules/**", ".next/**"],
    passWithNoTests: true,
  },
});
