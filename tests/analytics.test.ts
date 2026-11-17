import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { summarize, exportAnalysis } from '../scripts/exportar-t4f';
import { validateDataset } from '../vendor/t4f/src/lib/validation/dataset';
import { forecastDemand } from '../vendor/t4f/src/lib/forecasting/models';
import { nps } from '../vendor/t4f/src/lib/analytics/metrics';
import type { Filters } from '../vendor/t4f/src/types/domain';

const load = (file: string): unknown => JSON.parse(readFileSync(file, 'utf8')) as unknown;
const fixture = validateDataset(load('vendor/t4f/tests/fixtures/kpi-reference.json'));
const cases = load('vendor/t4f/tests/fixtures/kpi-reference-expected.json') as {
  name: string; filters: Filters; expected: Record<string, number>;
}[];

for (const scenario of cases) {
  test(`carteira manual independente: ${scenario.name}`, () => {
    const result = summarize(fixture, scenario.filters);
    for (const [key, expected] of Object.entries(scenario.expected)) {
      const alias = key === 'confirmedBookings' ? 'confirmed' : key;
      const actual = result[alias as keyof typeof result];
      assert.equal(typeof actual, 'number', key);
      assert.ok(Math.abs((actual as number) - expected) < 1e-6, `${key}: ${actual} != ${expected}`);
    }
  });
}

test('nega snapshot malformado e origem não demonstrativa', () => {
  assert.throws(() => exportAnalysis({}));
  const data = structuredClone(fixture);
  data.bookings[0].departureId = 'inexistente';
  assert.throws(() => exportAnalysis(data));
  assert.throws(() => exportAnalysis({ ...fixture, metadata: { ...fixture.metadata, source_type: 'real' } }));
});

test('nega chaves repetidas e pagamento acima do contratado', () => {
  const duplicate = structuredClone(fixture);
  duplicate.bookings.push(duplicate.bookings[0]);
  assert.throws(() => exportAnalysis(duplicate));
  const excessive = structuredClone(fixture);
  excessive.payments[0].amount = 1e12;
  assert.throws(() => exportAnalysis(excessive));
});

test('NPS e previsão sem amostra não inventam evidência', () => {
  assert.equal(nps([]), null);
  assert.equal(nps([0, 7, 10]), 0);
  assert.equal(forecastDemand([], 6).selected, null);
});

test('demanda futura confirmada permanece fora do treino histórico', () => {
  const raw = validateDataset(load('data/raw/t4f-demo.json'));
  const result = exportAnalysis(raw);
  assert.equal(result.forecast.history.length, 34);
  assert.equal(result.forecast.history.reduce((sum, row) => sum + row.travelers, 0), 188);
  assert.ok(result.forecast.history.every(row => row.month <= '2026-10'));
  assert.equal(result.forecast.selectedId, 'ridge');
  assert.equal(result.forecast.independentTest, true);
  assert.equal(result.historical.totalRevenue, result.historical.realizedRevenue + result.historical.contractedFuture);
});
