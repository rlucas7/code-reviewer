"""This file includes the client which  is responsible for interacting with the ai."""

from json import loads
from google import genai
from google.genai import types # type: ignore
from pydantic import BaseModel # type: ignore

# NOTE: in practice these come from a pull request/change set
patches = """
--- /dev/null
+++ b/src/collections2/multiply.py
@@ -0,0 +1,2 @@
+def multiply(x, y):
+   return x*y
--- /dev/null
+++ b/tests/test_multiply.py
@@ -0,0 +1,15 @@
+from collections2.multiply import multiply
+
+import pytest
+
+# uncomment if needed
+#from unittest import TestCase
+
+
+
+class TestMultiply:
+   # you can use the parametrize fixture for concise looping like so
+   @pytest.mark.parametrize(\"a,b,expected\", [(3,5,15), (2,4,8)])
+   def test_multiply(self, a, b, expected):
+       assert multiply(a, b) == expected
+
"""

text1 = types.Part.from_text(text=f"""A pull request is made on a code repository with the following changes:

```
{patches}
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
```""")

# this is the system prompt:
# We can inject the `commit_id` into the system prompt here and the `path`
si_text1 = """You are a software developer trying to improve your colleagues code through a code review.
Please provide any comments with code changes in the form of suggestions via a json blob like this
{ \"body\":\"```suggestion\\n<some blob of code changes here>\\n```\\n the function should have a docstring\",
  \"commit_id\":\"90b82e3b2a91bb3f9f88a2ac4ca33d557027d71a\",
  \"path\":\"<filepath>\",
  \"start_line\":1,
  \"start_side\":\"RIGHT\",
  \"line\":2,
  \"side\":
  \"RIGHT\"
}.
Note that the \"line\" value must be greater than the \"start_line\" value.
"""

class Suggestion(BaseModel):
    body: str
    commit_id: str
    path: str
    start_line: int
    start_side: str
    line: int
    side: str

class AIClient:
    def __init__(self):
        # TODO: put these into config
        self.project_id = "my-project-1948-436821"
        self.model_name = "gemini-2.0-flash-001"
        self.region = "us-central1"
        self.sys_prompt = si_text1
        self.suggestion_model = Suggestion
        self.generation_config = types.GenerateContentConfig(
            temperature = 1,
            top_p = 0.95,
            max_output_tokens = 8192,
            response_modalities = ["TEXT"],
            response_mime_type='application/json', # NOTE: you need to be explicit here for custom schema
            safety_settings = [types.SafetySetting(
              category="HARM_CATEGORY_HATE_SPEECH",
              threshold="OFF"
            ),types.SafetySetting(
              category="HARM_CATEGORY_DANGEROUS_CONTENT",
              threshold="OFF"
            ),types.SafetySetting(
              category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
              threshold="OFF"
            ),types.SafetySetting(
              category="HARM_CATEGORY_HARASSMENT",
              threshold="OFF"
            )],
            system_instruction=[types.Part.from_text(text=self.sys_prompt)],
            response_schema=self.suggestion_model,
            )
        self.genai_client = genai.Client(
            vertexai=True,
            project=self.project_id,
            location=self.region,
        )

    def generate_code_review(self, contents:list[types.Content]) -> dict[str, str]:
        """Generate the code review for the pull request

        Args:
            contents (list[types.Content]): A list of the changes, the content
            is the prompt and the patches from the pull request.

        Returns:
            dict[str, str]: a dictionary with the input to a comment on github.
        """
        # NOTE this block of code comes direct from the console... I don't think we want the SSE,
        # we can wait and take the entire if that's feasible...
        # use: client.models.generate_content_stream() if you really want the stream...
        content = self.genai_client.models.generate_content(
            model = self.model_name,
            contents = contents,
            config = self.generation_config
        )
        # now process the content for posting as code review
        # TODO: make this handle > 1 candidate/part
        candidate = content.candidates[0]
        part = candidate.content.parts[0]
        completion = part.model_dump()
        suggestion = loads(completion['text'])
        # Now the `suggestion` should be in the format for github...
        return suggestion

if __name__ == "__main__":
    print("this is just for spot checking...")
    ai_client = AIClient()
    contents = [types.Content(role="user", parts=[text1])]
    cr = ai_client.generate_code_review(contents=contents)
    print(cr)
    print("this was just for spot checking...")