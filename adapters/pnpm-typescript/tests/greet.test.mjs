import assert from "node:assert/strict";
import { test } from "node:test";
import { greet } from "../src/greet.ts";

test("greets a named person", () => {
  assert.equal(greet("Ada"), "Hello, Ada!");
});
