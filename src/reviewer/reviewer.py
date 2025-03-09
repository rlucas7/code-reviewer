"""This file houses the code reviewer class.
Code reviewer is responsible for orchestration of code reviews.
"""

from google.genai import types # type: ignore

from git_client import GH, PatchCollator
from ai_client import AIClient, text1


class CodeReviewer:
    def __init__(self):
        self.ai_client = AIClient()
        self.gh_client = GH()



    def review_pr(self, pr_id: int) -> None:
        """This code is responsible for orchestrating the automatic code review.

        Args:
            pr_id (int): The id of the pull request on the repo.
        """
        pr_patches = self.gh_client.collect_pr_patches(pr_id)
        collator = PatchCollator(pr_patches)
        print(collator._collated_patches)
        # collator._collated_patches <- is list where (idx, idx+1) are (path, patch)
        contents = [types.Content(role="user", parts=[text1])]
        review = self.ai_client.generate_code_review(contents=contents)
        print(review)
        print("now do the review")
        self.gh_client.create_comment(pr_id, review)


if __name__ == "__main__":
    print("... this is for testing only ...")
    cr = CodeReviewer()
    cr.review_pr(1)
    print("... all done testing only ...")