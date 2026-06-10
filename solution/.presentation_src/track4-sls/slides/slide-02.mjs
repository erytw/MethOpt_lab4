const formulaPath = "/Users/erytw/Documents/AI360/MethOpt/Lab4/solution/output/track4/armijo_formula.png";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: "#f8fafc" });
  ctx.addText(slide, {
    x: 58, y: 42, w: 340, h: 28,
    text: "ПОСТАНОВКА",
    fontSize: 16, color: "#b45309", bold: true,
  });
  ctx.addText(slide, {
    x: 58, y: 80, w: 980, h: 66,
    text: "Армихо проверяется не на всей функции, а на фиксированном мини-батче.",
    fontSize: 36, color: "#111827", bold: true, typeface: ctx.fonts.title,
  });
  ctx.addShape(slide, {
    x: 88, y: 190, w: 1120, h: 76,
    fill: "#fff7ed",
  });
  await ctx.addImage(slide, {
    path: formulaPath,
    x: 170, y: 200, w: 940, h: 58,
    fit: "contain",
    alt: "Условие Армихо на фиксированном мини-батче",
  });
  ctx.addText(slide, {
    x: 90, y: 320, w: 500, h: 210,
    text: "Зачем это нужно\n\n- шаг адаптируется к локальной геометрии батча\n- не требуется вычислять F(x) на всей выборке\n- можно сравнить с лучшим ручным расписанием шага",
    fontSize: 24, color: "#1f2937",
  });
  ctx.addText(slide, {
    x: 690, y: 320, w: 450, h: 210,
    text: "Ограничение\n\nЕсли батч слишком мал, оценка f_I шумная. Тогда условие Армихо может принять слишком большой или слишком маленький шаг.",
    fontSize: 24, color: "#1f2937",
  });
  ctx.addShape(slide, { x: 58, y: 650, w: 1160, h: 2, fill: "#e5e7eb" });
  return slide;
}
