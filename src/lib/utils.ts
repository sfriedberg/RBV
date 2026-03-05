export function cn(...classes: (string | undefined | null | false)[]) {
  return classes.filter(Boolean).join(" ");
}

export function lerp(start: number, end: number, t: number) {
  return start + (end - start) * Math.max(0, Math.min(1, t));
}

export function mapRange(
  value: number,
  inMin: number,
  inMax: number,
  outMin: number,
  outMax: number
) {
  const t = (value - inMin) / (inMax - inMin);
  return lerp(outMin, outMax, t);
}
