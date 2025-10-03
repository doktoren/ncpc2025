# Commit Command

Create a git commit following the NCPC 2025 repository workflow.

## Steps

1. **Run complete test and lint suite**:
   ```bash
   ./test_and_lint.sh
   ```

2. **Regenerate documentation** (if code changes were made):
   ```bash
   ./update_docs.sh && cd ..
   ```

3. **Review changes**:
   - Run `git status` to see modified files
   - Run `git diff` to review changes
   - Ensure all changes are intentional

4. **Stage and commit**:
   - Stage relevant files with `git add`
   - Create commit with descriptive message


## Important Notes

- **Always regenerate PDFs** before committing if any algorithm code was modified
- **All tests must pass** before committing
- **Follow existing commit message style** (check `git log` for patterns)
- **Never commit** without running test_and_lint.sh first
- **Do not push** unless explicitly requested by user
