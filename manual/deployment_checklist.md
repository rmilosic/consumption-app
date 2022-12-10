
1. Stop and remove containers

```bash
docker compose down && docker compose rm
```

2. Pull latest changes

```bash
git fetch --all
git checkout 
```

3. [optional] Adapt environment variables

4. [optional] Adapt config files

5. Create containers
```bash
docker compose up -d
```