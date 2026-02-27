package ggtesla.authz

default allow = false

allow {
    input.role == "admin"
}

allow {
    input.role == "user"
    input.action == "read"
}

deny {
    contains(input.message, "banned_word")
}
