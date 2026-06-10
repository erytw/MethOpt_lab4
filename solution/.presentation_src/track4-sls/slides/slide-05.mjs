const alphaPath = "/Users/erytw/Documents/AI360/MethOpt/Lab4/solution/output/track4/track4_alpha.png";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: "#ffffff" });
  ctx.addText(slide, {
    x: 58, y: 38, w: 340, h: 28,
    text: "ВЫВОДЫ",
    fontSize: 16, color: "#b45309", bold: true,
  });
  ctx.addText(slide, {
    x: 58, y: 74, w: 990, h: 50,
    text: "SLS быстро находит рабочий масштаб шага и дальше держит его в шумовой зоне.",
    fontSize: 32, color: "#111827", bold: true, typeface: ctx.fonts.title,
  });
  await ctx.addImage(slide, {
    path: alphaPath,
    x: 58, y: 150, w: 690, h: 440,
    fit: "contain",
    alt: "График адаптации шага SLS",
  });
  ctx.addText(slide, {
    x: 790, y: 165, w: 380, h: 320,
    text: "Главные наблюдения\n\n- начальный alpha = 1 слишком велик, поэтому бэктрекинг резко уменьшает шаг\n- после первых эпох alpha стабилизируется около 6e-4\n- малый батч делает проверку Армихо шумной, отсюда локальные скачки\n- цена SLS выше по времени: 0.104 с против 0.040 с",
    fontSize: 23, color: "#1f2937",
  });
  ctx.addText(slide, {
    x: 790, y: 545, w: 380, h: 64,
    text: "Вывод: SLS полезен, когда ручная настройка шага дороже дополнительных батчевых проверок.",
    fontSize: 22, color: "#111827", bold: true,
  });
  return slide;
}
