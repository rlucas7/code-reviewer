# the actual prompt goes here, you interpolate the patch
text1 = """A pull request is made on a code repository with the following changes:

```
{}
```

Your task is to review this code and make a suggested edit to the code that is in patch form.
The patch should be directly applicable to the repository via a `git apply` command,
and *must* pass `git apply --check` without errors.
If these are new files being added, the patch should *only* contain
`--- /dev/null` and `+++ b/filename` lines for each file.
Do *not* include `--- a/filename` lines in the patch, as this will cause `git apply` to fail.
Make absolutely sure the patch format is correct.
Double check your patch to ensure it conforms to the expected format for new files.
For example, a valid patch for a new file would look like this:

```diff
--- /dev/null
+++ b/new_file.py
@@ -0,0 +1,1 @@
+print(\"Hello, world!\")
```"""

# this is the system prompt:
# We can inject the `commit_id` into the system prompt here and the `path`
si_text1 = """You are a software developer trying to improve your colleagues code through a code review.
Please provide any comments with code changes in the form of suggestions via a json blob like this
{ \"body\":\"```suggestion\\n<some blob of code changes here>\\n```\\n the function should have a docstring\",
  \"commit_id\":\"{}\",
  \"path\":\"{}\",
  \"start_line\":1,
  \"start_side\":\"RIGHT\",
  \"line\":2,
  \"side\":
  \"RIGHT\"
}.
Note that the \"line\" value must be greater than the \"start_line\" value.
"""
