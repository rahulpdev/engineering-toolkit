# CI/CD And Deployment

## DigitalOcean Deployment (Terraform + DOCR)

- Employ specific image SHA digests in Terraform for DigitalOcean App Platform services; tag resolution for manifest lists is unreliable.
- Ensure tags point to runnable image manifests, not intermediary structures. `docker push <repository>:<tag>` can result in manifest list tags in DigitalOcean Container Registry (DOCR).
- Specify the `digest` attribute within the `image` block for `digitalocean_app` resources in Terraform. Example:

  ```hcl
  # ...
  image {
    registry_type = "DOCR"
    repository    = "your-registry/your-image"
    digest        = "sha256:abcdef0123456789..." # MANDATORY for reliability
  }
  # ...
  ```

## Digest-Based Image Update Process

1. Build Docker image; push to DOCR.
2. Secure full SHA256 digest of the specific image manifest.
3. Update `digest` in Terraform configuration.
4. Execute `terraform apply`.

## Python Applications In Docker

- Ensure consistent Python module resolution and avoid `ImportError` during deployment:

  - Use absolute imports that reference modules from the application's designated root directory within the Docker container (commonly `/app` if `WORKDIR /app` is used).
  - In `Dockerfile`, always explicitly set the `PYTHONPATH` environment variable to this application root. For example: `ENV PYTHONPATH=/app`.
  - Align local development environment (e.g., IDE project settings, virtual environment activation scripts) to mirror this `PYTHONPATH` setup.
