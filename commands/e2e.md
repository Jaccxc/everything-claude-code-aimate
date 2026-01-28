---
description: Generate and run end-to-end tests for web interfaces. Creates test journeys and runs tests with Playwright.
---

# E2E Command

This command invokes the **e2e-runner** agent to generate and execute end-to-end tests.

## What This Command Does

1. **Generate Test Journeys** - Create Playwright tests for user flows
2. **Run E2E Tests** - Execute tests across browsers
3. **Capture Artifacts** - Screenshots, videos, traces on failures
4. **Identify Flaky Tests** - Quarantine unstable tests

## When to Use

Use `/e2e` when:
- Testing critical user journeys in web frontend
- Verifying multi-step flows work end-to-end
- Testing UI interactions and navigation
- Validating integration between frontend and backend API
- Preparing for production deployment

## How It Works

The e2e-runner agent will:

1. **Analyze user flow** and identify test scenarios
2. **Generate Playwright test** using Page Object Model pattern
3. **Run tests** across multiple browsers
4. **Capture failures** with screenshots, videos, and traces
5. **Generate report** with results and artifacts

## Running Tests

```bash
# Run all E2E tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/login.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Debug test
npx playwright test --debug

# Generate test code
npx playwright codegen http://localhost:3000

# View report
npx playwright show-report
```

## Test Artifacts

When tests run, the following artifacts are captured:

**On All Tests:**
- HTML Report with timeline and results

**On Failure Only:**
- Screenshot of the failing state
- Video recording of the test
- Trace file for debugging
- Console logs

## Best Practices

**DO:**
- ✅ Use Page Object Model for maintainability
- ✅ Use data-testid attributes for selectors
- ✅ Wait for API responses, not arbitrary timeouts
- ✅ Test critical user journeys end-to-end
- ✅ Review artifacts when tests fail

**DON'T:**
- ❌ Use brittle selectors (CSS classes can change)
- ❌ Test implementation details
- ❌ Ignore flaky tests
- ❌ Test every edge case with E2E (use unit tests)

## Integration with Backend API

For testing frontend that calls your FastAPI backend:

```typescript
// Wait for API response
await page.waitForResponse(resp =>
  resp.url().includes('/api/users') && resp.status() === 200
)

// Verify API response in UI
await expect(page.locator('[data-testid="user-name"]')).toContainText('John')
```

## Integration with Other Commands

- Use `/plan` to identify critical journeys to test
- Use `/tdd` for unit tests (faster, more granular)
- Use `/e2e` for integration and user journey tests
- Use `/code-review` to verify test quality

## Related Agents

This command invokes the `e2e-runner` agent located at:
`~/.claude/agents/e2e-runner.md`
