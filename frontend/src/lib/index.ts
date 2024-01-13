// place files you want to import through the `$lib` alias in this folder.
export function cx(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}
