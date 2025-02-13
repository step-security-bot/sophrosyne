"""sophrosyne module.

This module contains the sophrosyne application logic. The sophrosyne application is
responsible for handling the incoming requests, classifying the content, and
returning the classification results.

The application is divided into the following modules:
    - api: The API module contains the FastAPI application and the API routers.
    - core: The core module contains the core logic of the application, such as
            database operations and configuration.
    - grpc: The gRPC module contains autogenerated gRPC client code used to
            communicate with upstream services.

The application is started by running the main module. The main module creates
the FastAPI application and starts the uvicorn server. Requests are received by
the FastAPI application and routed to the appropriate API endpoint. The API is
in the style of a RPC-over-HTTP API, where each endpoint corresponds to a
specific action. The API is __not__ RESTful and does not follow RESTful design
principles.

The application serves an OpenAPI schema at the `/.well-known/openapi` endpoint.
Additionally, the application serves a ReDoc UI at the `/docs` endpoint.
"""
