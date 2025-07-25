/**
 * Commitlint\u00a0\u2212 Conventional Commit rules.
 */
export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "subject-case": [2, "never", ["sentence-case"]],
  },
};
