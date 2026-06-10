export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: "#ffffff" });
  ctx.addText(slide, {
    x: 58, y: 42, w: 340, h: 28,
    text: "АЛГОРИТМ",
    fontSize: 16, color: "#b45309", bold: true,
  });
  ctx.addText(slide, {
    x: 58, y: 80, w: 1040, h: 58,
    text: "SLS делает обычный SGD-шаг, но alpha выбирается бэктрекингом.",
    fontSize: 34, color: "#111827", bold: true, typeface: ctx.fonts.title,
  });
  const rows = [
    ["1", "Выбираем мини-батч I и считаем g = grad f_I(x)."],
    ["2", "Берем стартовый alpha = rho * alpha_prev, чтобы метод мог разгоняться."],
    ["3", "Пока условие Армихо не выполнено, уменьшаем alpha <- gamma * alpha."],
    ["4", "Обновляем x <- x - alpha * g и сохраняем alpha для следующей итерации."],
  ];
  for (let i = 0; i < rows.length; i += 1) {
    const y = 180 + i * 95;
    ctx.addShape(slide, { x: 80, y, w: 54, h: 54, fill: "#f59e0b" });
    ctx.addText(slide, {
      x: 80, y: y + 9, w: 54, h: 34,
      text: rows[i][0],
      fontSize: 24, color: "#ffffff", bold: true, align: "center",
    });
    ctx.addText(slide, {
      x: 165, y: y + 2, w: 940, h: 56,
      text: rows[i][1],
      fontSize: 25, color: "#1f2937",
    });
  }
  ctx.addText(slide, {
    x: 80, y: 585, w: 1040, h: 46,
    text: "В реализации batch_idx не меняется внутри цикла линейного поиска.",
    fontSize: 22, color: "#475569", fill: "#f1f5f9",
    insets: { left: 18, right: 18, top: 10, bottom: 10 },
  });
  return slide;
}
