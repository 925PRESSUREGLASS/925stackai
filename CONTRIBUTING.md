# Contributing

We use **trunk-based development** and **Conventional Commits**.

1.  **Create a branch**  
    ```
    # feat, fix, chore, docs, test, refactor …
    git checkout -b feat/<slug>
    ```

2.  **Run the generator**  
    Follow the Codex prompt->patch->lint->test workflow already documented.

3.  **Commit style**  
    ```
    feat(memory): expose vector memory tool
    fix(quote): handle missing price gracefully
    ```

4.  **Open a Pull Request**  
    * One reviewer minimum  
    * CI must pass  
    * Use **Squash & Merge**; the squash message should follow Conventional Commits.

5.  **Do *not* push directly to `main`.**
