from prodapi_cli.settings import NewProjectSettings


def test_that_project_slug_is_added_from_project_name():
    s = NewProjectSettings(
        project_name="My Project",
        path="/home/projects/proj",
    )
    assert s.project_slug == "my-project"
