import { expect, test, type Page } from "@playwright/test";

/**
 * TASK-E2E-MATE-AUTH 관련 인증 필요 Smoke: E2E-006~007.
 *
 * 이 파일은 실제 Supabase 테스트 계정이 있어야 의미 있게 실행되므로, 인증 환경변수가
 * 없으면 파일 전체를 명시적으로 skip한다(공개 Smoke인 public-smoke.spec.ts는 이 조건과
 * 무관하게 항상 실행된다).
 *
 * 필요한 환경변수:
 *   E2E_TEST_USER_EMAIL     성인 확인이 완료된 테스트 계정 이메일
 *   E2E_TEST_USER_PASSWORD  위 계정 비밀번호
 *
 * 아직 SCR-003(동행 작성)·SCR-004(동행 조회)·SCR-005(계정) Page가 구현되지 않았으므로
 * 아래 테스트는 "선(先) 명세" 골격이다. 각 구현 Task는 여기서 가정한 role/label 접근성
 * 이름을 그대로 제공해야 한다.
 */

const TEST_EMAIL = process.env.E2E_TEST_USER_EMAIL;
const TEST_PASSWORD = process.env.E2E_TEST_USER_PASSWORD;
const hasAuthEnv = Boolean(TEST_EMAIL && TEST_PASSWORD);

async function login(page: Page): Promise<void> {
  await page.goto("/account");
  await page.getByLabel("이메일").fill(TEST_EMAIL!);
  await page.getByLabel("비밀번호").fill(TEST_PASSWORD!);
  await page.getByRole("button", { name: "로그인" }).click();
}

test.describe("E2E-006~007 동행 인증 Smoke", () => {
  test.skip(
    !hasAuthEnv,
    "E2E_TEST_USER_EMAIL/E2E_TEST_USER_PASSWORD 환경변수가 없어 인증 Smoke를 건너뜁니다(공개 Smoke만 실행).",
  );

  test("E2E-006 로그인 사용자의 동행글 작성과 목록·상세 확인", async ({ page }) => {
    await login(page);

    await page.goto("/travel-tools");
    await page.getByRole("tab", { name: "동행 구하기" }).click();

    const uniqueTitle = `E2E-006 테스트 모집글 ${Date.now()}`;
    await page.getByLabel("제목").fill(uniqueTitle);
    await page.getByLabel("국가").selectOption({ index: 1 });
    await page.getByLabel("지역").selectOption({ index: 1 });
    await page.getByLabel("시작일").fill("2027-02-01");
    await page.getByLabel("종료일").fill("2027-02-05");
    await page.getByLabel("모집 인원").fill("2");
    await page
      .getByLabel("상세 설명")
      .fill("E2E 테스트용 모집글입니다. 연락처는 포함하지 않습니다.");
    await page.getByRole("checkbox", { name: /안전수칙/ }).check();
    await page.getByRole("button", { name: "등록" }).click();

    // TASK-PAGE-SCR003 §Verify: 작성 완료 후 Toast 안내(CMP-SHARED-TOAST)
    await expect(page.getByText(/등록되었습니다|작성되었습니다/)).toBeVisible();

    await page.goto("/mates");
    const createdCard = page.getByRole("link", { name: new RegExp(uniqueTitle) });
    await expect(createdCard).toBeVisible();

    await createdCard.click();
    await expect(page.getByRole("heading", { name: uniqueTitle })).toBeVisible();
  });

  test("E2E-007 동행글 신청과 계정 화면의 내 활동 확인", async ({ page }) => {
    await login(page);

    await page.goto("/mates");
    // TODO(구현 확정 후 조정): 본인이 작성하지 않은 첫 모집글에 참가 요청을 보낸다.
    // 시드 데이터(DB-SEED-BASE)에 테스트 계정 소유가 아닌 모집글이 최소 1건 있어야 한다.
    const firstMateCard = page.getByRole("link", { name: /./ }).first();
    await firstMateCard.click();

    await page.getByLabel("참가 메시지").fill("함께 여행하고 싶습니다. E2E 테스트 메시지입니다.");
    await page.getByRole("button", { name: "참가 요청 보내기" }).click();

    await expect(page.getByText(/요청이 접수되었습니다|신청이 완료되었습니다/)).toBeVisible();

    await page.goto("/account");
    // TASK-CMP-SCR005-MY-ACTIVITY: 참가 요청 목록 탭
    await page.getByRole("tab", { name: "내 활동" }).click();
    await expect(page.getByText(/참가 요청/)).toBeVisible();
  });
});
