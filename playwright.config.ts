import { defineConfig, devices } from "@playwright/test";

const DEFAULT_BASE_URL = "http://127.0.0.1:3000";
const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? DEFAULT_BASE_URL;
const isCI = !!process.env.CI;

// Chromium Smoke Test 전용 설정. Firefox·WebKit 프로젝트, 시각적 회귀,
// 성능 테스트는 추가하지 않는다(CLAUDE.md 규칙 18).
export default defineConfig({
  testDir: "tests/e2e",
  fullyParallel: true,
  forbidOnly: isCI,
  retries: isCI ? 1 : 0,
  reporter: [["list"], ["html", { outputFolder: "playwright-report", open: "never" }]],
  use: {
    baseURL,
    screenshot: "only-on-failure",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  // PLAYWRIGHT_BASE_URL이 지정되면(예: Vercel Preview URL) 이미 떠 있는 서버를 대상으로
  // 하므로 로컬 dev 서버를 별도로 띄우지 않는다. 지정되지 않은 로컬 실행에서만
  // `npm run dev`를 webServer로 사용한다.
  webServer: process.env.PLAYWRIGHT_BASE_URL
    ? undefined
    : {
        command: "npm run dev",
        url: baseURL,
        reuseExistingServer: !isCI,
        timeout: 120_000,
      },
});
