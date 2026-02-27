FROM rust:1.75-bullseye AS builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bullseye-slim
WORKDIR /app
COPY --from=builder /app/target/release/crdt-sync /app/service
CMD ["/app/service"]
