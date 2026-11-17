import { readFileSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { analyze, DEFAULT_FILTERS, DEFAULT_THRESHOLDS } from '../vendor/t4f/src/lib/analytics/metrics';
import { validateDataset } from '../vendor/t4f/src/lib/validation/dataset';
import { forecastDataset } from '../vendor/t4f/src/lib/forecasting/dataset';
import { seasonalAnalysis, cancellationAnalysis, satisfactionAnalysis } from '../vendor/t4f/src/lib/analytics/statistics';
import { deriveAlerts } from '../vendor/t4f/src/lib/analytics/alerts';
import { detectAnomalies } from '../vendor/t4f/src/lib/analytics/anomalies';
import type { Dataset, Filters } from '../vendor/t4f/src/types/domain';

export function summarize(data: Dataset, filters: Filters) {
  const view = analyze(data, filters);
  return {
    filters, bookings: view.bookings.length, confirmed: view.confirmed.length,
    travelers: view.travelers, servedTravelers: view.servedTravelers,
    uniqueCustomers: view.uniqueCustomers, totalRevenue: view.totalRevenue,
    realizedRevenue: view.realizedRevenue, contractedFuture: view.contractedFuture,
    cost: view.cost, contribution: view.totalRevenue - view.cost,
    ticket: view.ticket, nps: view.nps, responses: view.feedback.length,
    occupancy: view.occupancy, cancellationRate: view.cancellationRate,
    conversion: view.conversion, paid: view.paid,
    capacity: view.allocations.reduce((sum, row) => sum + row.capacity, 0),
    committed: view.allocations.reduce((sum, row) => sum + row.committed, 0),
    shortage: view.allocations.reduce((sum, row) => sum + row.shortage, 0),
    monthly: view.monthly, routes: view.routeStats, slots: view.allocations,
  };
}

export function exportAnalysis(input: unknown) {
  const data = validateDataset(input);
  const filters = { ...DEFAULT_FILTERS, start: data.metadata.historyStart, end: data.metadata.historyEnd };
  const forecast = forecastDataset(data, filters, 6);
  const historical = summarize(data, filters);
  const futureFilters = { ...DEFAULT_FILTERS, start: data.metadata.referenceDate };
  return {
    metadata: data.metadata,
    counts: Object.fromEntries(Object.entries(data).filter(([, value]) => Array.isArray(value)).map(([key, value]) => [key, (value as unknown[]).length])),
    historical, planning: summarize(data, futureFilters),
    seasonality: seasonalAnalysis(forecast.history),
    cancellations: cancellationAnalysis(data, filters),
    satisfaction: satisfactionAnalysis(data, filters), forecast,
    alerts: deriveAlerts(data, DEFAULT_FILTERS, DEFAULT_THRESHOLDS),
    anomalies: detectAnomalies(data, filters, forecast.history),
    byRoute: data.routes.map(route => ({ id: route.id, ...summarize(data, { ...filters, route: route.id }) })),
  };
}

function main(): void {
  const file = process.argv[2] ?? 'data/raw/t4f-demo.json';
  if (statSync(file).size > 5_000_000) throw new Error('Snapshot excede o limite local de 5 MB.');
  const content = readFileSync(file);
  if (content.length > 5_000_000) throw new Error('Snapshot excede o limite local de 5 MB.');
  const result = exportAnalysis(JSON.parse(content.toString('utf8')) as unknown);
  process.stdout.write(JSON.stringify({ datasetSha256: createHash('sha256').update(content).digest('hex'), ...result }));
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try { main(); }
  catch (error: unknown) {
    process.stderr.write(`Falha na análise T4F: ${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 2;
  }
}
