const convergencePath = "/Users/erytw/Documents/AI360/MethOpt/Lab4/solution/output/track4/track4_convergence.png";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: "#f8fafc" });
  ctx.addText(slide, {
    x: 58, y: 38, w: 340, h: 28,
    text: "ЭКСПЕРИМЕНТ",
    fontSize: 16, color: "#b45309", bold: true,
  });
  ctx.addText(slide, {
    x: 58, y: 74, w: 920, h: 50,
    text: "SLS сравнивался с лучшим ручным inverse sqrt.",
    fontSize: 34, color: "#111827", bold: true, typeface: ctx.fonts.title,
  });
  await ctx.addImage(slide, {
    path: convergencePath,
    x: 58, y: 145, w: 780, h: 490,
    fit: "contain",
    alt: "График сходимости SLS и ручного SGD",
  });
  ctx.addText(slide, {
    x: 880, y: 160, w: 300, h: 210,
    text: "Данные\nbodyfat\nm = 252, n = 14\nbatch = 32\n80 эпох\n\nФункция\nLog-Cosh + L2",
    fontSize: 24, color: "#1f2937",
  });
  ctx.addText(slide, {
    x: 880, y: 430, w: 300, h: 150,
    text: "Итог\nmanual: 0.000992\nSLS: 0.000958\n\nSLS немного глубже, без ручного расписания.",
    fontSize: 23, color: "#111827", bold: true,
  });
  return slide;
}
