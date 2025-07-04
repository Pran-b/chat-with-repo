import os
import zipfile
import tempfile
import shutil
import git


def process_repo(repo_url=None, zip_path=None):
    """
    Clones a GitHub repo or extracts a zip file and returns the local repo path.
    """
    if repo_url:
        tmpdir = tempfile.mkdtemp()
        try:
            git.Repo.clone_from(repo_url, tmpdir)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to clone repo: {e}")
        return tmpdir

    elif zip_path:
        tmpdir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to extract zip: {e}")

        # If repo contents are in a nested folder, adjust
        contents = os.listdir(tmpdir)
        if len(contents) == 1:
            nested = os.path.join(tmpdir, contents[0])
            if os.path.isdir(nested):
                return nested

        return tmpdir

    else:
        raise ValueError("Either repo_url or zip_path must be provided.")
