import { describe, it, expect } from 'vitest';

describe('ApexSales Revenue Suite 001', () => {
  it('validates quota attainment calculation', () => {
    const closed = 2840000;
    const quota = 2000000;
    const attainment = (closed / quota) * 100;
    expect(attainment).toBe(142);
  });
});
