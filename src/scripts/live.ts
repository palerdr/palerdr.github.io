/**
 * While a transition sweeps, the stage holds a copy of the page being left so
 * the hand can erase it. The copy is a picture, not a page — but it is real
 * markup in the document, and it sits in front of the live page in tree order,
 * so a plain document.querySelector finds it first and hands a component the
 * wrong element to drive. A clock bound to the copy ticks a frozen dial.
 *
 * Every component that wires itself up on astro:page-load should look for its
 * root through these, so it always binds to the page you are arriving at.
 */
const copied = (el: Element) => el.closest('[data-stage]') !== null;

export function live<T extends Element>(selector: string): T | null {
  for (const el of document.querySelectorAll<T>(selector)) {
    if (!copied(el)) return el;
  }
  return null;
}

export function allLive<T extends Element>(selector: string): T[] {
  return [...document.querySelectorAll<T>(selector)].filter((el) => !copied(el));
}
