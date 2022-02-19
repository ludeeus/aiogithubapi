"""Example GrapQL Query to get repository tags."""

EXAMPLE_QUERY = """
query ($owner: String!, $repository: String!, $number_of_tags: Int = 1) {
  repository(owner: $owner, name: $repository) {
    refs(
      refPrefix: "refs/tags/"
      first: $number_of_tags
      orderBy: {field: TAG_COMMIT_DATE, direction: DESC}
    ) {
      tags: nodes {
        name
      }
    }
  }
}
"""
