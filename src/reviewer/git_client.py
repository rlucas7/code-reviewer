"""This module houses the client that is used to interact with the remote git
   instance.
   For now we focus on use with github as the remote client.
"""
from configparser import ConfigParser
from typing import Optional
from github import Auth, Github

config = ConfigParser()
config.read('./codeconfig.ini')

# NOTE: we'll want a superclass once we include others here
class GH:
    def __init__(self, cfg: Optional[ConfigParser] = None, repo: str = ""):
        if not cfg:
            self.auth = Auth.Token(config['DEFAULT']['github_pat'])
        else:
            self.auth = Auth.Token(cfg['DEFAULT']['github_pat'])
        self.client = Github(auth=self.auth)
        # TODO: make PR and repo as args to constructor
        self.repo = self.client.get_repo("rlucas7/suggerere")

    def collect_pr_patches(self, pr_id: int) -> list[str]:
        """The patches are stored ina nested structure:
        PR <- Commits <- Files <- Patches
        So we iterate through these and return them
        """
        patches = []
        pr = self.repo.get_pull(pr_id)
        for commit in pr.get_commits():
            for file in commit.files:
                # TODO: figure out if we want to include the files just prior to the patch itself
                # similar to how git would do this in cli...
                patches.append(file.raw_data)
        return patches

    def create_comment(self, pr_id: int, comment: dict[str, str]):
        """This function is responsible for generating a comment given the input"""
        pr = self.repo.get_pull(pr_id)
        last_commit = pr.get_commits()[pr.commits - 1]
        comment = pr.create_comment(
            body=comment.get('body'),
            commit=last_commit,
            path=comment.get('path'),
            position=comment.get('start_line')
        )
        print(comment)

# NOTE: for now this is a separate class this decision is tentative
class PatchCollator:
    def __init__(self, patches: list[str]):
        self.patches = patches
        self._collated_patches = self._collate()

    def _collate(self) -> list[str]:
        """Collates the patches into a single string for the ai.
        We assume the patches are 'raw data' from github-for now.
        """
        cp = []
        for rd_patch in self.patches:
            cp.append(rd_patch.get('filename') + '\n')
            cp.append(rd_patch.get('patch') + '\n')
        return cp

    def get_collated_patches(self) -> str:
        return "".join(self._collated_patches)

if __name__ == "__main__":
    print("this is just for spot checking...")
    gh = GH(cfg=config['DEFAULT']['github_pat'])
    pr_patches = gh.collect_pr_patches()
    collator = PatchCollator(pr_patches)
    print(collator._collated_patches)
    # now that we have the raw data for the patches we need to handle the preparation...
    # the preparation goes into the
    print("this was just for spot checking...")