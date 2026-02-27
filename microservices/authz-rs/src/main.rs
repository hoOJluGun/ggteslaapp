#[tokio::main]
async fn main() {
    let nats = std::env::var("NATS_URL").unwrap_or_else(|_| "nats://localhost:4222".to_string());
    println!("service starting with NATS: {}", nats);
    // TODO: subscribe/publish JetStream events for service-specific workflows.
}
