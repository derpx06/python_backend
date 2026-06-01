# Scalability Note

## Current Architecture

The application follows a layered architecture with clear separation of concerns:

```
Client (Next.js) → API Gateway (FastAPI) → Service Layer → Database (PostgreSQL)
```

Each layer has a single responsibility:
- **Routers**: HTTP request handling, input parsing
- **Services**: Business logic, authorization checks
- **Models**: Data persistence, schema definition
- **Middleware**: Cross-cutting concerns (auth, logging, error handling)

## Horizontal Scaling Strategy

### Application Layer

The FastAPI server runs with Uvicorn workers (configurable via `--workers` flag). In production:

- Deploy multiple instances behind a load balancer (NGINX, AWS ALB, or Kubernetes Ingress)
- Use the Dockerfile's multi-worker configuration: `uvicorn app.main:app --workers 4`
- Since JWT auth is stateless, any instance can handle any request — no sticky sessions needed

### Database Layer

- **Connection Pooling**: SQLAlchemy is configured with `pool_size=20, max_overflow=10` to efficiently manage database connections
- **Read Replicas**: For read-heavy workloads, configure PostgreSQL streaming replication and route read queries to replicas
- **PgBouncer**: Add a connection pooler like PgBouncer in front of PostgreSQL to handle thousands of concurrent connections

### Caching Layer (Future)

For frequently accessed data (task lists, user profiles):

- Add Redis as a caching layer with TTL-based expiration
- Cache GET responses and invalidate on mutations (POST/PUT/DELETE)
- Use Redis for rate limiting counters (replacing in-memory rate limits)
- Store revoked JWT token IDs in Redis for immediate token invalidation

## Microservices Evolution

The modular structure makes it straightforward to split into microservices:

```
                    ┌──────────────┐
                    │  API Gateway │
                    │   (NGINX)    │
                    └──────┬───────┘
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │   Auth   │ │  Tasks   │ │  Users   │
        │ Service  │ │ Service  │ │ Service  │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Auth DB  │ │ Tasks DB │ │ Users DB │
        └──────────┘ └──────────┘ └──────────┘
```

Each service would:
- Have its own database (database-per-service pattern)
- Communicate via HTTP/REST or gRPC for synchronous calls
- Use a message queue (RabbitMQ, Kafka) for async event-driven communication
- Be independently deployable and scalable

## Container Orchestration

The Docker Compose setup is designed for local development. For production:

- Use **Kubernetes** for container orchestration with:
  - Horizontal Pod Autoscaler (HPA) based on CPU/memory metrics
  - Liveness and readiness probes using the `/health` endpoint
  - Rolling deployments with zero downtime
- Or use managed services like AWS ECS, Google Cloud Run, or Azure Container Apps

## Logging & Monitoring

- **Structured logging** with Loguru — outputs to stdout (for container log aggregation) and rotating file logs
- Ready for integration with log aggregation tools (ELK Stack, Datadog, CloudWatch)
- The `/health` endpoint can be used by load balancers and monitoring systems
- Request timing is logged per-request for performance tracking

## Security at Scale

- JWT tokens are stateless — no session store needed across instances
- bcrypt with 12 salt rounds for password hashing
- Pydantic validation prevents malformed input from reaching business logic
- CORS restricted to specific frontend origins
- Rate limiting can be moved to Redis for distributed enforcement
