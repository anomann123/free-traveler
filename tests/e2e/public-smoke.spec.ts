import { expect, test } from "@playwright/test";

/**
 * TASK-E2E-PUBLIC-SMOKE / TASK-PAGE-SCR001 / TASK-PAGE-SCR002 / TASK-PAGE-SCR003 관련
 * 공개(비로그인) Smoke: E2E-001~005.
 *
 * Selector 규칙(사용자 지정):
 *   1) role 우선 2) label 우선 3) test id 순으로 사용하고, 텍스트 위치나 CSS 구조에
 *      의존하지 않는다. 외부 사이트로 실제 이동한 뒤 그 사이트의 내용을 검사하지
 *      않는다 — 버튼/링크의 href·target·rel 속성과 비전달 고지 문구까지만 확인한다.
 *
 * 아래 테스트는 아직 구현되지 않은 화면(SCR-001 Starter 제거, SCR-002~005 신규 생성)을
 * 대상으로 하는 "선(先) 명세" 테스트다. 구현 Task가 완료되기 전까지는 실패하는 것이
 * 정상이며, 각 구현 Task(CMP-SCR001-*, PAGE-SCR002, PAGE-SCR003 등)는 아래에서
 * 요구하는 role/label/data-testid 계약을 그대로 제공해야 한다.
 */

// data-testid 계약(구현 Task가 반드시 부여해야 하는 값):
//   destination-card            여행지 카드(국내/해외 공통) — TASK-CMP-SCR001-DEST-DOMESTIC/OVERSEAS
//   hero-travel-tools-cta       SCR-001 Hero의 `/travel-tools` 이동 CTA — TASK-CMP-SCR001-HERO

test.describe("E2E-001~005 공개 Smoke", () => {
  test("E2E-001 메인 페이지의 추천 여행지와 주요 CTA", async ({ page }) => {
    await page.goto("/");

    const destinationCards = page.getByTestId("destination-card");
    await expect(destinationCards.first()).toBeVisible();
    expect(await destinationCards.count()).toBeGreaterThan(0);

    const heroCta = page.getByTestId("hero-travel-tools-cta");
    await expect(heroCta).toBeVisible();
    await expect(heroCta).toHaveAttribute("href", "/travel-tools");
  });

  test("E2E-002 대표 소개의 free_traveler, 50회 이상, 30개국 이상", async ({ page }) => {
    await page.goto("/about");

    // CON-09: 대표 지표는 전역에서 `50+ Trips`, `30+ Countries`로 표현한다.
    await expect(page.getByText("free_traveler", { exact: false }).first()).toBeVisible();
    await expect(page.getByText("50+ Trips", { exact: false }).first()).toBeVisible();
    await expect(page.getByText("30+ Countries", { exact: false }).first()).toBeVisible();
  });

  test("E2E-003 여행 도구의 항공 외부 이동 안내와 href", async ({ page }) => {
    await page.goto("/travel-tools");

    await page.getByRole("tab", { name: "항공편" }).click();
    const flightPanel = page.getByRole("tabpanel", { name: "항공편" });

    // 국가/지역은 드롭다운(select), 출발일/귀국일은 날짜 입력을 가정한다(REQ-FUNC-011).
    // 구현이 다른 컨트롤(예: combobox)을 쓴다면 이 부분만 맞춰 조정한다.
    await flightPanel.getByLabel("국가").selectOption({ index: 1 });
    await flightPanel.getByLabel("지역").selectOption({ index: 1 });
    await flightPanel.getByLabel("출발일").fill("2027-01-10");
    await flightPanel.getByLabel("귀국일").fill("2027-01-15");

    // AC-F03: 유효한 입력 후 "계속" 선택 시 요약+비전달 고지가 표시된다.
    await flightPanel.getByRole("button", { name: "계속" }).click();

    await expect(
      flightPanel.getByText("입력값은 외부 사이트로 전달되지 않습니다", { exact: false }),
    ).toBeVisible();

    // AC-F04: "항공편 보러 가기" 선택 시 설정된 외부 URL을 새 탭으로 연다.
    const outboundLink = flightPanel.getByRole("link", { name: "항공편 보러 가기" });
    await expect(outboundLink).toBeVisible();
    const href = await outboundLink.getAttribute("href");
    expect(href).toBeTruthy();
    expect(href).toMatch(/^https:\/\//);
    // REQ-FUNC-016: 목적지·날짜 query 파라미터를 붙이지 않는다.
    expect(href).not.toMatch(/[?&](country|region|date|from|to)=/i);
    await expect(outboundLink).toHaveAttribute("target", "_blank");
    const rel = await outboundLink.getAttribute("rel");
    expect(rel).toMatch(/noopener/);
    expect(rel).toMatch(/noreferrer/);
    // 실제 외부 사이트로는 이동/검사하지 않는다(새 탭 클릭·콘텐츠 확인 금지).
  });

  test("E2E-004 여행 도구의 숙소 외부 이동 안내와 href", async ({ page }) => {
    await page.goto("/travel-tools");

    await page.getByRole("tab", { name: "숙소" }).click();
    const hotelPanel = page.getByRole("tabpanel", { name: "숙소" });

    await hotelPanel.getByLabel("국가").selectOption({ index: 1 });
    await hotelPanel.getByLabel("지역").selectOption({ index: 1 });
    await hotelPanel.getByLabel("체크인").fill("2027-01-10");
    await hotelPanel.getByLabel("체크아웃").fill("2027-01-12");

    // AC-H03: 유효한 입력 후 "계속" 선택 시 요약+비전달 고지가 표시된다.
    await hotelPanel.getByRole("button", { name: "계속" }).click();

    await expect(
      hotelPanel.getByText("입력값은 외부 사이트로 전달되지 않습니다", { exact: false }),
    ).toBeVisible();

    // AC-H04: "호텔 보러 가기" 선택 시 설정된 외부 URL을 새 탭으로 연다.
    const outboundLink = hotelPanel.getByRole("link", { name: "호텔 보러 가기" });
    await expect(outboundLink).toBeVisible();
    const href = await outboundLink.getAttribute("href");
    expect(href).toBeTruthy();
    expect(href).toMatch(/^https:\/\//);
    expect(href).not.toMatch(/[?&](country|region|date|checkin|checkout)=/i);
    await expect(outboundLink).toHaveAttribute("target", "_blank");
    const rel = await outboundLink.getAttribute("rel");
    expect(rel).toMatch(/noopener/);
    expect(rel).toMatch(/noreferrer/);
  });

  test("E2E-005 비로그인 동행글 작성의 로그인 안내", async ({ page }) => {
    await page.goto("/travel-tools");

    await page.getByRole("tab", { name: "동행 구하기" }).click();

    // TASK-PAGE-SCR003 Visual AC에 정의된 완성형 안내 카드 문구를 그대로 사용한다.
    await expect(page.getByText("로그인하고 동행을 구해보세요", { exact: false })).toBeVisible();
    await expect(page.getByRole("link", { name: /로그인/ })).toBeVisible();
  });
});
