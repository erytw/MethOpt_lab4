export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  const W = ctx.W;
  const H = ctx.H;
  ctx.addShape(slide, { x: 0, y: 0, w: W, h: H, fill: "#101820" });
  ctx.addShape(slide, { x: 0, y: 0, w: 14, h: H, fill: "#f59e0b" });
  ctx.addText(slide, {
    x: 72, y: 70, w: 820, h: 42,
    text: "Лабораторная работа 4",
    fontSize: 24, color: "#fbbf24", bold: true,
  });
  ctx.addText(slide, {
    x: 72, y: 150, w: 1040, h: 150,
    text: "Трек 4. Стохастический линейный поиск",
    fontSize: 54, color: "#f8fafc", bold: true, typeface: ctx.fonts.title,
  });
  ctx.addText(slide, {
    x: 76, y: 330, w: 980, h: 68,
    text: "SLS подбирает шаг на текущем мини-батче по условию Армихо и снижает ручную настройку learning rate.",
    fontSize: 26, color: "#cbd5e1",
  });
  ctx.addText(slide, {
    x: 76, y: 530, w: 620, h: 80,
    text: "Пакет №1: Log-Cosh regression + Exponential classification\nЭксперимент: bodyfat, Log-Cosh, L2",
    fontSize: 22, color: "#e2e8f0",
  });
  ctx.addText(slide, {
    x: 1030, y: 620, w: 170, h: 32,
    text: "Track 4",
    fontSize: 18, color: "#f8fafc", align: "right",
  });
  return slide;
}
