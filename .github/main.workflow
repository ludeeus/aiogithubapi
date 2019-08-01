workflow "Release" {
  on = "release"
  resolves = ["Publish to PyPi"]
}

action "Publish to PyPi" {
  uses = "mariamrf/py-package-publish-action@v0.0.2"
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
}