FROM rust:1.82-alpine AS build
WORKDIR /app
COPY . .
RUN cargo build --release

FROM alpine:3.20
WORKDIR /app
COPY --from=build /app/target/release/* /usr/local/bin/
CMD ["sh", "-lc", "exec $(ls /usr/local/bin | head -1)"]
