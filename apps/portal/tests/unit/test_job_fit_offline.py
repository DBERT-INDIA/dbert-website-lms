from services.ai.ats_engine import compare_job_skills


def test_job_skills_are_specific_and_stable():
    result = compare_job_skills(
        "Sample inventory project built with React.js and NodeJS. Created a PostgreSQL schema.",
        "React, Node.js, SQL, Docker, PostgreSQL, Docker",
    )
    assert result["matched"] == ["React", "Node.js", "PostgreSQL"]
    assert result["missing"] == ["SQL", "Docker"]
    assert [step["href"] for step in result["next_steps"]] == ["/search?q=SQL", "/search?q=Docker"]


def test_job_skills_keep_punctuation_and_handle_unknown_terms():
    result = compare_job_skills("Wrote C++ exercises", "C++ and C# are useful. iOS is optional.")
    assert result["matched"] == ["C++"]
    assert result["missing"] == ["C#", "iOS"]
    assert result["next_steps"][0]["href"] == "/search?q=C%23"
    assert compare_job_skills("Sample", "Unrecognized capability")["matched"] == []
