package ggtesla.authz

default allow = false

allow {
  input.user.role == "admin"
}

allow {
  input.action == "report:read"
  input.user.role == "analyst"
}
