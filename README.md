# Reviewer
A bunch of code to make code reviews.

## pip installs

NOTE: these will go into a dependencies file once they stabilize a bit

If you want the env isolated then make a venv
```bash
pip install PyGithub
pip install --upgrade google-cloud-aiplatform
# actually the console says to use this latter one, not sure if we need both here?
pip install --upgrade google-genai
```

## Configuration

The file `example_codeconfig.ini` contains the structure of the config file.
To use the package you need to configure an actual configuration file by changing
this file via

```bash
mv example_codeconfig.ini codeconfig.ini
```

and then use your text editor to put in the necessary values.
Note that the package assumes the file is in this location at the repo root.

# editable install

Navigate to the directory that houses the starter and do:
first clone the repo from the remote and then
setup the development dependencies
```bash
python3  -m pip install -r dev-requirements.txt
```

then setup the dev editable install
```bash
python3 -m pip install -e .
```

now the local env has an editable install


# running tests

in the top level of the package you cloned locally do:
```bash
pytest  tests
```

if anything fails then try to get the cases to pass


# updating version
when you tag a commit for a release you must do:


```
git tag -a vX.Y.Z
```
o/w git won't find the tag.
In particular

```
git tag -s vX.Y.Z
```

won't work, so DO NOT do the latter

to get the cwd version number you do
```
python3 -m setuptools_scm
```

from top level directory.

To see all the files which are tracked you do
```
python3 -m setuptools_scm ls
```

If you amend a commit that already has a tag you need to update the
tag-commit relation to have the new tag. If your tag is vX.Y.Z and
the commit is `abcdef` after the amend then you do
```
git tag -f vX.Y.Z abcdef
```
to update the commit-tag relation so that setuptools_scm will pick up the
new tag.

when you push to the remote tags will not be updated in the push by default
so you need to do
```
git push --follow-tags
```
