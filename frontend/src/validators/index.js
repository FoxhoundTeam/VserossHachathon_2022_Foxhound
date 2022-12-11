export const required = (value) => !!value || "Данное поле обязательно.";
export const isEmail = (v) =>
  !v ||
  /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,4})+$/.test(v) ||
  "Введите корректный email.";
